import sys
from network_security.logging.logger import logging
from network_security.components.model_trainer import ModelTrainer
from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_validation import DataValidation
from network_security.exception.exception import NetworkSecurityException
from network_security.components.data_transformation import DataTransformation
from network_security.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig

if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(traning_pipeline_config=training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        logging.info("Data Ingestion started")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data Ingestion completed")


        data_validation_config = DataValidationConfig(traning_pipeline_config=training_pipeline_config)
        data_validation = DataValidation(data_validation_config=data_validation_config, data_ingestion_artifact=data_ingestion_artifact)
        logging.info("Data Validation started")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data Validation completed")

        logging.info("Data Transformation started")
        data_transformation_config = DataTransformationConfig(traning_pipeline_config=training_pipeline_config)
        data_transformation = DataTransformation(data_transformation_config=data_transformation_config, data_validation_artifact= data_validation_artifact)
        data_transformation_artifact =data_transformation.initiate_data_transformation()
        logging.info("Data Transformation completed")
        
        model_trainer_config = ModelTrainerConfig(traning_pipeline_config=training_pipeline_config)
        model_trainer = ModelTrainer(model_trainer_config=model_trainer_config, data_transformation_artifact=data_transformation_artifact)
        logging.info("Model Trainer started")
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        logging.info("Model Trainer completed")

        print(model_trainer_artifact)
    except Exception as e:
        logging.error(f"Error occured in main module {str(e)}")
        raise NetworkSecurityException(e, sys)