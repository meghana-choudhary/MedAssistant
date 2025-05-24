# 🏥 AI-Based Medical Assistant

An intelligent medical assistant built using AI, ML, and DL techniques to aid in early diagnosis and consultation. This system classifies diabetes using a machine learning model, detects pneumonia and diabetic retinopathy from medical images using deep learning, and includes a conversational medical chatbot powered by Gemini 2.5 Flash.

---

## 🚀 Features

### ✅ Disease Detection
- **🩺 Diabetes Classification**  
  Predicts diabetes using patient data via a machine learning model.

- **🫁 Pneumonia Detection**  
  Processes chest X-ray images to detect pneumonia using a convolutional neural network (CNN).

- **👁️ Diabetic Retinopathy Detection**  
  Detects signs of diabetic retinopathy from retinal fundus images using a deep learning model.

### 💬 Medical Chatbot
- **AI-Powered Consultation**  
  Interact with a Gemini 2.5 Flash-powered medical chatbot for general medical queries and explanations.

---

## 🧠 Tech Stack

| Component             | Technology                         |
|-----------------------|-------------------------------------|
| Backend               | FastAPI                            |
| Frontend              | HTML, CSS, JavaScript    |
| ML/DL Libraries       | TensorFlow, Keras, scikit-learn    |
| Image Processing      | Pillow, OpenCV                     |
| Model Inference       | ONNX, ONNX Runtime                 |
| Chatbot               | LangChain + Gemini 2.5 Flash       |
| Environment Management| Conda / Python venv                |
| Deployment            | Render / Local                     |

---

## 🖼️ Model Inputs

- **Diabetes**: Age, BMI, Glucose, Insulin, etc.
- **Pneumonia**: Chest X-ray images (JPEG/PNG)
- **Retinopathy**: Fundus images (JPEG/PNG)

---

## 📦 Setup Instructions

```bash
# 1. Clone the repo
git clone https://github.com/meghana-choudhary/MedAssistant.git
cd medical-assistant

# 2. Create and activate a conda environment
conda create -n medassist python=3.11
conda activate medassist

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python main.py

