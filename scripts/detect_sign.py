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

CHARACTERISTIC_UUID = "19B10001-E8F2-537E-4F6C-D104768A1214"
address = "02:81:b7:4b:04:26" # MAC addres of the remove ble device

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

async def collect_bt(address, model):
    global class_tracker
    client = BleakClient(address)
    await client.connect()
    if client.is_connected():
        print('I\'m connected to the device ! ')

    while True:
        time.sleep(0.2)
        value = await client.read_gatt_char(CHARACTERISTIC_UUID)
        received_data = bytes_to_floats(value)
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

def handle_usb_data(model, ser):
    if ser.in_waiting > 0:  # Check if there's data available to read
        received_data = ser.readline().decode().strip()
        # print(received_data)
        data_array = torch.tensor([float(x) for x in received_data.split(',')])  # Split and convert to int array
        
        start = time.time()
        probs = model(data_array)
        end = time.time()
        # print("ML time: ", end-start, "sec")

        # Get the index of the highest value
        index = torch.argmax(probs, dim=0).item()

        yhat = dict_to_let[index]

        ser.reset_input_buffer()
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
            asyncio.run(collect_bt(device_mac_address, model))
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
    parser.add_argument('device_mac_address', default='INVALID', help='MAC address of the device (default is USB connection)')
    args = parser.parse_args()

    main(args.connection_type, args.device_mac_address)

# python detect_sign.py usb INVALID
# python detect_sign.py bluetooth 02:81:b7:4b:04:26
    
# Make sure to change data filepath and label before running