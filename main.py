from network_security.logging.logger import logging
from network_security.exception.exception import NetworkSecurityException
from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_validation import DataValidation
from network_security.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig
import sys

if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(traning_pipeline_config=training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        logging.info("Data Ingestion started")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data Ingestion completed")

        print(data_ingestion_artifact)


        data_validation_config = DataValidationConfig(traning_pipeline_config=training_pipeline_config)
        data_validation = DataValidation(data_validation_config=data_validation_config, data_ingestion_artifact=data_ingestion_artifact)
        logging.info("Data Validation started")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data Validation completed")

        print(data_validation_artifact)

    except Exception as e:
        logging.error(f"Error occured in main module {str(e)}")
        raise NetworkSecurityException(e, sys)