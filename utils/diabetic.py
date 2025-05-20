import numpy as np
import pickle
import pandas as pd

df = pd.read_csv("data/diabetes_prediction_dataset.csv")
loaded_model = pickle.load(open('models/diabetic_model.sav', 'rb'))

def diabetes_prediction(input_data):
    input_data_as_numpy_array = np.asarray(input_data)
    input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)
    prediction = loaded_model.predict(input_data_reshaped)

    if prediction[0] == 0:
        return 'You may not have diabetes.'
    else:
        return 'You may have diabetes.'




