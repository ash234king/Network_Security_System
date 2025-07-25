import os
import sys

import mlflow.sklearn
import pickle
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.artifact_entity import DataTranformationArtifact,ModelTrainerArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig

from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utils import save_object,load_object
from networksecurity.utils.main_utils.utils import load_numpy_array_data,evaluate_models
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import(
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier
)
import mlflow
from urllib.parse import urlparse
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")

print("MLFLOW_TRACKING_USERNAME:", os.getenv("MLFLOW_TRACKING_USERNAME"))
print("MLFLOW_TRACKING_PASSWORD:", os.getenv("MLFLOW_TRACKING_PASSWORD"))
print("MLFLOW_TRACKING_URI:", os.getenv("MLFLOW_TRACKING_URI"))

os.environ["MLFLOW_TRACKING_URI"]=os.getenv("MLFLOW_TRACKING_URI")
os.environ["MLFLOW_TRACKING_USERNAME"] = os.getenv("MLFLOW_TRACKING_USERNAME")
os.environ["MLFLOW_TRACKING_PASSWORD"] = os.getenv("MLFLOW_TRACKING_PASSWORD")


class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:DataTranformationArtifact):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def track_mlflow(self,best_model,Classifiactionmetric,stage="train"):
        mlflow.set_registry_uri("MLFLOW_TRACKING_URI")
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
        with mlflow.start_run():
            mlflow.set_tag("stage",stage)
            mlflow.set_tag("model_name",best_model.__class__.__name__)
            f1_score=Classifiactionmetric.f1_score
            precision_score=Classifiactionmetric.precision_score
            recall_score=Classifiactionmetric.recall_score

            mlflow.log_metric(f"{stage}_f1_score",f1_score)
            mlflow.log_metric(f"{stage}_precision",precision_score)
            mlflow.log_metric(f"{stage}_recall_score",recall_score)
            local_model_path = f"final_models/{stage}_model.pkl"
            with open(local_model_path, 'wb') as f:
                pickle.dump(best_model, f)
        
            mlflow.log_artifact(local_model_path, artifact_path=f"{stage}_model")



    def train_model(self,x_train,y_train,x_test,y_test):
        models={
            "Random Forest": RandomForestClassifier(verbose=1),
            "Decision Tree":DecisionTreeClassifier(),
            "Gradient Boosting":GradientBoostingClassifier(verbose=1),
            "Logistic Regression":LogisticRegression(verbose=1),
            "Adaboost": AdaBoostClassifier(),
            "Kneighbors Classifier":KNeighborsClassifier()
        }
        params={
            "Decision Tree":{
                'criterion':['gini','entropy','log_loss'],
                'splitter':['best','random'],
                'max_features':['sqrt','log2']
            },
            "Random Forest":{
                'criterion':['gini','entropy','log_loss'],
                'max_features':['sqrt','log2',None],
                'n_estimators':[8,16,32,64,128,256]
            },
            "Gradient Boosting":{
                'loss':['log_loss','exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.8,0.85],
                'criterion':['squared_error','friedman_mse'],
                'max_features':['auto','sqrt','log2'],
                'n_estimators':[8,16,32,64,128]
            },
            "Logistic Regression":{},
            "Adaboost":{
                'learning_rate':[.1,.01,0.5,.001],
                'n_estimators':[8,16,32,64,128]
            },
            "Kneighbors Classifier":{
                'n_neighbors': [3, 5, 7, 9, 11],
                'weights': ['uniform', 'distance'],
                'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
                'metric': ['minkowski', 'euclidean', 'manhattan']
            }
        }

        model_report:dict=evaluate_models(x_train=x_train,y_train=y_train,x_test=x_test,y_test=y_test,models=models,param=params)
        best_model_score=max(sorted(model_report.values()))

        best_model_name=list(model_report.keys())[list(model_report.values()).index(best_model_score)]
        best_model=models[best_model_name]
        y_train_pred=best_model.predict(x_train)
        classification_train_metric=get_classification_score(y_true=y_train,y_pred=y_train_pred)
        
        ##function to track the mlflow
        self.track_mlflow(best_model,classification_train_metric,stage="train")

        y_test_pred=best_model.predict(x_test)
        classification_test_metric=get_classification_score(y_true=y_test,y_pred=y_test_pred)
        self.track_mlflow(best_model,classification_test_metric,stage="test")
        preprocessor=load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
        model_dir_path=os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path,exist_ok=True)
        Network_Model=NetworkModel(preprocessor=preprocessor,model=best_model)
        save_object(self.model_trainer_config.trained_model_file_path,obj=NetworkModel)
        save_object("final_models/model.pkl",best_model)

        ##Model trainer Artifact
        model_trainer_artifact=ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                             train_metric_artifact=classification_train_metric,
                             test_metric_artifact=classification_test_metric
                             )
        logging.info(f"Model trainer artifact: {model_trainer_artifact}")
        return model_trainer_artifact


    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            train_file_path=self.data_transformation_artifact.transformed_train_file_path
            test_file_path=self.data_transformation_artifact.transformed_test_file_path

            train_arr=load_numpy_array_data(train_file_path)
            test_arr=load_numpy_array_data(test_file_path)

            x_train,y_train,x_test,y_test=(
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )
            model=self.train_model(x_train,y_train,x_test,y_test)
        except Exception as e:
            raise NetworkSecurityException(e,sys)