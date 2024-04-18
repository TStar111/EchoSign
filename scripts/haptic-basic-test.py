#!/usr/bin/env python3

# structured based on detect_sign_bt_2.py


import time


from utils import initialize_bt


# Empty storage (aka Global variables)
start_time = None
end_time = None

# ARDUINO Bluetooth information
CHARACTERISTIC_UUID1 = "19B10001-E8F2-537E-4F6C-D104768A1214"
address1 = "02:81:b7:4b:04:26" # MAC address of the remove ble device
CHARACTERISTIC_UUID2 = "19b10000-e8f2-537e-4f6c-d104768a1214"
address2= "84:f5:9a:b9:e4:13"



if __name__ == "__main__":
    peripheral1, service_uuid1, characteristic_uuid1 = initialize_bt(mac=address2, uuid=CHARACTERISTIC_UUID2)
    # peripheral2, service_uuid2, characteristic_uuid2 = initialize_bt(mac=address1, uuid=CHARACTERISTIC_UUID1)

    try:

        # Haptic signal here to signal beginning of calibration
        # Example condition to trigger the motor
        start_calibrating = True  # Replace with your actual condition
        
        if start_calibrating:
            print("(BT to Arduino) Sending calibration start haptic signal...")
            peripheral1.write(service_uuid, characteristic_uuid, bytearray([1]))  # Send signal to glove 1 Arduino to trigger motors
            time.sleep(1)  # Delay to ensure the motor is activated
         

        print("Calibrating for 5 second, please move between max and min flexion")
        curTime = time.time()
        while time.time() - curTime < 5: # 10 second period of calibration
            time.sleep(0.05)
            # haptic won't send anything back so we just wait 

        
        input("Press enter to start inference (don't actually, this is just a test)")


        # Haptic signal here to signal end of calibration
        # Example condition to trigger the motor
        end_calibrating = True  # Replace with your actual condition

        if end_calibrating:
            print("(BT to Arduino) Sending calibration end haptic signal...")
            peripheral1.write(service_uuid, characteristic_uuid, bytearray([1]))  # Send signal to Arduino to trigger motor
            time.sleep(1)  # Delay to ensure the motor is activated

          


    except KeyboardInterrupt:
        print("KeyboardInterrupt: Stopping inference...")
        peripheral1.disconnect()
        # peripheral2.disconnect()
        exit()

# Run command below in scripts folder
# python haptic_basic_test.py
        