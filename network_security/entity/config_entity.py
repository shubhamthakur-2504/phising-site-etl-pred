from datetime import datetime
import os
from network_security.constants import training_pipelline
from network_security.exception.exception import NetworkSecurityException
from network_security.logging import logger

logger.logging.info("Enter in config_entity module")


class TrainingPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name: str = training_pipelline.PIPELINE_NAME
        self.artifact_name: str = training_pipelline.ARTIFACT_DIR
        self.artifact_dir: str = os.path.join(self.artifact_name,timestamp)
        self.timestamp: str = timestamp


class DataIngestionConfig:
    def __init__(self,traning_pipeline_config:TrainingPipelineConfig):
        self.data_ingestion_dir: str = os.path.join(traning_pipeline_config.artifact_dir,training_pipelline.DATA_INGESTION_DIR_NAME)
        self.feature_store_file_path: str = os.path.join(self.data_ingestion_dir,training_pipelline.DATA_INGESTION_FEATURE_STORE_DIR_NAME,training_pipelline.FILE_NAME)
        self.training_file_path: str = os.path.join(self.data_ingestion_dir,training_pipelline.DATA_INGESTION_INGESTED_DIR_NAME,training_pipelline.TRAIN_FILE_NAME)
        self.testing_file_path: str = os.path.join(self.data_ingestion_dir,training_pipelline.DATA_INGESTION_INGESTED_DIR_NAME,training_pipelline.TEST_FILE_NAME)
        self.train_test_split_ratio: float = training_pipelline.DATA_INGESTION_TRAIN_TEST_SPLIT
        self.database_name : str = training_pipelline.DATA_INGESTION_DATABASE_NAME
        self.collection_name : str = training_pipelline.DATA_INGESTION_COLLECTION_NAME
