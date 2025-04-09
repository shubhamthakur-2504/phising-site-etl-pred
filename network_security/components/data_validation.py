from network_security.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from network_security.entity.config_entity import DataValidationConfig
from network_security.exception.exception import NetworkSecurityException
from network_security.constants.training_pipelline import SCHEMA_FILE_PATH
from network_security.utils.utils import read_yaml_file, read_csv_file, write_yaml_file
from network_security.logging import logger
from scipy.stats import ks_2samp
import pandas as pd
import os
import sys

class DataValidation:
    def __init__(self, data_validation_config: DataValidationConfig, data_ingestion_artifact: DataIngestionArtifact):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            logger.logging.error(f"Error occured in DataValidation class constructor {str(e)}")
            raise NetworkSecurityException(e, sys)
        
    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            status = len(dataframe.columns) == len(self.schema_config["columns"])
            return status
        except Exception as e:
            logger.logging.error(f"Error occured in validate_number_of_columns function {str(e)}")
            raise NetworkSecurityException(e, sys)
    
    def validate_number_of_numerical_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            status = len(dataframe.select_dtypes(include=["float64", "int64"]).columns) == len(self.schema_config["numerical_columns"])
            return status
        except Exception as e:
            logger.logging.error(f"Error occured in validate_number_of_numerical_columns function {str(e)}")
            raise NetworkSecurityException(e, sys)

    def detect_dataset_drift(self, base_df: pd.DataFrame, current_df: pd.DataFrame, threshold: float = 0.05) -> bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_distribution = ks_2samp(d1, d2)
                if threshold <= is_same_distribution.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update({column: {
                    "p_value": float(is_same_distribution.pvalue),
                    "dirft_status": is_found
                }})
            drift_file_path = self.data_validation_config.drift_report_file_path
            os.makedirs(os.path.dirname(drift_file_path), exist_ok=True)
            write_yaml_file(drift_file_path, report)
            return status
        except Exception as e:
            logger.logging.error(f"Error occured in detect_dataset_drift function {str(e)}")
            raise NetworkSecurityException(e, sys)


    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            logger.logging.info("Enter in initiate_data_validation class")

            train_file_path = self.data_ingestion_artifact.training_file_path
            test_file_path = self.data_ingestion_artifact.testing_file_path

            train_dataframe = read_csv_file(train_file_path)
            test_dataframe = read_csv_file(test_file_path)

            logger.logging.info("Validating train dataframe")
            status = self.validate_number_of_columns(train_dataframe)
            if not status:
                error_message = f"Expected number of columns in train dataframe: {len(self.schema_config['columns'])}. Found {len(train_dataframe.columns)}"
                raise Exception(error_message)

            status = self.validate_number_of_numerical_columns(train_dataframe)
            if not status:
                error_message = f"Expected number of numerical columns in train dataframe: {len(self.schema_config['numerical_columns'])}. Found {len(train_dataframe.select_dtypes(include=['float64', 'int64']).columns)}"
                raise Exception(error_message)
            logger.logging.info("Successfully validated train dataframe ")

            logger.logging.info("Validating test dataframe")
            status = self.validate_number_of_columns(test_dataframe)
            if not status:
                error_message = f"Expected number of columns in test dataframe: {len(self.schema_config['columns'])}. Found {len(test_dataframe.columns)}"
                raise Exception(error_message)

            status = self.validate_number_of_numerical_columns(test_dataframe)
            if not status:
                error_message = f"Expected number of numerical columns in test dataframe: {len(self.schema_config['numerical_columns'])}. Found {len(test_dataframe.select_dtypes(include=['float64', 'int64']).columns)}"
                raise Exception(error_message)
            logger.logging.info("Successfully validated test dataframe")

            logger.logging.info("Detecting dataset drift")
            status = self.detect_dataset_drift(base_df=train_dataframe, current_df=test_dataframe)
            
            if status:
                dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
                os.makedirs(dir_path, exist_ok=True)
                logger.logging.info("Dataset drift not detected")
                logger.logging.info("Saving valid training and testing dataset")
                train_dataframe.to_csv(self.data_validation_config.valid_train_file_path, index=False, header=True)
                test_dataframe.to_csv(self.data_validation_config.valid_test_file_path, index=False, header=True)
                data_validation_artifact = DataValidationArtifact(
                    validation_status=True,
                    valid_train_file_path=self.data_validation_config.valid_train_file_path,
                    valid_test_file_path=self.data_validation_config.valid_test_file_path,
                    invalid_train_file_path=None,
                    invalid_test_file_path=None,
                    drift_report_file_path=self.data_validation_config.drift_report_file_path
                )
            else:
                dir_path = os.path.dirname(self.data_validation_config.invalid_train_file_path)
                os.makedirs(dir_path, exist_ok=True)
                logger.logging.info("Dataset drift detected")
                logger.logging.info("Saving invalid training and testing dataset") 
                train_dataframe.to_csv(self.data_validation_config.invalid_train_file_path, index=False, header=True)
                test_dataframe.to_csv(self.data_validation_config.invalid_test_file_path, index=False, header=True)
                data_validation_artifact = DataValidationArtifact(
                    validation_status=False,
                    valid_train_file_path=None,
                    valid_test_file_path=None,
                    invalid_train_file_path=self.data_validation_config.invalid_train_file_path,
                    invalid_test_file_path=self.data_validation_config.invalid_test_file_path,
                    drift_report_file_path=self.data_validation_config.drift_report_file_path
                )  
            return data_validation_artifact         

            
        except Exception as e:
            logger.logging.error(f"Error occured in initiate_data_validation class {str(e)}")
            raise NetworkSecurityException(e, sys)