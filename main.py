from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import io
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.efficientnet import preprocess_input

app = FastAPI()

# Define model globally
def load_custom_model():
    base_model = tf.keras.applications.EfficientNetB0(include_top=False, input_shape=(224, 224, 3), pooling='avg')
    x = tf.keras.layers.Dense(256, activation='relu')(base_model.output)
    output = tf.keras.layers.Dense(5, activation='softmax')(x)  # Changed from 10 to 5

    model = tf.keras.Model(inputs=base_model.input, outputs=output)
    model.load_weights("model.weights.h5")
    return model

model = load_custom_model()

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        image = image.resize((224, 224))

        image_array = np.array(image)
        image_array = preprocess_input(image_array)  # EfficientNet preprocessing
        image_array = np.expand_dims(image_array, axis=0)  # Shape: (1, 224, 224, 3)

        prediction = model.predict(image_array)
        predicted_class = int(np.argmax(prediction))

        return {"predicted_class": predicted_class, "raw_output": prediction.tolist()}

    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})



