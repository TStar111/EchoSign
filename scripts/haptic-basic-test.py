#!/usr/bin/env python3

# structured based on detect_sign_bt_2.py
# sending bytes only to left hand rn 
import time
import simplepyble


from utils import initialize_bt


# Empty storage (aka Global variables)
start_time = None
end_time = None

# ARDUINO Bluetooth information (Adjust this for ARDUINO, left=1, right=2) new
CHARACTERISTIC_UUID1 = "19b10000-e8f2-537e-4f6c-d104768a1214"
address1 = "75:4f:4e:83:72:84" # MAC addres of the remove ble device
CHARACTERISTIC_UUID2 = "19b10000-e8f2-537e-4f6c-d104768a1214"
address2= "6b:b9:05:ce:25:18"


# # ARDUINO Bluetooth information (old)
# CHARACTERISTIC_UUID1 = "19B10001-E8F2-537E-4F6C-D104768A1214"
# address1 = "02:81:b7:4b:04:26" # MAC address of the remove ble device
# CHARACTERISTIC_UUID2 = "19b10000-e8f2-537e-4f6c-d104768a1214"
# address2= "84:f5:9a:b9:e4:13"



if __name__ == "__main__":
    # peripheral1, service_uuid1, characteristic_uuid1 = initialize_bt(mac=address2, uuid=CHARACTERISTIC_UUID2)
    # peripheral2, service_uuid2, characteristic_uuid2 = initialize_bt(mac=address1, uuid=CHARACTERISTIC_UUID1)
    peripheral2, service_uuid2, characteristic_uuid2 = initialize_bt()
    start_calibrating_byte_sent = False
    end_calibrating_byte_sent = False

    try:

        # Haptic signal here to signal beginning of calibration
        # Example condition to trigger the motor
        start_calibrating = True  # Replace with your actual condition
        # stop once Acked 
        if start_calibrating and not start_calibrating_byte_sent:
            print("entered start calibrating conditional")
            print("(BT to Arduino) Sending calibration start haptic signal...")
            # time.sleep(5)  # Delay to ensure the motor is activated
            # print("just slept for 5 seconds")
            print("(BT) about to send a 6")
            peripheral2.write_command(service_uuid2, characteristic_uuid2, b'6')  # Send signal to glove 1 Arduino to trigger motors
            print("(BT) after sending a 6")
            print("I should only see this printed once?")
            start_calibrating_byte_sent = True 


        print("Calibrating for 5 second, please move between max and min flexion")
        curTime = time.time()
        print("curTime is:", curTime)
        while time.time() - curTime < 5: # 5 second period of calibration
            time.sleep(0.05)
            # haptic won't send anything back so we just wait 

        
        

        print("Now the time is:", time.time(), "...I expect this to be 5 seconds after curTime")
        # Haptic signal here to signal end of calibration
        # Example condition to trigger the motor
        end_calibrating = True  # Replace with your actual condition

        if end_calibrating and not end_calibrating_byte_sent:
            print("(BT to Arduino) Sending calibration end haptic signal...")

            peripheral2.write_command(service_uuid2, characteristic_uuid2, b'7')  # Send signal to Arduino to trigger motor
            time.sleep(1)  # Delay to ensure the motor is activated
            end_calibrating_byte_sent = True
            
        print("Press enter to start inference (don't actually, this is just a test)")
        # Testing sign_detected signal 
        time.sleep(3)
        sign_detected = True
        if sign_detected: 
            print("(BT to Arduino) Sending sign detected haptic signal...")
            peripheral2.write_command(service_uuid2, characteristic_uuid2, b'8')  # Send signal to Arduino to trigger motor
            time.sleep(3)
    


    except KeyboardInterrupt:
        print("KeyboardInterrupt: Stopping inference...")
        # peripheral1.disconnect()
        try: 
            peripheral2.disconnect()
            exit()
        except: 
            print("There was an error disconnecting peripheral")
        
        

# Run command below in scripts folder
# python haptic_basic_test.py
        