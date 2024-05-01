import csv
import time
import argparse
import serial
import asyncio
import sys
from bleak import *

from ..inference.utils import bytes_to_floats

# File for data to be written to
filepath = "../../data/data.csv"

# Alphabel dictionary
my_dict = {chr(i): i - 97 for i in range(97, 107)}

# Current label (manual)
label = my_dict["a"]
label = 10

CHARACTERISTIC_UUID = "19B10001-E8F2-537E-4F6C-D104768A1214"
address = "02:81:b7:4b:04:26" # MAC addres of the remove ble device

def handle_usb_data(ser):
    if ser.in_waiting > 0:  # Check if there's data available to read
        received_data = ser.readline().decode().strip()
        data_array = [float(x) for x in received_data.split(',')]  # Split and convert to int array
        write_data(data_array)

def write_data(data):
    with open(filepath, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        data.append(label)
        writer.writerow(data)

async def collect_bt(address):
    client = BleakClient(address)
    await client.connect()
    if client.is_connected():
        print('I\'m connected to the device ! ')

    while True:
        time.sleep(0.2)
        value = await client.read_gatt_char(CHARACTERISTIC_UUID)
        received_data = bytes_to_floats(value)
        write_data(received_data)

def main(connection_type, device_mac_address):
    header = ["Thumb1", "Index1", "Middle1", "Ring1", "Pinky1", "AccelX", "AccelY", "AccelZ",
              "GyroX", "GyroY", "GyroZ", "MagX", "MagY", "MagZ", "Letter"]

    with open(filepath, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)

    if connection_type == 'bluetooth':
        try:
            asyncio.run(collect_bt(device_mac_address))
        except KeyboardInterrupt:
            print("KeyboardInterrupt: Stopping data collection...")
            exit()

    elif connection_type == 'usb':
        try:
            # Connect to Arduino via USB
            ser = serial.Serial('COM9', 9600, timeout=1)  # Adjust port and baud rate as needed

            # Keep reading data
            while True:
                time.sleep(0.1)
                handle_usb_data(ser)

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
    parser.add_argument('device_mac_address', default='INVALID', help='MAC address of the device (default is USB connection)')
    args = parser.parse_args()

    main(args.connection_type, args.device_mac_address)

# python collect_data_manual.py usb INVALID
# python collect_data_manual.py bluetooth 02:81:b7:4b:04:26
    
# Make sure to change data filepath and label before running