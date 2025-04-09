from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
import pandas as pd
import numpy as np
import os
import sys
import yaml
import dill
import pickle

def read_yaml_file(file_path: str) -> dict: 
    try:
        with open(file_path, "rb") as file:
            return yaml.safe_load(file)
    except Exception as e:
        logging.error(f"Error occured in read_yaml_file function {str(e)}")
        raise NetworkSecurityException(e, sys)
    

def read_csv_file(file_path: str) -> pd.DataFrame:
    try:
        logging.info("Reading file from path: %s", file_path)
        return pd.read_csv(file_path)
    except Exception as e:
        logging.error(f"Error occured in read_csv_file function {str(e)}")
        raise NetworkSecurityException(e, sys)
    
def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
            
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
        logging.info(f"Yaml file saved at path: {os.path.basename(file_path)}")
    except Exception as e:
        logging.error(f"Error occured in write_yaml_file function {str(e)}")
        raise NetworkSecurityException(e, sys)
    

def save_numpy_array_data(file_path: str, array: np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file:
            np.save(file, array)
        logging.info(f"NumPy array saved at path: {os.path.basename(file_path)}")
    except Exception as e:
        logging.error(f"Error occured in save_numpy_array_data function {str(e)}")
        raise NetworkSecurityException(e, sys)
    

def save_object(file_path: str, obj: object) -> None:
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file:
            pickle.dump(obj, file)
        logging.info(f"Object saved at path: {os.path.basename(file_path)}")
    except Exception as e:
        logging.error(f"Error occured in save_object function {str(e)}")
        raise NetworkSecurityException(e, sys)