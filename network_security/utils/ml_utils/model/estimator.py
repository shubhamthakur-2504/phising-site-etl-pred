from network_security.constants.training_pipelline import MODEL_FILE_NAME, SAVED_MODEL_DIR
from network_security.logging.logger import logging
from network_security.exception.exception import NetworkSecurityException
import os
import sys

class NetworkSecurityModel:
    def __init__(self, model, preprocessor):
        try:
            self.model = model
            self.preprocessor = preprocessor
        except Exception as e:
            logging.error(f"Error occured in NetworkSecurityModel class constructor {str(e)}")
            raise NetworkSecurityException(e, sys)
        
    def predict(self, x):
        try:
            x_transformed = self.preprocessor.transform(x)
            y_hat = self.model.predict(x_transformed)
            return y_hat
        except Exception as e:
            logging.error(f"Error occured in NetworkSecurityModel class constructor {str(e)}")
            raise NetworkSecurityException(e, sys)