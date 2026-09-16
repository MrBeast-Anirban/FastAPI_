from fastapi import FastAPI

app = FastAPI()

# app decorator to create a route for the root endpoint. Listening to get rquests.
@app.get("/")
def hello():
    return {'message': "Hello World"}

# app decorator to create a route for the about endpoint. Listening to get requests.
@app.get("/about")
def about():
    return {'message': "This is a FastAPI application."}