from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig
from networksecurity.entity.config_entity import TrainingpipelineConfig
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_tranformation import DataTransformation,DataTransformationConfig
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.entity.config_entity import ModelTrainerConfig
import sys

if __name__=="__main__":
    try:
        training_pipeline_config=TrainingpipelineConfig()
        data_ingestion_config=DataIngestionConfig(training_pipeline_config)
        data_ingestion=DataIngestion(data_ingestion_config)
        logging.info("Initiate the data ingestion")
        dataingestionartifact=data_ingestion.initate_data_ingestion()
        logging.info("Data initiation completed")

        data_validation_config=DataValidationConfig(training_pipeline_config)
        data_validation=DataValidation(dataingestionartifact,data_validation_config)
        logging.info("Inititate the data validation")
        datavalidationartifact=data_validation.initiate_data_validation()
        logging.info("Data Validation Completed")
        print(dataingestionartifact)

        data_transformation_config=DataTransformationConfig(training_pipeline_config)
        logging.info("Data Transformation started")
        data_transformation=DataTransformation(datavalidationartifact,data_transformation_config)
        data_transformation_artifact=data_transformation.initiate_data_transformation()
        logging.info("Data Transformation completed")
        print(data_transformation_artifact)

        logging.info("Model Trainer started")
        model_trainer_config=ModelTrainerConfig(training_pipeline_config)
        model_trainer=ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
        model_transformation_artifact=model_trainer.initiate_model_trainer()
        logging.info("Model training completed")

    except Exception as e:
        raise NetworkSecurityException(e,sys)