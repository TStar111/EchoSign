import torch
import time
from win32com.client import Dispatch

import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from utils import bytes_to_floats, initialize_bt
from NN.models_NN import SimpleNN, SimpleNN2

# Empty storage (aka Global variables)
start_time = None
end_time = None
class_tracker = [None, None]

num_to_word1 = {0: "what",  1: "time",
               2: "car",    3: "church",
               4: "family", 5: "meet",
               6: "live",   7: "big",
               8: "more",   9: "but",
               10: " "}
num_to_word2 = {0:"meet",  1:"live",
                2:"big",    3:"more",
                4:"but"}
num_to_word3 = {0: "time", 1: "church"}
bad_words = ["meet", "live", "big", "more", "but"]

# Model parameters
# Make sure to adjust this to reflect your choice of single/double, or model
input_dim = 28
hidden_dim = 128
output_dim = 11
checkpoint_path = 'models/double_pcb/rr_compv3.pt'
checkpoint_path2 = "models/double_pcb/rr_five.pt"
checkpoint_path3 = "models/double_pcb/rr_two.pt"

# Calibration storage
minFlex1 = [float('inf')] * 5
maxFlex1 = [-float('inf')] * 5
minFlex2 = [float('inf')] * 5
maxFlex2 = [-float('inf')] * 5

# Hyperparameters
consecutive = 4

# ARDUINO Bluetooth information (Adjust this for ARDUINO, left=1, right=2)
CHARACTERISTIC_UUID1 = "19b10000-e8f2-537e-4f6c-d104768a1214"
address1 = "02:81:b7:4b:04:26" # MAC addres of the remove ble device
CHARACTERISTIC_UUID2 = "19b10000-e8f2-537e-4f6c-d104768a1214"
address2= "75:4f:4e:83:72:84"

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
    peripheral1, service_uuid1, characteristic_uuid1 = initialize_bt(mac=address1, uuid=CHARACTERISTIC_UUID1)
    peripheral2, service_uuid2, characteristic_uuid2 = initialize_bt(mac=address2, uuid=CHARACTERISTIC_UUID2)

    # Initialize model with saved weights
    model = SimpleNN2(input_dim, hidden_dim, output_dim)
    model2 = SimpleNN2(input_dim, hidden_dim, output_dim-6)
    model3 = SimpleNN2(input_dim, hidden_dim, output_dim-9)

    # Load the model checkpoint
    checkpoint = torch.load(checkpoint_path, map_location=torch.device('cpu'))  # Change 'cpu' to 'cuda' if you're using GPU
    checkpoint2 = torch.load(checkpoint_path2, map_location=torch.device('cpu'))  # Change 'cpu' to 'cuda' if you're using GPU
    checkpoint3 = torch.load(checkpoint_path3, map_location=torch.device('cpu'))  # Change 'cpu' to 'cuda' if you're using GPU

    # Load the model state_dict
    model.load_state_dict(checkpoint)
    model2.load_state_dict(checkpoint2)
    model3.load_state_dict(checkpoint3)

    # Set the model to evaluation mode
    model.eval()
    model2.eval()
    model3.eval()

    # Initialize speaker (for Windows)
    speak = Dispatch("SAPI.SpVoice").Speak

    try:

        # Haptic signal here to signal beginning of calibration
        
        # Calibrate data to map 

        print("Calibrating for 5 second, please move between max and min flexion")
        time.sleep(1)
        curTime = time.time()
        while time.time() - curTime < 4: # 5 second period of calibration
            time.sleep(0.05)
            contents1 = bytes_to_floats(peripheral1.read(service_uuid1, characteristic_uuid1))
            contents2 = bytes_to_floats(peripheral2.read(service_uuid2, characteristic_uuid2))
            for i in range(5):
                minFlex1[i] = min(minFlex1[i], contents1[i])
                minFlex2[i] = min(minFlex2[i], contents2[i])
                maxFlex1[i] = max(maxFlex1[i], contents1[i])
                maxFlex2[i] = max(maxFlex2[i], contents2[i])

        print(minFlex1)
        print(maxFlex1)
        print(minFlex2)
        print(maxFlex2)
        input("Press enter to start inference")


        # Haptic signal here to signal end of calibration

        # Keep reading data
        while True:
            time.sleep(0.05)
            contents1 = bytes_to_floats(peripheral1.read(service_uuid1, characteristic_uuid1))
            contents2 = bytes_to_floats(peripheral2.read(service_uuid2, characteristic_uuid2))
            # print("Left Hand:")
            # print(contents1)
            # print("Right Hand:")
            # print(contents2)

            for i in range(5):
                contents1[i] = (contents1[i] - minFlex1[i])/(maxFlex1[i] - minFlex1[i])
                contents2[i] = (contents2[i] - minFlex2[i])/(maxFlex2[i] - minFlex2[i])

            content = contents1 + contents2
            data_array = torch.tensor(content)
            probs = model(data_array)
            print(probs)
            index = torch.argmax(probs, dim=0).item()
            yhat = num_to_word1[index]

            if yhat in bad_words:
                probs = model2(data_array)
                index = torch.argmax(probs, dim=0).item()
                yhat = num_to_word2[index]

            if yhat in ["time", "church"]:
                probs = model3(data_array)
                index = torch.argmax(probs, dim=0).item()
                yhat = num_to_word3[index]

            if yhat is not None:
                print(yhat)
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
# python detect_sign_bt2.py
        
# Make sure to select the proper ML model before starting
        
# With consecutive=8, it takes around 0.82