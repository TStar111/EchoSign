import serial
import pandas as pd
from time import sleep
from sklearn.preprocessing import OneHotEncoder

# from models import ML model 

# Setup serial connection
ser = serial.Serial('/dev/tty.usbmodemXXXX', 9600)
sleep(2)  # Wait for connection

# Initialize one-hot encoder???
encoder = OneHotEncoder(sparse=False)

# Initialize ML model 
# model = MLmodel()

def preprocess_data(csv_string):
    # Assume data comes in as CSV string
    data = pd.DataFrame([csv_string.split(',')], columns=['Timestamp', 'IMU', 'FlexSensors'])

    # One-hot encoding 
    encoded_data = encoder.fit_transform(data[['IMU', 'FlexSensor']])

    return encoded_data

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        processed_data = preprocess_data(line)
        
        # Predict using ML model
        # prediction = model.predict(processed_data)
        
        # Send message to glove if classified gesture
        # ser.write(str(prediction).encode())
        
        print(processed_data)
