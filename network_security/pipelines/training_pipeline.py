import os
import sys
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_validation import DataValidation
from network_security.components.data_transformation import DataTransformation
from network_security.components.model_trainer import ModelTrainer
from network_security.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact, ModelTrainerArtifact
from network_security.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig, TrainingPipelineConfig


class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()

    def start_data_ingestion(self):
        try:
            data_ingestion_config = DataIngestionConfig(traning_pipeline_config= self.training_pipeline_config)
            logging.info("Data Ingestion started")
            data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
            data_ingestion_artifacts = data_ingestion.initiate_data_ingestion()
            logging.info("Data Ingestion completed")
            return data_ingestion_artifacts
        except Exception as e:
            logging.error(f"Error occured in start_data_ingestion class {str(e)}")
            raise NetworkSecurityException(e, sys)
        
    def start_data_validation(self, data_ingestion_artifacts:DataIngestionArtifact):
        try:
            data_validation_config = DataValidationConfig(traning_pipeline_config=self.training_pipeline_config)
            logging.info("Data Validation started")
            data_validation = DataValidation(data_validation_config=data_validation_config,data_ingestion_artifact=data_ingestion_artifacts)
            data_validation_artifacts = data_validation.initiate_data_validation()
            logging.info("Data Validation completed")
            return data_validation_artifacts
        except Exception as e:
            logging.error(f"Error occured in start_data_validation class {str(e)}")
            raise NetworkSecurityException(e, sys)
    
    def start_data_transformation(self,data_validation_artifacts:DataValidationArtifact):
        try:
            data_transformation_config = DataTransformationConfig(traning_pipeline_config=self.training_pipeline_config)
            logging.info("Data Transformation started")
            data_transformation = DataTransformation(data_transformation_config=data_transformation_config,data_validation_artifact=data_validation_artifacts)
            data_transformation_artifacts = data_transformation.initiate_data_transformation()
            logging.info("Data Transformation completed")
            return data_transformation_artifacts
        except Exception as e:
            logging.error(f"Error occured in start_data_transformation class {str(e)}")
            raise NetworkSecurityException(e, sys)
        
    def start_model_trainer(self,data_transformation_artifacts:DataTransformationArtifact):
        try:
            model_trainer_config = ModelTrainerConfig(traning_pipeline_config=self.training_pipeline_config)
            logging.info("Model Trainer started")
            model_trainer = ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifacts)
            model_trainer_artifacts = model_trainer.initiate_model_trainer()
            logging.info("Model Trainer completed")
            return model_trainer_artifacts
        except Exception as e:
            logging.error(f"Error occured in start_model_trainer class {str(e)}")
            raise NetworkSecurityException(e, sys)
        
    def run_pipeline(self):
        try:
            data_ingestion_artifacts = self.start_data_ingestion()
            data_validation_artifacts = self.start_data_validation(data_ingestion_artifacts=data_ingestion_artifacts)
            data_transformation_artifacts = self.start_data_transformation(data_validation_artifacts=data_validation_artifacts)
            model_trainer_artifacts = self.start_model_trainer(data_transformation_artifacts=data_transformation_artifacts)
            return model_trainer_artifacts
        except Exception as e:
            logging.error(f"Error occured in run_pipeline class {str(e)}")
            raise NetworkSecurityException(e, sys)