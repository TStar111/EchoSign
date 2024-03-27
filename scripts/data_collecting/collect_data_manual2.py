import csv
import time
import argparse
import serial
import asyncio
import sys
from bleak import *

from ..utils import bytes_to_floats

# Note for both implementations, the left should always be 1, and the right should always be 2

# File for data to be written to
filepath = "../../data/data.csv"

# Alphabel dictionary
my_dict = {chr(i): i - 97 for i in range(97, 107)}

# Current label (manual)
label = my_dict["a"]
label = 10

# Stuff for BT1
CHARACTERISTIC_UUID1 = "19B10001-E8F2-537E-4F6C-D104768A1214"
address1 = "02:81:b7:4b:04:26" # MAC addres of the remove ble device
# Stuff for BT2
CHARACTERISTIC_UUID2 = "19B10001-E8F2-537E-4F6C-D104768A1214"
address2 = "02:81:b7:4b:04:26" # MAC addres of the remove ble device

def handle_usb_data(ser1, ser2):
    if ser1.in_waiting > 0 and ser2.in_waiting > 0:  # Check if there's data available to read
        received_data1 = ser1.readline().decode().strip()
        received_data2 = ser2.readline().decode().strip()
        data_array1 = [float(x) for x in received_data1.split(',')]  # Split and convert to int array
        data_array2 = [float(x) for x in received_data2.split(',')]  # Split and convert to int array

        data_array = data_array1 + data_array2
        write_data(data_array)

def write_data(data):
    with open(filepath, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        data.append(label)
        writer.writerow(data)

async def collect_bt(address1, address2):
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
        value1 = await client1.read_gatt_char(CHARACTERISTIC_UUID)
        value2 = await client1.read_gatt_char(CHARACTERISTIC_UUID)
        received_data1 = bytes_to_floats(value1)
        received_data2 = bytes_to_floats(value2)
        received_data = received_data1 + received_data2
        write_data(received_data)

def main(connection_type, device_mac_address):
    header = ["Thumb1", "Index1", "Middle1", "Ring1", "Pinky1", "AccelX", "AccelY", "AccelZ",
              "GyroX", "GyroY", "GyroZ", "MagX", "MagY", "MagZ", 
              "Thumb2", "Index2", "Middle2", "Ring2", "Pinky2", "AccelX2", "AccelY2", "AccelZ2",
              "GyroX2", "GyroY2", "GyroZ2", "MagX2", "MagY2", "MagZ2", "Letter"]

    with open(filepath, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)

    if connection_type == 'bluetooth':
        try:
            asyncio.run(collect_bt(address1, address2))
        except KeyboardInterrupt:
            print("KeyboardInterrupt: Stopping data collection...")
            exit()

    elif connection_type == 'usb':
        try:
            # Connect to Arduino via USB
            ser1 = serial.Serial('COM9', 9600, timeout=1)  # Adjust port and baud rate as needed
            ser2 = serial.Serial('COM8', 9600, timeout=1)  # Adjust port and baud rate as needed

            # Keep reading data
            while True:
                time.sleep(0.1)
                handle_usb_data(ser1, ser2)

        except serial.SerialException as e:
            print("Serial Error:", e)
            ser.close()  # Close the serial connection before exiting
            print("Serial connection closed.")
            exit()

        except KeyboardInterrupt:
            print("KeyboardInterrupt: Stopping data collection...")
            ser.close()  # Close the serial connection before exiting
            print("Serial connection closed.")
            exit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Collect data from Arduino via Bluetooth or USB')
    parser.add_argument('connection_type', choices=['bluetooth', 'usb'], default='usb', help='Type of connection (bluetooth or usb)')
    args = parser.parse_args()

    main(args.connection_type, args.device_mac_address)

# python collect_data_manual.py usb
# python collect_data_manual.py bluetooth
    
# Make sure to change data filepath and label before running