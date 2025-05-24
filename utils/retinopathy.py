from fastapi import UploadFile
import numpy as np
from PIL import Image
import io
import onnxruntime as ort


session = ort.InferenceSession("models/retinal_model.onnx")
input_name = session.get_inputs()[0].name


def retinopathy_prediction(file: UploadFile):
    contents = file.file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    image = image.resize((224, 224))
    image = np.array(image).astype("float32") / 255.0
    image = np.expand_dims(image, axis=0)

    prediction = session.run(None, {input_name: image})[0][0][0]

    # print(f"Prediction score: {prediction}")

    if prediction >= 0.2:
        return "Normal (No DR)"
    else:
        return "Diabetic Retinopathy Detected"
