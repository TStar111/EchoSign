import torch
import time
from win32com.client import Dispatch

from utils import bytes_to_floats, initialize_bt
from NN.models_NN import SimpleNN

from datetime import datetime

# Empty storage (aka Global variables)
start_time = None
end_time = None
class_tracker = [None, None]
dict_to_let = {0:"a", 1:"b", 2:"c", 3:"d", 4:"e", 5:"f", 6:"g", 7:"h", 8:"i", 9:"k", 10:" "}

# Model parameters TODO: Adjust for double
input_dim = 14
hidden_dim = 64
output_dim = 11
checkpoint_path = '../models/simpleNN_none1.pt'

flexFloor = 0
flexCeil = 5

minFlex1 = [float('inf')] * 5
maxFlex1 = [-float('inf')] * 5

minFlex2 = [float('inf')] * 5
maxFlex2 = [-float('inf')] * 5

# Hyperparameters
consecutive = 8

# ARDUINO Bluetooth information TODO: Add this, though not sure if needed
CHARACTERISTIC_UUID = "19B10001-E8F2-537E-4F6C-D104768A1214"
address = "02:81:b7:4b:04:26" # MAC addres of the remove ble device

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


if __name__ == "__main__":
    peripheral1, service_uuid1, characteristic_uuid1 = initialize_bt()
    peripheral2, service_uuid2, characteristic_uuid2 = initialize_bt()

    # Initialize model with saved weights
    model = SimpleNN(input_dim, hidden_dim, output_dim)

    # Load the model checkpoint
    checkpoint = torch.load(checkpoint_path, map_location=torch.device('cpu'))  # Change 'cpu' to 'cuda' if you're using GPU

    # Load the model state_dict
    model.load_state_dict(checkpoint)

    # Set the model to evaluation mode
    model.eval()

    # Initialize speaker (for Windows)
    speak = Dispatch("SAPI.SpVoice").Speak

    try:

        # Haptic signal here to signal beginning of calibration
        
        # Calibrate data to map 
        curTime = datetime.now()
        while datetime.now() - curTime < 10: # 10 second period of calibration
            time.sleep(0.05)
            contents1 = bytes_to_floats(peripheral1.read(service_uuid1, characteristic_uuid1))
            contents2 = bytes_to_floats(peripheral2.read(service_uuid2, characteristic_uuid2))
            for i in range(5):
                minFlex1[i] = min(minFlex1[i], contents1[i])
                minFlex2[i] = min(minFlex2[i], contents2[i])
                maxFlex1[i] = max(maxFlex1[i], contents1[i])
                maxFlex2[i] = max(maxFlex2[i], contents2[i])


        # Haptic signal here to signal end of calibration

        # Keep reading data
        while True:
            time.sleep(0.05)
            contents1 = bytes_to_floats(peripheral1.read(service_uuid1, characteristic_uuid1))
            contents2 = bytes_to_floats(peripheral2.read(service_uuid2, characteristic_uuid2))

            for i in range(5):
                contents1[i] = 5 * contents1[i]/(maxFlex1[i] - minFlex1[i])
                contents2[i] = 5 * contents2[i]/(maxFlex2[i] - minFlex2[i])

            content = contents1 + contents2
            data_array = torch.tensor(content)
            probs = model(data_array)
            index = torch.argmax(probs, dim=0).item()
            yhat = dict_to_let[index]
                        
            if yhat is not None:
                passed, letter, class_tracker = classification_heuristic(yhat, class_tracker, consecutive)
                if passed:
                    print(letter)
                    print("Elapsed time:", end_time - start_time)
                    speak(letter)


    except KeyboardInterrupt:
        print("KeyboardInterrupt: Stopping inference...")
        peripheral1.disconnect()
        peripheral2.disconnect()
        exit()

# Run command below in scripts folder
# python detect_sign_bt.py
        
# Make sure to select the proper ML model before starting
        
# With consecutive=8, it takes around 0.82