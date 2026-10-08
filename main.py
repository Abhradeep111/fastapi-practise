from fastapi import FastAPI,Path, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated,  Literal
import json

app = FastAPI(
    title="Team Task Tracker API",
    version="1.0.0",
)

class Patient(BaseModel):
   id:Annotated[str,Field(..., description='this is the id' , examples=['P0001'])]
   name:Annotated[str,Field(..., description='ths is name')]
   city:Annotated[str, Field(..., description="this is city")]
   age:Annotated[int , Field(..., gt=0,lt=100, description='thios is age')]
   gender:Annotated[Literal['male','female','others '], Field(..., description='gender of the patient')]
   height: Annotated[float,Field(...,gt=0,description='thios is height')]
   weight: Annotated[float,Field(...,gt=0,description='thios is weight')]


   @computed_field
   @property
   def bmi(self) -> float:
      bmi =round(self.weight/(self.height**2),2)
      return bmi;

   @computed_field
   @property
   def get_verdict(self) -> str:
      if self.bmi < 18:
         return "underweight"
      elif self.bmi <25:
         return "normal"
      else:
         return "overweight" 
      





 










@app.get("/")
def get_me():
    return {"message" :"hello world"}

def load_data():
 with open('patients.json','r') as f:
    data = json.load(f)
    return data;

def write_data(data):
   with open('patients.json','w') as f:
      json.dump(data,f)

       

@app.get('/getalldata')
def get_all_data():
    data = load_data()
    return data


@app.get('/getdata/{patientid}')
def get_myuser(patientid:str = Path(..., description="Patient ID" , examples='P001')):
    data = load_data()
    if patientid in data:
        return data[patientid]
    return {"message" :"patient not found"}


@app.get("/getpatients")
def getpatients(city :str):
   data =load_data();
   result=[]
   for patient in data.values():
      if patient.get('city')==city:
         result.append(patient)

   return result

@app.post("/create")
def create_patient(patient:Patient):
   data=load_data()
   if patient.id in data:
      raise HTTPException(status_code=400, detail="patient already exists")
   else:
     data[patient.id]= patient.model_dump(exclude=["id"])
     write_data(data)
     return JSONResponse(status_code=201, content={'message':'patient created successfully'})
      



   