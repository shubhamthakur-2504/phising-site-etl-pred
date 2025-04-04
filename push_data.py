from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
from network_security.exception.exception import NetworkSecurityException
from network_security.logging import logger
import os
import sys
import certifi
import json
import pandas as pd
import numpy as np

load_dotenv()
client_url = os.getenv("MONGOCLIENT_URL")
ca = certifi.where()

class Network_Data_Extract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def cv_to_json(self,file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(inplace=True,drop=True)
            records =list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def insert_data_mongo(self,records,database,collection):
        try:
            self.records = records
            self.database = database
            self.collection = collection
            self.client = MongoClient(client_url,tlsCAFile=ca)
            self.database = self.client[self.database]
            self.collection = self.database[self.collection]

            self.collection.insert_many(self.records)
            logger.logging.info(f"Data inserted in {database} database {collection} collection successfully in MongoDB length of data {len(self.records)}")
            return f"length of data {len(self.records)}"
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
if __name__ == "__main__":
    File_Path = r"network_data\phisingData.csv"
    Data_Base = "network_security"
    Collection = "phising_data"
    network_obj = Network_Data_Extract()
    records = network_obj.cv_to_json(File_Path)
    records = network_obj.insert_data_mongo(records,Data_Base,Collection)
    print(records)