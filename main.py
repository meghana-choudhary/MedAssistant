from fastapi import FastAPI, Request, Form, UploadFile, File, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import uvicorn

from utils.diabetic import diabetes_prediction
from utils.pneumonia import pneumonia_prediction
from utils.retinopathy import retinopathy_prediction
from utils.chatbot import get_chatbot_response

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/predict_diabetes", response_class=HTMLResponse)
def predict_diabetes_form(request: Request):
    return templates.TemplateResponse("diabetes.html", {"request": request})

@app.post("/predict_diabetes", response_class=JSONResponse)
async def predict_diabetes(
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
    return JSONResponse(content={"result": result})

@app.get("/predict_pneumonia", response_class=HTMLResponse)
def predict_pneumonia_form(request: Request):
    return templates.TemplateResponse("pneumonia.html", {"request": request})

@app.post("/predict_pneumonia", response_class=JSONResponse)
async def predict_pneumonia(file: UploadFile = File(...)):
    result = pneumonia_prediction(file)
    return JSONResponse(content={"result": result})

@app.get("/predict_retinal", response_class=HTMLResponse)
def predict_retinopathy_form(request: Request):
    return templates.TemplateResponse("retinopathy.html", {"request": request})

@app.post("/predict_retinal", response_class=JSONResponse)
async def predict_retinopathy(file: UploadFile = File(...)):
    result = retinopathy_prediction(file)
    return JSONResponse(content={"result": result})

@app.get("/chatbot", response_class=HTMLResponse)
async def get_chat(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "user_message": None, "bot_response": None})

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        response = get_chatbot_response(request.message)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)








 