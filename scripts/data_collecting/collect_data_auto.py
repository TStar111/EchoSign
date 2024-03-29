import csv
import time
import argparse
from pygatt import BLEDevice, exceptions
import serial

# File for data to be written to
filepath = "../data/data.csv"

# Current label (manual)
label = 0

def handle_ble_data(handle, value_bytes):
    received_data = value_bytes.decode('utf-8')
    write_data(received_data)

def handle_usb_data(ser):
    received_data = ser.readline().decode().strip()
    write_data(received_data)

def write_data(data):
    with open(filepath, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([data, label])

def main(connection_type, device_mac_address):
    global label
    global filepath
    if connection_type == 'bluetooth':
        try:
            # Connect to the Arduino BLE device
            device = BLEDevice(device_mac_address)
            device.connect()

            # Collect data for each label
            for letter in range(26):
                filepath = f"../data/data_{chr(ord('A') + label)}.csv"

                # Change the global label
                label = letter

                # Prompt to start data collection
                input(f"Collecting data for label '{chr(ord('A') + letter)}'. Press Enter to start...")

                # Subscribe to the characteristic to receive data
                device.subscribe("2A37", callback=handle_ble_data)

                # Prompt to stop data collection
                input(f"Press enter to stop...")

                # Turn off subscription
                device.unsubscribe("2A37")

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
            ser = serial.Serial('/dev/ttyUSB0', 9600)  # Adjust port and baud rate as needed

            # Collect data for each label
            for letter in range(26):
                filepath = f"../data/data_{chr(ord('A') + label)}.csv"

                # Change the global label
                label = letter

                # Prompt to start data collection
                input(f"Collecting data for label '{chr(ord('A') + letter)}'. Press Enter to start...")

                # Start collecting data
                try:
                    while True:
                        handle_usb_data(ser)
                        time.sleep(0.01)  # Adjust as needed
                except KeyboardInterrupt:
                    print("Data collection stopped by user.")
                    continue

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
