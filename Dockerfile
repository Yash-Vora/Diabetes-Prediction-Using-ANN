FROM python:3.9
COPY ./Code/diabetes.h5 ./Code/scaler.pkl ./Web_App_Code/app.py ./Dockerfile ./requirements.txt  ./diabetespredictionapp/
COPY ./Web_App_Code/templates ./diabetespredictionapp/templates/
WORKDIR /diabetespredictionapp
RUN pip install -r requirements.txt
EXPOSE 8000
CMD gunicorn --workers 4 --bind 0.0.0.0:8000 app:app