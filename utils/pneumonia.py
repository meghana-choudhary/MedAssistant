from fastapi import UploadFile
import numpy as np
import keras
from PIL import Image
import io

pneumonia_model= keras.saving.load_model("models/pneumonia_model.h5")

def pneumonia_prediction(file: UploadFile):
    contents = file.file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    image = image.resize((224, 224))
    image = np.array(image).astype("float32") / 255.0
    image = np.expand_dims(image, axis=0)

    prediction = pneumonia_model.predict(image)[0][0]

    if prediction > 0.5:
        return "PNEUMONIA Detected"
    else:
        return "NORMAL (No Pneumonia)"






