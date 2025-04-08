from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
import os
import sys
import yaml
import numpy as np
import dill
import pickle

def read_yaml_file(file_path: str) -> dict: 
    try:
        with open(file_path, "rb") as file:
            return yaml.safe_load(file)
    except Exception as e:
        logging.error("Error occured in read_yaml_file function", e)
        raise NetworkSecurityException(e, sys)