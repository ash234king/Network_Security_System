import sys
import os

import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGO_DB_URL")
print(mongo_db_url)
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd

from networksecurity.utils.main_utils.utils import load_object

from networksecurity.utils.ml_utils.model.estimator import NetworkModel


client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

from networksecurity.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from networksecurity.constant.training_pipeline import DATA_INGESTION_DATABASE_NAME

database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")
from fastapi.staticfiles import StaticFiles
app.mount("/static",StaticFiles(directory="static"),name="static")

@app.get("/", tags=["navigation"])
async def home(request:Request):
    return templates.TemplateResponse("index.html",{"request":request})

@app.get("/train",tags=["training"])
async def train_page(request:Request):
     return templates.TemplateResponse("train.html",{"request":request})

@app.post("/train-model",tags=["training"])
async def train_route():
    try:
        train_pipeline=TrainingPipeline()
        train_pipeline.run_pipeline()
        return RedirectResponse(url="/train",status_code=303)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
@app.get("/predict",tags=["prediction"])
def predict_page(request:Request):
     return templates.TemplateResponse("predict.html",{"request":request})

@app.post("/predict-data",tags=["prediction"])
async def predict_route(request: Request,file: UploadFile = File(...)):
    try:
        if not file.filename.endswith('.csv'):
             return templates.TemplateResponse("predict.html",{"request":request,"error":"Please upload the csv file."})
        df=pd.read_csv(file.file)
        #print(df)
        preprocesor=load_object("final_models/preprocessor.pkl")
        final_model=load_object("final_models/model.pkl")
        network_model = NetworkModel(preprocessor=preprocesor,model=final_model)
        print(df.iloc[0])
        y_pred = network_model.predict(df)
        print(y_pred)
        df['predicted_column'] = y_pred
        print(df['predicted_column'])
        #df['predicted_column'].replace(-1, 0)
        #return df.to_json()
        df.to_csv('prediction_output/output.csv')
        table_html = df.to_html(classes='data-table')
        #print(table_html)
        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})
        
    except Exception as e:
            raise NetworkSecurityException(e,sys)

    
if __name__=="__main__":
    app_run(app,host="0.0.0.0",port=8000)