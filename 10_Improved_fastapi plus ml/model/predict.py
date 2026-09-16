import pickle
import pandas as pd

# import the ml model
with open('model/model.pkl', 'rb') as f:
    model = pickle.load(f)

# comes from mlflow
MODEL_VERSION = '1.0.0'

# Get class labels from the model (important for matching the probabilities of class name)
class_labels = model.classes_.tolist()

def prediction(user_input: dict):
    input_df =pd.DataFrame([user_input])

    # predict the class 
    predicted_class = model.predict(input_df)[0]

    # Get probabilities for each class
    probabilities = model.predict_proba(input_df)[0]
    confidence = max(probabilities) # Get the highest probability as confidence

    # Create mapping: {class_label : probability}
    class_probabilities = dict(zip(class_labels, map(lambda x: round(x, 4), probabilities)))

    return {
        'predicted_category' : predicted_class,
        'confidence' : round(confidence, 4),
        'class_probabilities' : class_probabilities
    }