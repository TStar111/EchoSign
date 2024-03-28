import torch
import time
from win32com.client import Dispatch

from utils import bytes_to_floats, initialize_bt
from NN.models_NN import SimpleNN

# Empty storage (aka Global variables)
start_time = None
end_time = None
class_tracker = [None, None]
dict_to_let = {0:"a", 1:"b", 2:"c", 3:"d", 4:"e", 5:"f", 6:"g", 7:"h", 8:"i", 9:"k", 10:" "}

# Model parameters
input_dim = 14
hidden_dim = 64
output_dim = 11
checkpoint_path = '../models/simpleNN_none1.pt'

# Hyperparameters
consecutive = 8

# ARDUINO Bluetooth information
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
    peripheral, service_uuid, characteristic_uuid = initialize_bt()

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
        # Keep reading data
        while True:
            time.sleep(0.05)
            contents = bytes_to_floats(peripheral.read(service_uuid, characteristic_uuid))
            data_array = torch.tensor(contents)
            print(contents)
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
        peripheral.disconnect()
        exit()

# Run command below in scripts folder
# python detect_sign_bt.py
        
# Make sure to select the proper ML model before starting
        
# With consecutive=8, it takes around 0.82