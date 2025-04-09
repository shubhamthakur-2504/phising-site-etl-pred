import os
import sys
import pandas as pd
import numpy as np



"""  training constants  """

ARTIFACT_DIR = "artifact"
TARGET_COLUMN = "result"
PIPELINE_NAME = "network_security"
FILE_NAME = "phisingData.csv"

TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"




"""  data_ingestion constants  """

DATA_INGESTION_COLLECTION_NAME = "phising_data"
DATA_INGESTION_DATABASE_NAME = "network_security"
DATA_INGESTION_DIR_NAME = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR_NAME = "feature_store"
DATA_INGESTION_INGESTED_DIR_NAME = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION = 0.2

"""  data_validation constants  """

DATA_VALIDATION_DIR_NAME = "data_validation"
DATA_VALIDATION_VALID_DIR_NAME = "validated"
DATA_VALIDATION_INVALID_DIR_NAME = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR_NAME = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME = "report.yaml"


"""  data_transformation constants  """

DATA_TRANSFORMATION_DIR_NAME = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR = "transformed_object"

DATA_TRANSFORMATION_IMPUTER_PARAMS: dict = {
    "missing_values" : np.nan,
    "n_neighbors" : 3,
    "weights" : "uniform"
}

SCHEMA_FILE_PATH = r"data_schema\schema.yaml"