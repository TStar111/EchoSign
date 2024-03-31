import csv
import time

from ..utils import bytes_to_floats, initialize_bt

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

def write_data(data):
    with open(filepath, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        data.append(label)
        writer.writerow(data)

if __name__ == "__main__":
    header = ["Thumb1", "Index1", "Middle1", "Ring1", "Pinky1", "AccelX", "AccelY", "AccelZ",
              "GyroX", "GyroY", "GyroZ", "MagX", "MagY", "MagZ", 
              "Thumb2", "Index2", "Middle2", "Ring2", "Pinky2", "AccelX2", "AccelY2", "AccelZ2",
              "GyroX2", "GyroY2", "GyroZ2", "MagX2", "MagY2", "MagZ2", "Letter"]

    with open(filepath, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)

    peripheral1, service_uuid1, characteristic_uuid1 = initialize_bt()
    peripheral2, service_uuid2, characteristic_uuid2 = initialize_bt()

    try:
        # Keep reading data
        while True:
            time.sleep(0.05)
            contents1 = bytes_to_floats(peripheral1.read(service_uuid1, characteristic_uuid1))
            contents2 = bytes_to_floats(peripheral2.read(service_uuid2, characteristic_uuid2))
            content = contents1 + contents2
            write_data(content)


    except KeyboardInterrupt:
        print("KeyboardInterrupt: Stopping inference...")
        peripheral1.disconnect()
        peripheral2.disconnect()
        exit()

# Run command below in scripts folder
# python collect_data_manual_bt2.py
        
# Make sure to adjust label and output file before running