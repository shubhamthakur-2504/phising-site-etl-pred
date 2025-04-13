import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from network_security.constants.training_pipelline import DATA_TRANSFORMATION_IMPUTER_PARAMS, TARGET_COLUMN
from network_security.entity.artifact_entity import DataTransformationArtifact, DataValidationArtifact
from network_security.utils.utils import save_numpy_array_data, save_object, read_data
from network_security.entity.config_entity import DataTransformationConfig
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging


class DataTransformation:
    def __init__(self, data_transformation_config: DataTransformationConfig, data_validation_artifact: DataValidationArtifact):
        try:
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
        except Exception as e:
            logging.error(f"Error occured in DataTransformation class constructor {str(e)}")
            raise NetworkSecurityException(e, sys)
    

    def get_data_transformer_object(self) -> Pipeline: #cls
        logging.info("Enter in get_data_transformer_object function")

        try:
            imputer:KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info("Imputer object created")
            processor = Pipeline(steps=[("imputer", imputer)])
            logging.info("Pipeline created")
            return processor
        except Exception as e:
            logging.error(f"Error occured in get_data_transformer_object function {str(e)}")
            raise NetworkSecurityException(e, sys)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        logging.info("Enter in initiate_data_transformation function")
        try:
            logging.info("Starting data transformation")
            train_df = read_data(file_path=self.data_validation_artifact.valid_train_file_path)
            test_df = read_data(file_path=self.data_validation_artifact.valid_test_file_path)

            # Selecting features and target for train and test dataframe
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1, 0)

            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1, 0)


            logging.info("Getting preprocessor object")
            preprocessor = self.get_data_transformer_object()
            preprocessor_obj = preprocessor.fit(input_feature_train_df)
            logging.info("preprocessor object created")

            logging.info("Transforming train and test data")
            transformed_input_train_arr = preprocessor.transform(input_feature_train_df)
            transformed_input_test_arr = preprocessor.transform(input_feature_test_df)
            logging.info("Data transformation completed")

            logging.info("combining train and test data with target feature")
            train_arr = np.c_[transformed_input_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_arr, np.array(target_feature_test_df)]

            logging.info("Saving preprocessor object")
            save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_file_path, array=train_arr)
            save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_file_path, array=test_arr)
            save_object(file_path=self.data_transformation_config.transformed_object_file_path, obj=preprocessor_obj)
            save_object(file_path=r"final_model/preprocessor.pkl", obj=preprocessor_obj)
            logging.info("Preprocessor object, train and test data array saved")

            logging.info("Creating data transformation artifact")
            data_transformation_artifact =DataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path
            )
            return data_transformation_artifact

        except Exception as e:
            logging.error(f"Error occured in initiate_data_transformation function {str(e)}")
            raise NetworkSecurityException(e, sys)
