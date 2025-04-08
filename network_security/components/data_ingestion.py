from network_security.exception.exception import NetworkSecurityException
from network_security.logging import logger
from network_security.entity.config_entity import DataIngestionConfig
import os 
import sys
import numpy as np
import pandas as pd
from typing import List
from sklearn.model_selection import train_test_split
from pymongo import MongoClient
from dotenv import load_dotenv
from network_security.entity.artifact_entity import DataIngestionArtifact

load_dotenv()
Mongo_client_url = os.getenv("MONGOCLIENT_URL")

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            logger.logging.error("Error occured in DataIngestion class", e)
            raise NetworkSecurityException(e, sys)
        

    def export_collection_as_dataframe(self):
        """Read data from mongoDB and return as dataframe"""
        try:
            logger.logging.info("Enter in export_collection_as_dataframe class")
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.client = MongoClient(Mongo_client_url)
            collection = self.client[database_name][collection_name]
            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df = df.drop("_id",axis=1)

            df.replace({"na":np.nan},inplace=True)
            return df
        except Exception as e:
            logger.logging.error("Error occured in export_collection_as_dataframe class", e)
            raise NetworkSecurityException(e, sys)
        
    
    def export_data_into_feature_store(self,data_frame: pd.DataFrame):
        try:
            logger.logging.info("Enter in export_data_into_feature_store class")
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            data_frame.to_csv(feature_store_file_path,index=False,header=True)
            return data_frame
        except Exception as e:
            logger.logging.error("Error occured in export_data_into_feature_store class", e)
            raise NetworkSecurityException(e, sys)

    def split_data_as_train_test(self,data_frame: pd.DataFrame):
        try:
            logger.logging.info("Enter in split_data_as_train_test class")
            train_set, test_set = train_test_split(data_frame, test_size=self.data_ingestion_config.train_test_split_ratio)
            logger.logging.info("Successfully split data into train and test")
            dir_name = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_name,exist_ok=True)
            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path,index=False,header=True)
            logger.logging.info("Successfully split data into train and test")
            return train_set,test_set
        except Exception as e:
            logger.logging.error("Error occured in split_data_as_train_test class", e)
            raise NetworkSecurityException(e, sys)

    def initiate_data_ingestion(self):
        try:
            logger.logging.info("Enter in initiate_data_ingestion class")
            data_frame = self.export_collection_as_dataframe()
            data_frame = self.export_data_into_feature_store(data_frame)
            train_set,test_set = self.split_data_as_train_test(data_frame)
            data_ingestion_artifact = DataIngestionArtifact(
                training_file_path=self.data_ingestion_config.training_file_path,
                testing_file_path= self.data_ingestion_config.testing_file_path
            )
            return data_ingestion_artifact
        except Exception as e:
            logger.logging.error("Error occured in initiate_data_ingestion class", e)
            raise NetworkSecurityException(e, sys)

