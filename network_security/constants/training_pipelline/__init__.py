import os
import sys
import pandas as pd
import numpy as np



"""

training constants

"""

ARTIFACT_DIR = "artifact"
TARGET_COLUMN = "result"
PIPELINE_NAME = "network_security"
FILENAME = "phisingData.csv"

TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"




"""

data_ingestion constants

"""

DATA_INGESTION_COLLECTION_NAME = "phising_data"
DATA_INGESTION_DATABASE_NAME = "network_security"
DATA_INGESTION_DIR_NAME = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR = "feature_store"
DATA_INGESTION_INGESTED_DIR_NAME = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION = 0.2