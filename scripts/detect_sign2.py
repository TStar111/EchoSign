import csv
import time
import argparse
import serial
import torch
import asyncio
import sys
import pyttsx3
from bleak import *

from NN.models_NN import SimpleNN

from utils import bytes_to_floats

# Parameters
input_dim = 14
hidden_dim = 64
output_dim = 11
checkpoint_path = '../models/simpleNN_none1.pt'
consecutive = 8

# BT1
CHARACTERISTIC_UUID1 = "19B10001-E8F2-537E-4F6C-D104768A1214"
address1 = "02:81:b7:4b:04:26" # MAC addres of the remove ble device

# BT2
CHARACTERISTIC_UUID2 = "19B10001-E8F2-537E-4F6C-D104768A1214"
address2 = "02:81:b7:4b:04:26" # MAC addres of the remove ble device

engine = pyttsx3.init()

# Alphabet dictionary
dict_to_num = {chr(i): i - 97 for i in range(97, 107)}
dict_to_let = {0:"a", 1:"b", 2:"c", 3:"d", 4:"e", 5:"f", 6:"g", 7:"h", 8:"i", 9:"k", 10:" "}

# Empty storage (aka Global variables)
start_time = None
end_time = None
class_tracker = [None, None]

# Function that will return [bool, letter, new_tracker]
def classification_heuristic(new_letter, tracker, consecutive):
    global start_time
    global end_time
    curr_letter = tracker[0]
    if new_letter == curr_letter:
        tracker[1] += 1

        if tracker[1] == consecutive:
            tracker = [None, None]
            end_time = time.time()
            return True, curr_letter, tracker
        else:
            return False, None, tracker
    
    else:
        tracker = [new_letter, 1]
        start_time = time.time()
        return False, None, tracker

async def collect_bt(model):
    global class_tracker
    client1 = BleakClient(address1)
    await client1.connect()
    if client1.is_connected():
        print('I\'m connected to the device1 ! ')

    client2 = BleakClient(address2)
    await client2.connect()
    if client2.is_connected():
        print('I\'m connected to the device2 ! ')

    while True:
        time.sleep(0.2)
        value1 = await client1.read_gatt_char(CHARACTERISTIC_UUID1)
        value2 = await client2.read_gatt_char(CHARACTERISTIC_UUID2)
        received_data1 = bytes_to_floats(value1)
        received_data2 = bytes_to_floats(value2)
        received_data = received_data1 + received_data2
        data_array = torch.tensor(received_data)  # Split and convert to int array
        
        # start = time.time()
        probs = model(data_array)
        # end = time.time()
        # print("ML time: ", end-start, "sec")

        # Get the index of the highest value
        index = torch.argmax(probs, dim=0).item()

        yhat = dict_to_let[index]

        passed, letter, class_tracker = classification_heuristic(yhat, class_tracker, consecutive)
        if passed:
            print(letter)
            print("Elapsed time:", end_time - start_time)
            engine.say(letter)
            engine.runAndWait()

def handle_usb_data(model, ser1, ser2):
    if ser1.in_waiting > 0 and ser2.in_waiting > 0:  # Check if there's data available to read
        received_data1 = ser1.readline().decode().strip()
        received_data2 = ser2.readline().decode().strip()
        # print(received_data)
        data_array1 = torch.tensor([float(x) for x in received_data1.split(',')])  # Split and convert to int array
        data_array2 = torch.tensor([float(x) for x in received_data2.split(',')])  # Split and convert to int array
        data_array = data_array1 + data_array2
        
        start = time.time()
        probs = model(data_array)
        end = time.time()
        # print("ML time: ", end-start, "sec")

        # Get the index of the highest value
        index = torch.argmax(probs, dim=0).item()

        yhat = dict_to_let[index]

        ser2.reset_input_buffer()
        ser2.reset_input_buffer()
        return yhat
    else:
        return None

def main(connection_type, device_mac_address):

    # Initialize model with saved weights
    model = SimpleNN(input_dim, hidden_dim, output_dim)

    # Load the model checkpoint
    checkpoint = torch.load(checkpoint_path, map_location=torch.device('cpu'))  # Change 'cpu' to 'cuda' if you're using GPU

    # Load the model state_dict
    model.load_state_dict(checkpoint)

    # Set the model to evaluation mode
    model.eval()

    if connection_type == 'bluetooth':
        try:
            asyncio.run(collect_bt(model))
        except KeyboardInterrupt:
            print("KeyboardInterrupt: Stopping inference...")
            exit()

    elif connection_type == 'usb':
        try:
            # Connect to Arduino via USB
            ser = serial.Serial('COM9', 9600, timeout=1)  # Adjust port and baud rate as needed

            # Keep reading data
            while True:
                time.sleep(0.05)
                yhat = handle_usb_data(model, ser)
                # print(yhat)
                
                global class_tracker
                if yhat is not None:
                    passed, letter, class_tracker = classification_heuristic(yhat, class_tracker, consecutive)
                    if passed:
                        print(letter)
                        print("Elapsed time:", end_time - start_time)
                        engine.say(letter)
                        engine.runAndWait() 

        except serial.SerialException as e:
            print("Serial Error:", e)
            ser.close()  # Close the serial connection before exiting
            print("Serial connection closed.")
            exit()

        except KeyboardInterrupt:
            print("KeyboardInterrupt: Stopping inference...")
            ser.close()  # Close the serial connection before exiting
            print("Serial connection closed.")
            exit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Collect data from Arduino via Bluetooth or USB')
    parser.add_argument('connection_type', choices=['bluetooth', 'usb'], default='usb', help='Type of connection (bluetooth or usb)')
    args = parser.parse_args()

    main(args.connection_type, args.device_mac_address)

# python detect_sign.py usb 
# python detect_sign.py bluetooth
    
# Make sure to change data filepath and label before running