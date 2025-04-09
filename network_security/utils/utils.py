from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
import os
import sys
import yaml
import pandas as pd
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
    except Exception as e:
        logging.error(f"Error occured in write_yaml_file function {str(e)}")
        raise NetworkSecurityException(e, sys)