from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema.user_input import UserInput
from model.predict import MODEL_VERSION, prediction, model
from schema.prediction_response import PredictionResponse

app = FastAPI()


# adding a home route
@app.get('/')
def home():
    return {'message': "Insurence Premium Prediction API."}

# recommended by cloud service providers like aws --> make machine readable
# add a health - health check route --> to know whether the api is live
@app.get('/health')
def health_check():
    return {
        'status' : 'Ok', 
        'model_version' : MODEL_VERSION,
        'model_loaded' : model is not None
        # any other message can also be added like 'uptime', 'server_time', 'dependencies' etc
        }

@app.post('/predict', response_model = PredictionResponse) # adding response model to validate api output
def predict_premium(data: UserInput):

    user_input = {
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }

    # handle if the model is not loaded or any other error occurs during prediction
    try : 
        output = prediction(user_input)
        return JSONResponse(status_code=200, content={'response': output})
    except Exception as e:
        return JSONResponse(status_code = 500, content = {'error' : str(e)})
    




