import csv
import time
import serial

from utils import bytes_to_floats, initialize_bt

# Note for both implementations, the left should always be 1, and the right should always be 2

# File for data to be written to
# Change this to suit your needs
filepath = "data/data_pcb/ricky-none2.csv"

# Current label (manual)
# Change this to suit your needs
label = 10

# Calibration storage
minFlex1 = [float('inf')] * 5
maxFlex1 = [-float('inf')] * 5
minFlex2 = [float('inf')] * 5
maxFlex2 = [-float('inf')] * 5

# Change this to suit your needs
ser1 = serial.Serial('COM9', 9600, timeout=1)  # Adjust port and baud rate as needed
ser2 = serial.Serial('COM13', 9600, timeout=1)  # Adjust port and baud rate as needed

def handle_usb_data(ser1, ser2):
    if ser1.in_waiting > 0 and ser2.in_waiting > 0:  # Check if there's data available to read
        received_data1 = ser1.readline().decode().strip()
        received_data2 = ser2.readline().decode().strip()
        data_array1 = [float(x) for x in received_data1.split(',')]  # Split and convert to int array
        data_array2 = [float(x) for x in received_data2.split(',')]  # Split and convert to int array
        # ser1.reset_input_buffer()
        # ser2.reset_input_buffer()
        return data_array1 + data_array2
    else:
        return None

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

    try:
        # Keep reading data

        print("Calibrating for 5 second, please move between max and min flexion")
        curTime = time.time()
        while time.time() - curTime < 5: # 10 second period of calibration
            time.sleep(0.05)
            contents = handle_usb_data(ser1, ser2)
            if contents is not None:
                for i in range(5):
                    minFlex1[i] = min(minFlex1[i], contents[i])
                    minFlex2[i] = min(minFlex2[i], contents[i+14])
                    maxFlex1[i] = max(maxFlex1[i], contents[i])
                    maxFlex2[i] = max(maxFlex2[i], contents[i+14])
        print(minFlex1)
        print(maxFlex1)
        print(minFlex2)
        print(maxFlex2)
        input("Press enter to start collecting data")

        curTime = time.time()
        # Change the number to collect different number of data (110 ~= 1100 datapoints)
        while time.time() - curTime < 220:
            time.sleep(0.05)
            contents = handle_usb_data(ser1, ser2)
            
            if contents is not None:
                for i in range(5):
                    contents[i] = (contents[i] - minFlex1[i])/(maxFlex1[i] - minFlex1[i])
                    contents[i+14] = (contents[i+14] - minFlex2[i])/(maxFlex2[i] - minFlex2[i])

                write_data(contents)


    except KeyboardInterrupt:
        print("KeyboardInterrupt: Stopping inference...")
        ser1.close()
        ser2.close()
        exit()

# Run command below in scripts folder
# python collect_data_manual_usb2.py
        
# Make sure to adjust label and output file before running

# Steps
# 1. Change the label and filepath before each run
# 2. Plug in both arduinos
# 3. Run the script
# 4. Follow the bluetooth steps. Look for Left and right. ALways connect to the left one first!
# 5. Service UUID is always the nonzero one
# 6. Quickly check to see that the pinouts aare where you expect. Thumb, pointer, middle, ring, pinky