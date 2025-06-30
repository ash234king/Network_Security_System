import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os,sys
import numpy as np
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import r2_score
import warnings
warnings.filterwarnings("ignore")
#import dill
import pickle

def read_yaml_file(file_path: str)->dict:
    try:
        with open(file_path,"rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def write_yaml_file(file_path:str,content: object,replace:bool=False):
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"w") as file:
            yaml.dump(content,file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    

def save_numpy_array_data(file_path: str,array: np.array):
    try:
        
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            np.save(file_obj,array)
        
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e
    
def save_object(file_path: str, obj: object)->None:
    try:
        logging.info("Entered the save_object method of MainUtils class")
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"wb") as file_obj:
            pickle.dump(obj,file_obj)
        logging.info("Exited the save_object method of MainUtils class")
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e


def load_object(file_path:str)->object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} does not exists")
        with open(file_path,"rb") as file_obj:
            print(file_obj)
            return pickle.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e

def load_numpy_array_data(file_path:str)->np.array:
    try:
        with open(file_path,"rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e

def evaluate_models(x_train,y_train,x_test,y_test,models,param):
    try:
        report={}
        for model_name,model in models.items():
            para=param[model_name]
            gs=RandomizedSearchCV(
                estimator=model,
                param_distributions=para,
                n_iter=10,
                cv=3,
                scoring='r2',
                n_jobs=-1,
                verbose=1,
                random_state=42
            )
            gs.fit(x_train,y_train)
            best_model=gs.best_estimator_
            y_train_pred=best_model.predict(x_train)
            y_test_pred=best_model.predict(x_test)
            train_model_score=r2_score(y_train,y_train_pred)
            test_model_score=r2_score(y_test,y_test_pred)
            report[model_name]=test_model_score
        return report
    except Exception as e:
        raise NetworkSecurityException(e,sys)