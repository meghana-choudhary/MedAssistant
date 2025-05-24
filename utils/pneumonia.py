from fastapi import UploadFile
import numpy as np
from PIL import Image
import io
import onnxruntime as ort


session = ort.InferenceSession("models/pneumonia_model.onnx")
input_name = session.get_inputs()[0].name

def pneumonia_prediction(file: UploadFile):
    contents = file.file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    image = image.resize((224, 224))
    image = np.array(image).astype("float32") / 255.0
    image = np.expand_dims(image, axis=0)

    output = session.run(None, {input_name: image})[0]
    prediction = output[0][0]

    if prediction > 0.5:
        return "PNEUMONIA Detected"
    else:
        return "NORMAL (No Pneumonia)"







