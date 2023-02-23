from typing import Union
from fastapi import FastAPI, Response, UploadFile, File
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from google.cloud import bigquery
import csv
import codecs
import json
import pandas as pd
from fastapi.responses import JSONResponse
from pydantic import BaseModel


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/file")
async def upload_file(file: UploadFile = File(...)):
    # Do here your stuff with the file
    return {"filename": file.filename}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/data/{getData}")
def read_item(getData: str):
    return {"Data sent": "hello from cancervison team"}

@app.get("/listdataset/")
def read_item():
    data = ["ovarian cancer","lung cancer"]
    getCancerData()
    return {"Data sent": data}

@app.get("/getStats/{datset}")
def read_item(dataset: str):
    data = ""
    if dataset=="tcga":
        data = "tcga"
    return {"Data sent": "tcga"}

@app.get("/login/{data}")
def read_item(summary1: str):
    return {"Data sent": summary1}

@app.get("/getlungcancerdata")
def read_item():
    data = {}
    csvFilePath = r'lungcancerdatasetdemo.csv'
    # Open a csv reader called DictReader
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
        for rows in csvReader:
            key = rows['Case ID']
            data[key] = rows
    return data

@app.get("/getovariancancerdata")
def read_item(info : Request):
    df = pd.read_csv (r'lungcancerdatasetdemo.csv')
    #print(df.to_dict)
    #return df.to_dict()
    #return Response(df.to_dict(orient="records"), media_type="application/json")
    #return df.to_json
    data = {}
    csvFilePath = r'lungcancerdatasetdemo.csv'
    # Open a csv reader called DictReader
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
         
        # Convert each row into a dictionary
        # and add it to data
        for rows in csvReader:
             
            # Assuming a column named 'No' to
            # be the primary key
            key = rows['No']
            data[key] = rows
    #pd.set_option('display.max_rows', None)
    return data

@app.get("/json")
def get_json_data():
    df = pd.DataFrame(
        [["Canada", 10], ["USA", 20]], 
        columns=["team", "points"]
    )
    return df.to_dict(orient="records")

def login_data():
    data="OK"
    return data

def genomics():
    data=[]
    return data

def read_lung_cancer_data():
    df = pd.read_csv (r'lungcancerdatasetdemo.csv')
    # create a dictionary
    data = {}
    csvFilePath = r'lungcancerdatasetdemo.csv'
    # Open a csv reader called DictReader
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
         
        # Convert each row into a dictionary
        # and add it to data
        for rows in csvReader:
             
            # Assuming a column named 'No' to
            # be the primary key
            key = rows['No']
            data[key] = rows
    #pd.set_option('display.max_rows', None)
    return data
    #return Response(df.to_dict(orient="records"))
    #df.to_dict()
    #js=json.load(open('lungcancerdatasetdemo.json'))
    #return json.dumps(df.to_dict())

def read_ovarian_cancer_data():
    df = pd.read_csv (r'lungcancerdataset.csv')
    #pd.set_option('display.max_rows', None)
    data = pd.DataFrame(
        #[["Canada", 10], ["USA", 20]], 
        #columns=df.columns
    )
    #data = df.to_json (r'lungcancerdataset.json')
    #return data.to_dict(orient="records")
    #return df.to_string
    #return Response(df.to_json(orient="records"), media_type="application/json")
    js=json.load(open('lungcancerdataset.json'))
    return json.dumps(js)
          

def getCancerData():
    client = bigquery.Client()
    query_job = client.query(
        """
        SELECT * FROM `solution-kit-11.cancer_cases_dataset.lung_cancer_data` WHERE DATE(_PARTITIONTIME) < '2023-02-22' """
    )
    query_job.result()  # Waits for job to complete.
    destination = query_job.destination
    destination = client.get_table(destination)
    print("The query data:")
    rows = client.list_rows(destination, start_index=0, max_results=20)
    for row in rows:
        print("Case_ID={}, Patient_affiliation={}".format(row["Case_ID"], row["Patient_affiliation"]))
