import csv
import time
import argparse
from pygatt import BLEDevice, exceptions
import serial

# File for data to be written to
filepath = "../data/data.csv"

# Alphabel dictionary
my_dict = {chr(i): i - 97 for i in range(97, 107)}

# Current label (manual)
label = my_dict["a"]

def handle_ble_data(handle, value_bytes):
    received_data = value_bytes.decode('utf-8')
    write_data(received_data)

def handle_usb_data(ser):
    if ser.in_waiting > 0:  # Check if there's data available to read
        received_data = ser.readline().decode().strip()
        data_array = [float(x) for x in received_data.split(',')]  # Split and convert to int array
        write_data(data_array)

def write_data(data):
    with open(filepath, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data.append(label))

def main(connection_type, device_mac_address):
    header = ["Thumb1", "Index1", "Middle1", "Ring1", "Pinky1", "AccelX", "AccelY", "AccelZ",
              "GyroX", "GyroY", "GyroZ", "MagX", "MagY", "MagZ", "Letter"]

    with open(filepath, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)

    if connection_type == 'bluetooth':
        try:
            # Connect to the Arduino BLE device
            device = BLEDevice(device_mac_address)
            device.connect()

            # Subscribe to the characteristic to receive data
            device.subscribe("2A37", callback=handle_ble_data)

            # Keep the program running
            input("Press Enter to stop data collection and exit...")

        except exceptions.BLEError as e:
            print("BLE Error:", e)
            device.disconnect()  # Disconnect from the BLE device before exiting
            print("BLE device disconnected.")
            exit()

        except KeyboardInterrupt:
            print("KeyboardInterrupt: Stopping data collection...")
            device.disconnect()  # Disconnect from the BLE device before exiting
            print("BLE device disconnected.")
            exit()

        finally:
            if device:
                device.disconnect()

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
            # ser.close()  # Close the serial connection before exiting
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