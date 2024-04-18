#include "Arduino_BMI270_BMM150.h"
#include <Adafruit_DRV2605.h>
#include <ArduinoBLE.h>

float x, y, z;
float dx, dy, dz;
float mx, my, mz;
int degreesX = 0;
int degreesY = 0;
int motorPin = 9;

Adafruit_DRV2605 drv; // haptic motor driver object


BLEService customService("19B10000-E8F2-537E-4F6C-D104768A1214"); // define a custom service UUID
BLECharacteristic customCharacteristic("19B10001-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify | BLEWrite, 500); // define a custom characteristic UUID

void setup() {
  pinMode(motorPin, OUTPUT);
  Serial.begin(9600);

  if (!BLE.begin()) {
    Serial.println("Starting BLE failed!");
    while (1);
  }

  if (! drv.begin()) {
    Serial.println("Could not find DRV2605");
    while (1) delay(10);
  }
  

  BLE.setLocalName("RightHand");
  BLE.setAdvertisedService(customService);

  customService.addCharacteristic(customCharacteristic);
  BLE.addService(customService);

  customCharacteristic.setValue(0);

  BLE.advertise();
  Serial.println("BLE server is up and advertising!");

  String address = BLE.address();

  Serial.print("Local address is: ");
  Serial.println(address);

  // Initialize the DRV2605
  drv.begin();
//  drv.useLRA()
  drv.selectLibrary(1);
  drv.setMode(DRV2605_MODE_INTTRIG);

  
//  // Set the waveform for a custom pulse
//  uint8_t waveform[] = {0x5E, 0x00}; // Customize the waveform data according to your requirements
//  drv.setWaveform(0, waveform, sizeof(waveform));
//
}

uint8_t effect = 8;

void loop() {
  BLEDevice central = BLE.central();
  char incomingByte; 
  if (central) {
    Serial.print("Connected to central: ");
    Serial.println(central.address());

    while (central.connected()) {
      char incomingByte = customCharacteristic.canRead(); // might be canRead()
      Serial.println("incomingByte is: "); 
      Serial.println(incomingByte); 
      if (incomingByte == '1') { // Calibration signal from BT to Arduino 
      // Activate the haptic motor (pulse, vibrate, etc.)
        effect = 8; 
        if (effect == 8) {
          Serial.println(F("8 − Soft Bump - 60%"));
        }
        drv.setWaveform(0, effect);  // play effect 
        drv.setWaveform(1, 0);       // end waveform

        // play the effect!
        drv.go(); 
        
//        digitalWrite(motorPin, HIGH);
//        delay(1000); // Pulse duration (1 second)
//        digitalWrite(motorPin, LOW);
      }
      if (incomingByte == '2') { // "Sign detected" signal from BT to Arduino 
        effect = 104; 
        if (effect == 104) {
          Serial.println(F("104 − Transition Ramp Down Short Sharp 1 – 50 to 0%"));
        }
        
        // set the effect to play
        drv.setWaveform(0, effect);  // play effect 
        drv.setWaveform(1, 0);       // end waveform
      
        // play the effect!
        drv.go();
//        digitalWrite(motorPin, HIGH);
//        delay(500); // Pulse duration (1 second)
//        digitalWrite(motorPin, LOW);
      }
    }

    Serial.print("Disconnected from central: ");
    Serial.println(central.address());
  }
  delay(10); // Delay a second between readings
}

