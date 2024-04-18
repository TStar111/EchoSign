import torch
import time
from win32com.client import Dispatch

from utils import bytes_to_floats, initialize_bt
from NN.models_NN import SimpleNN, SimpleNN2

# Empty storage (aka Global variables)
start_time = None
end_time = None
class_tracker = [None, None]

# number_to_alphabet[26] = " "
num_to_word = {0: "what",   1: "time",
               2: "car",    3: "church",
               4: "family", 5: "meet",
               6: "live",   7: "big",
               8: "more",   9: "but",
               10: " "}

# Model parameters
# Make sure to adjust this to reflect your choice of single/double, or model
input_dim = 28 * 5
hidden_dim = 64
output_dim = 11
checkpoint_path = 'models/double_word/rs_word_time.pt'

# Calibration storage
minFlex1 = [float('inf')] * 5
maxFlex1 = [-float('inf')] * 5
minFlex2 = [float('inf')] * 5
maxFlex2 = [-float('inf')] * 5

# Hyperparameters
consecutive = 8

# ARDUINO Bluetooth information
CHARACTERISTIC_UUID1 = "19B10001-E8F2-537E-4F6C-D104768A1214"
address1 = "02:81:b7:4b:04:26" # MAC addres of the remove ble device
CHARACTERISTIC_UUID2 = "19b10000-e8f2-537e-4f6c-d104768a1214"
address2= "84:f5:9a:b9:e4:13"

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

# Function that will handle reading data and adding to queue
def readin_data(peripheral1, suuid1, cuuid1, peripheral2, suuid2, cuuid2, buffer, minFlex1, maxFlex1, minFlex2, maxFlex2):
    contents1 = bytes_to_floats(peripheral1.read(suuid1, cuuid1))
    contents2 = bytes_to_floats(peripheral2.read(suuid2, cuuid2))

    for i in range(5):
                contents1[i] = (contents1[i] - minFlex1[i])/(maxFlex1[i] - minFlex1[i])
                contents2[i] = (contents2[i] - minFlex2[i])/(maxFlex2[i] - minFlex2[i])

    # Handles the queueing
    buffer = buffer[14:] + contents1 + contents2

    return buffer


if __name__ == "__main__":
    peripheral1, service_uuid1, characteristic_uuid1 = initialize_bt(mac=address2, uuid=CHARACTERISTIC_UUID2)
    peripheral2, service_uuid2, characteristic_uuid2 = initialize_bt(mac=address1, uuid=CHARACTERISTIC_UUID1)

    # Initialize model with saved weights
    model = SimpleNN2(input_dim, hidden_dim, output_dim)

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

        print("Calibrating for 5 second, please move between max and min flexion")
        time.sleep(5)
        curTime = time.time()
        while time.time() - curTime < 5: # 5 second period of calibration
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

        # Some calibration time to fill the buffer
        buffer = [None] * input_dim

        print("Additional 5 sec to fill buffer")
        curTime = time.time()
        while time.time() - curTime < 5: # 5 second period of calibration
            time.sleep(0.05)
            buffer = readin_data(peripheral1, service_uuid1, characteristic_uuid1,
                                 peripheral2, service_uuid2, characteristic_uuid2,
                                 buffer,
                                 minFlex1, maxFlex1, minFlex2, maxFlex2)

        # Keep reading data
        while True:
            time.sleep(0.05)
            buffer = readin_data(peripheral1, service_uuid1, characteristic_uuid1,
                                 peripheral2, service_uuid2, characteristic_uuid2,
                                 buffer,
                                 minFlex1, maxFlex1, minFlex2, maxFlex2)

            data_array = torch.tensor(buffer)
            probs = model(data_array)
            index = torch.argmax(probs, dim=0).item()
            yhat = num_to_word[index]
                        
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