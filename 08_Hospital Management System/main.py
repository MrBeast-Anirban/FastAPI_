"""
A Doctor has a database with patients and he wants us to build an API. Through that API he wants to perform following opetations

1. Have a homepage with a text 'Hospital Management System' at '/' -> ✅
2. Have an about page at '/about' -> ✅
3. View the details of all the patients at '/view' -> ✅
4. View any perticular patient detail at '/view/patient_id' -> ✅
5. Sort the patient by height, weight, or bmi and view in ascending or descending order at '/sort' -> ✅
6. Add a new patient to the database at '/create' -> ✅
7. Update any perticular patient in database at '/update/patient_id' -> ✅
7. Delete any patient at '/delete/patient_id' -> ✅

We have the database as a format of json file 
"P001": {
    "name": "Ananya Verma", 
    "city": "Guwahati", 
    "age": 28, 
    "gender": "female", 
    "height": 1.65, 
    "weight": 90.0, 
    "bmi": 33.06, 
    "verdict": "Obese"
}


"""

from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.responses import JSONResponse
import json
from typing import Annotated, Literal, Optional
from pydantic import BaseModel, Field, computed_field

app = FastAPI()

# load data from json file (database)
def load_data():
    with open('patients.json') as f:
        data = json.load(f)
    return data

# save data to json file (database)
def save_data(data):
    with open('patients.json', 'w') as f:
        data = json.dump(data, f)
    return data

# Adding new patient pydantic schema
class Patient(BaseModel):
    id : Annotated[str, Field(..., description = "ID of the patient", examples = ['P001'])]
    name : Annotated[str, Field(..., description = "name of the patient")]
    city : Annotated[str, Field(..., description = "city where patient live")]
    age : Annotated[int, Field(..., gt = 0, lt = 120, description = "Age of the patient")]
    gender : Annotated[Literal['male', 'female', 'others'], Field(..., description = "Gender of the patient")]
    height : Annotated[float, Field(..., gt = 0, description = "Height of the patients in meters")]
    weight : Annotated[float, Field(..., gt = 0, description = "Weight of the patient in kgs")]

    @computed_field
    @property
    def bmi(self) -> float:
        v = round(self.weight/(self.height**2), 2)
        return v

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

# Update operation pydantic schema
class PatientUpdate(BaseModel):
    name : Annotated[Optional[str], Field(default = None)]
    city : Annotated[Optional[str], Field(default = None)]
    age : Annotated[Optional[int], Field(default = None, gt = 0, lt = 120)]
    gender : Annotated[Optional[Literal['male', 'female', 'others']], Field(default = None)]
    height : Annotated[Optional[float], Field(default = None, gt = 0)] 
    weight : Annotated[Optional[float], Field(default = None, gt = 0)]



@app.get('/')
def homepage():
    return {'message' : 'Hospital Managemant System'}

@app.get('/about')
def about():
    return {'message' : 'A fully functional API to manage the patient records.'}

@app.get('/view')
def view_patients():
    data = load_data()
    return data

@app.get('/view/{patient_id}')
def view_patient_id(patient_id: Annotated[str, Path(..., description = "The ID of the patient to retrieve")]):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code = 404, detail = "Patient not found")

@app.get('/sort')
def sort_patients(sort_by : str = Query(..., description = "Sort on the basis of height, weight or bmi"), order : str = Query('asc', description = "Sort in the ascending or descending order.")):
    valid_field = ['height', 'weight', 'bmi']
    if sort_by not in valid_field:
        raise HTTPException(status_code = 400, detail = "Invalid Field, select from {valid_field}")
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code = 400, detail = "Invalid order, select from ['asc', 'desc']")
    
    data = load_data()
    sort_order = False if order == 'asc' else True
    sorted_data = sorted(data.items(), key = lambda x: x[1].get(sort_by, 0), reverse = sort_order)
    return dict(sorted_data)


@app.post('/create')
def create_patient(patient : Patient):
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code = 400, detail = "Patient already exist")
    data[patient.id] = patient.model_dump(exclude = ['id'])
    save_data(data)
    return JSONResponse(status_code = 201, content = {'message': 'patient created successfully.'})

@app.put('/update/{patient_id}')
def update_patient(patient_id: Annotated[str, Path(..., description = "The ID of the patient to update")], patient_update : PatientUpdate):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code = 404, detail = "Patient not found")
    existing_patient_info = data[patient_id]
    updated_patient_info = patient_update.model_dump(exclude_unset = True)
    for key, values in updated_patient_info.items():
        existing_patient_info[key] = values
    existing_patient_info['id'] = patient_id
    patient_pydantic_object = Patient(**existing_patient_info)
    existing_patient_info = patient_pydantic_object.model_dump(exclude = ['id'])
    data[patient_id] = existing_patient_info
    save_data(data)
    return JSONResponse(status_code = 200, content = {'message' : 'patient updated'})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: Annotated[str, Path(..., description = "The ID of the patient to delete")]):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code = 404, detail = "Patient not found")
    del data[patient_id]
    save_data(data)
    return JSONResponse(status_code = 200, content = {'message' : 'patient deleted'})







