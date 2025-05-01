from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import numpy as np
import pandas as pd
import pickle
from fastapi.staticfiles import StaticFiles
import os
from fastapi.responses import JSONResponse

from fastapi import File, UploadFile
from tensorflow.keras.models import load_model
import cv2
import io
from PIL import Image


app = FastAPI()


# Load model and data
df = pd.read_csv(r"C:\Heliware\fastAPI\medical\data\diabetes_prediction_dataset (2).csv")
loaded_model = pickle.load(open('trained_model.sav', 'rb'))
pneumonia_model = load_model("pneumonia.h5")

templates = Jinja2Templates(directory="templates")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

def diabetes_prediction(input_data):
    input_data_as_numpy_array = np.asarray(input_data)
    input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)
    prediction = loaded_model.predict(input_data_reshaped)

    if prediction[0] == 0:
        return 'You may not have diabetes.'
    else:
        return 'You may have diabetes.'

def pneumonia_prediction(file: UploadFile):
    contents = file.file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    image = image.resize((224, 224))  # Here i m using (224, 224) 
    image = np.array(image).astype("float32") / 255.0
    image = np.expand_dims(image, axis=0)

    prediction = pneumonia_model.predict(image)[0][0]

    if prediction > 0.5:
        return "PNEUMONIA Detected"
    else:
        return "NORMAL (No Pneumonia)"



@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/predict_diabetes", response_class=HTMLResponse)
def predict_form(request: Request):
    return templates.TemplateResponse("diabetes.html", {"request": request})


@app.post("/predict_diabetes", response_class=HTMLResponse)
async def predict(request: Request,
    gender: int = Form(...),
    age: float = Form(...),
    hypertension: int = Form(...),
    heart_disease: int = Form(...),
    smoking_history: int = Form(...),
    bmi: float = Form(...),
    HbA1c_level: float = Form(...),
    blood_glucose_level: int = Form(...)
):
    input_data = [gender, age, hypertension, heart_disease, smoking_history, bmi, HbA1c_level, blood_glucose_level]
    result = diabetes_prediction(input_data)
    #return templates.TemplateResponse("result.html", {"request": request, "result": result})
    return JSONResponse(content={"result": result})


@app.get("/predict_pneumonia", response_class=HTMLResponse)
def predict_form(request: Request):
    return templates.TemplateResponse("pneumonia.html", {"request": request})

@app.post("/predict_pneumonia")
async def predict_pneumonia(request: Request, file: UploadFile = File(...)):
    result = pneumonia_prediction(file)
    return JSONResponse(content={"result": result})


