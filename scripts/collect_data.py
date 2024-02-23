import csv
import time
from pygatt import BLEDevice, exceptions

# MAC address of the Arduino BLE device
DEVICE_MAC_ADDRESS = '00:00:00:00:00:00'

# File for data to be written to
filepath = "../data/data.csv"

# Current label
label = 0

# Function to handle incoming data and save it to a CSV file
def handle_data(handle, value_bytes):
    # Decode the received data (assuming it's UTF-8 encoded)
    # TODO: Figure out how data is encoded
    # TODO: Figure out how data will be structured
    received_data = value_bytes.decode('utf-8')

    # Write the data along with the label to a CSV file
    with open(filepath, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([received_data, label])

def main():
    try:
        # Connect to the Arduino BLE device
        device = BLEDevice(DEVICE_MAC_ADDRESS)
        device.connect()

        # Subscribe to the characteristic to receive data
        device.subscribe("2A37", callback=handle_data)

        # Keep the program running
        input("Press Enter to stop data collection and exit...")

    except exceptions.BLEError as e:
        print("BLE Error:", e)

    finally:
        if device:
            device.disconnect()

if __name__ == "__main__":
    main()