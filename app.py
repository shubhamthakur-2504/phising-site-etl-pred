import os
import sys
import pymongo
import certifi
import pandas as pd
from dotenv import load_dotenv


from network_security.logging.logger import logging
from network_security.utils.utils import load_object
from network_security.exception.exception import NetworkSecurityException
from network_security.pipelines.training_pipeline import TrainingPipeline
from network_security.utils.ml_utils.model.estimator import NetworkSecurityModel
from network_security.constants.training_pipelline import DATA_INGESTION_DATABASE_NAME, DATA_INGESTION_COLLECTION_NAME


from fastapi import FastAPI,File,UploadFile,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates

from uvicorn import run as app_run
from starlette.responses import RedirectResponse


ca = certifi.where()
load_dotenv()
mongo_client_url = os.getenv("MONGOCLIENT_URL")
client = pymongo.MongoClient(mongo_client_url, tlsCAFile=ca)
templates = Jinja2Templates(directory="templates")

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
    
@app.post("/predict")
async def predict(request: Request, file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        preprocessor = load_object(file_path=r"final_model/preprocessor.pkl")
        model = load_object(file_path=r"final_model/model.pkl")
        network_security_model = NetworkSecurityModel(model=model, preprocessor=preprocessor)
        y_hat = network_security_model.predict(df)
        df["predicted_column"] = y_hat
        df.to_csv(r"prediction_output/predicted.csv", index=False)
        table_html = df.to_html(classes= "table table-striped")
        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})
    except Exception as e:
        logging.error(f"Error occured in predict route {str(e)}")
        raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    app_run(app, host="0.0.0.0", port=8000)