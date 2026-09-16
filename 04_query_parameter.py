# Endpoint to sort patients by height, weight, bmi. This endpoint will accept a query parameter 'order' which can be either 'asc' or 'desc'.

from fastapi import FastAPI, Path, HTTPException, Query
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



@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description = "Sort on the basis of height, weight or bmi"), order: str = Query('asc', description = "Sort in ascending or descending order")):
    # sort_by is required parameter, order is optional parameter with default value 'asc'
    valid_fields = ['height', 'weight', 'bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code = 400, detail = "Invalid Fields, select from {valid_fields}")
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code = 400, detail = "Invalid order, select from ['asc', 'desc']")
    
    data = load_data()

    sort_order = True if order == 'desc' else False
    
    sorted_data = sorted(data.items(), key = lambda x: x[1].get(sort_by, 0), reverse = sort_order)
    # reverse = True means descending order, reverse = False means ascending order
    return (dict(sorted_data))





# output -> http://127.0.0.1:8000/sort?sort_by=weight&order=asc
"""
{
  "P003": {
    "name": "Sneha Kulkarni",
    "city": "Pune",
    "age": 22,
    "gender": "female",
    "height": 1.6,
    "weight": 45,
    "bmi": 17.58,
    "verdict": "Underweight"
  },
  "P005": {
    "name": "Neha Sinha",
    "city": "Kolkata",
    "age": 30,
    "gender": "female",
    "height": 1.55,
    "weight": 75,
    "bmi": 31.22,
    "verdict": "Obese"
  },
  "P002": {
    "name": "Ravi Mehta",
    "city": "Mumbai",
    "age": 35,
    "gender": "male",
    "height": 1.75,
    "weight": 85,
    "bmi": 27.76,
    "verdict": "Overweight"
  },
  "P001": {
    "name": "Ananya Verma",
    "city": "Guwahati",
    "age": 28,
    "gender": "female",
    "height": 1.65,
    "weight": 90,
    "bmi": 33.06,
    "verdict": "Obese"
  },
  "P004": {
    "name": "Arjun Verma",
    "city": "Mumbai",
    "age": 40,
    "gender": "male",
    "height": 1.8,
    "weight": 90,
    "bmi": 27.78,
    "verdict": "Normal"
  }
}
"""