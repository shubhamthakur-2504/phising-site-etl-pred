import os
import sys
import pymongo
import certifi
from dotenv import load_dotenv


from network_security.logging.logger import logging
from network_security.utils.utils import load_object
from network_security.exception.exception import NetworkSecurityException
from network_security.pipelines.training_pipeline import TrainingPipeline
from network_security.constants.training_pipelline import DATA_INGESTION_DATABASE_NAME, DATA_INGESTION_COLLECTION_NAME


from fastapi import FastAPI,File,UploadFile,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from uvicorn import run as app_run
from starlette.responses import RedirectResponse


ca = certifi.where()
load_dotenv()
mongo_client_url = os.getenv("MONGOCLIENT_URL")
client = pymongo.MongoClient(mongo_client_url, tlsCAFile=ca)

database = client[DATA_INGESTION_DATABASE_NAME]
collection = client[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train", tags=["training"])
async def train():
    try:
        training_pipeline = TrainingPipeline()
        training_pipeline.run_pipeline()
        return Response("Training successful !!")
    except Exception as e:
        logging.error(f"Error occured in train route {str(e)}")
        raise NetworkSecurityException(e, sys)

if __name__ == "__main__":
    app_run(app, host="0.0.0.0", port=8000)