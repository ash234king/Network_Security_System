from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig
from networksecurity.entity.config_entity import TrainingpipelineConfig
from networksecurity.components.data_validation import DataValidation
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
    except Exception as e:
        raise NetworkSecurityException(e,sys)