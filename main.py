from fastapi import FastAPI,Path
from pydantic import BaseModel
import json

app = FastAPI(
    title="Team Task Tracker API",
    version="1.0.0",
)
@app.get("/")
def get_me():
    return {"message" :"hello world"}

def load_data():
 with open('patients.json','r') as f:
    data = json.load(f)
    return data;


@app.get('/getalldata')
def get_all_data():
    data = load_data()
    return data


@app.get('/getdata/{patientid}')
def get_myuser(patientid:str = Path(..., description="Patient ID" , example='P001')):
    data = load_data()
    if patientid in data:
        return data[patientid]
    return {"message" :"patient not found"}