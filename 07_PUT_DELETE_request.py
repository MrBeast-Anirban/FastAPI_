# Update a patient on database | Delete a patient from Database

from pydantic import BaseModel, Field, computed_field
from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
import json
from typing import Annotated, Literal, Optional

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

# create pydantic model / schema
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
        
# step1 : create new pydantic model
class PatientUpdate(BaseModel):
    name : Annotated[Optional[str], Field(default = None)]
    city : Annotated[Optional[str], Field(default = None)]
    age : Annotated[Optional[int], Field(default = None, gt = 0)]
    gender : Annotated[Optional[Literal['male', 'female', 'others']], Field(default = None)]
    height : Annotated[Optional[float], Field(default = None, gt = 0)]
    weight : Annotated[Optional[float], Field(default = None, gt = 0)]



# design endpoint
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



# design end point for update
@app.put('/edit/{patient_id}')
def update_patient(patient_id : str, patient_update : PatientUpdate):
    # step 1: load existing data
    data = load_data()
    
    # step 2: check if patient already exist
    if patient_id not in data:
        raise HTTPException(status_code = 404, detail = "Patient Not Found")
    
    # step 3: Extract existing data of patient patient_id
    existing_patient_info = data[patient_id]
    
    # step 4: convert user input to dictionary
    updated_patient_info = patient_update.model_dump(exclude_unset = True) # dictionary with only filled fields

    # step 5: Update the existing patient info dictionary
    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value 

    # Note: But if we change any field like 'weight', the 'bmi' and 'vedict' fields need to be updated too
    #existing_patient_info -> pydantic object -> update bmi + verdict -> pydantic object -> convert to dictionary -> update database
    existing_patient_info['id'] = patient_id # to avoid error as id is a required field in Patient pydantig model
    patient_pydantic_object = Patient(**existing_patient_info)
    existing_patient_info = patient_pydantic_object.model_dump(exclude = 'id')

    # step 6: Update the patient patient_id in database 
    data[patient_id] = existing_patient_info
    save_data(data)

    # return json response
    return JSONResponse(status_code = 200, content = {'message' : 'patient updated'})


# create end point for delete
@app.delete('/delete/{patient_id}')
def delete_patient(patient_id : str):

    # load the data
    data = load_data()

    # check if patient_id exists in data
    if patient_id not in data:
        raise HTTPException(status_code = 404, detail = "Patient not found")

    # if patient is there -> delete the patient patient_id
    del data[patient_id]

    # save data
    save_data(data)

    # return json response
    return JSONResponse(status_code = 200, content = {'message' : "Patient Deleted"})