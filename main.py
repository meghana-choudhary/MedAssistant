from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
import numpy as np
import pandas as pd
import pickle
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from fastapi import File, UploadFile
from tensorflow.keras.models import load_model
import cv2
import io
import os
from PIL import Image

app = FastAPI()

load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')


class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str


# Load model and data
df = pd.read_csv("data/diabetes_prediction_dataset (2).csv")
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

@app.get("/chatbot", response_class=HTMLResponse)
async def get_chat(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "user_message": None, "bot_response": None})


# Define the medical prompt template
medical_prompt = PromptTemplate(
    input_variables=["query"],
    template="""
    You are Ema, an advanced AI medical assistant.
    Your goal is to provide clear, factual, and concise answers to medical queries.
    Always maintain a professional yet friendly tone.

    Guidelines:
    - If unsure, acknowledge uncertainty and recommend consulting a healthcare provider
    - Focus on general medical information and avoid specific diagnoses
    - Provide sources when discussing medical facts
    - Break down complex medical terms
    - Use bullet points for lists
    - Format important information in **bold**

    User Query: {query}

    Response:
    """
)

# Initialize the LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-preview-04-17",
    temperature=0.2,
    convert_system_message_to_human=True,
    google_api_key=api_key
)

# Create the chain
chain = LLMChain(llm=llm, prompt=medical_prompt)

# Keep your existing routes and add this new one
@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        response = chain.run(query=request.message)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


