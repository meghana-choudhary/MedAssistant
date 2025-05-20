from fastapi import UploadFile
import numpy as np
import keras
from PIL import Image
import io

retinopathy_model= keras.saving.load_model("models/retinal_model.keras")

def retinopathy_prediction(file: UploadFile):
    contents = file.file.read()
    image = Image.open(io.BytesIO(contents))
    image = image.resize((224, 224))
    image = np.array(image)
    image = np.expand_dims(image, axis=0)
    image= image / 255.0
    # img_array = image.img_to_array(image)
    # img_array = tf.expand_dims(img_array, 0)  
    # img_array = img_array / 255.0

    prediction = retinopathy_model.predict(image)[0][0]
    print(prediction)

    if prediction >= 0.2:
        return "Normal (No DR)"
    else:
        return "Diabetic Retinopathy Detected"





