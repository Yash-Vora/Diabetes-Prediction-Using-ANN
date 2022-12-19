# Required Libraries
from flask import Flask, render_template, request
from tensorflow.python.keras.models import load_model
from sklearn.pipeline import Pipeline
import pickle
import numpy as np
import pickle


# Threshold value for Binary Classification
threshold = 0.5

# Initializing app
app = Flask(__name__)

# Load Model
model = load_model('diabetes.h5')

# Load scaler object
with open('scaler.pkl', 'rb') as file:
    sc = pickle.load(file)
    
# Creating Pipeline
diabetes_pipeline = Pipeline(steps=[
    ('scaling', sc),
    ('model', model)
])

# Method that will predict whether person have diabetes or not
def diabetes(input_):  # input_ = [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]
    # convert to a numpy array
    input_arr = np.array(input_)
    # change shape from (8,) to (1,8)
    input_arr = np.expand_dims(input_arr, 0)
    # Diabetes Prediction
    prediction = 'Diabetic' if (diabetes_pipeline.predict(input_arr)[0,0] > threshold) else 'Non-Diabetic'
    
    return f'You are {prediction}'


# This route will return predicted calories
@app.route("/", methods=['GET', 'POST'])
def diabetes_prediction():
    if request.method == 'POST':
        # Input from user
        input_ = [request.form['Pregnancies'], request.form['Glucose'], request.form['BloodPressure'], request.form['SkinThickness'], 
                    request.form['Insulin'], request.form['BMI'], request.form['DiabetesPedigreeFunction'], request.form['Age']]
        # Diabetes Prediction
        prediction = diabetes(input_)

        return render_template('index.html', prediction = prediction)

    return render_template('index.html')


if __name__ == '__main__':
   app.run()