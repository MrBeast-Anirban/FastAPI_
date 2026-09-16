# Doctor want to see specific patient.

from fastapi import FastAPI, Path, HTTPException
import json

app = FastAPI()

def load_data():
    with open('patients.json') as f:
        data = json.load(f)
    return data 

# app decorator to create a route for the root endpoint. Listening to get rquests.
@app.get("/")
def hello():
    return {'message': "Patient Management System API"}

@app.get("/about")
def about():
    return {'message': "A fully functional API to manage your patients records."}

@app.get("/view")
def view_patients():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve")): # patient_id is str in json file.
    # Path() -> ... means required parameter, description provides information about the parameter
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code = 404, detail = "Patient not found")



# Output -> http://127.0.0.1:8000/patient/P001
"""
{
  "name": "Ananya Verma",
  "city": "Guwahati",
  "age": 28,
  "gender": "female",
  "height": 1.65,
  "weight": 90,
  "bmi": 33.06,
  "verdict": "Obese"
}"""