# Add a new patient to the database

from pydantic import BaseModel, Field, computed_field
from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
import json
from typing import Annotated, Literal

app = FastAPI()

# load json file (database)
def load_data():
    with open('patients.json') as f:
        data = json.load(f)
    return data 

# save json file (database)
def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)
    return data

# step 1: create pydantic model / schema
class Patient(BaseModel):
    id : Annotated[str, Field(..., description = "ID of the patient", example = ['P001'])]
    name : Annotated[str, Field(..., description = "name of the parient")]
    city : Annotated[str, Field(..., description = "city where patient live")]
    age : Annotated[int, Field(..., gt = 0, lt = 120, description = "Age of the patient")]
    gender : Annotated[Literal['male', 'female', 'others'], Field(..., description = "Gender of the patient")]
    height : Annotated[float, Field(..., gt = 0, description = "Height of the patients in meters")]
    weight : Annotated[float, Field(..., gt = 0, description = "Weight of the patient in kgs")]

    # computed fields
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2), 2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'underweight'
        elif self.bmi < 25:
            return 'normal'
        elif self.bmi < 30:
            return 'overweight'
        else:
            return 'obese'
        
# step 2 : design endpoint
@app.post('/create')
def create_patients(patient : Patient):
    # step1: load existing data
    data = load_data()

    # step2: check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code = 400, detail = "Patient already exists")
    
    # step3: add new patient to the database
    data[patient.id] = patient.model_dump(exclude = ['id']) # convert to dictionary

    # step4: save the updated json file
    save_data(data)

    # step5: return json response
    return JSONResponse(status_code = 201, content = {'message': 'patient created successfully.'})



# Result 
# goto -> http://127.0.0.1:8000/docs
# tryout some new data