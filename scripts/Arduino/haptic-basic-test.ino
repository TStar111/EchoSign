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
BLECharacteristic customCharacteristic("19B10001-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify | BLEWriteWithoutResponse | BLEWrite, 500); // define a custom characteristic UUID

void setup() {
  Serial.begin(9600);
  while(!Serial); 
  Serial.println("entered setup()"); 
  pinMode(motorPin, OUTPUT);
  

  if (!BLE.begin()) {
    Serial.println("Starting BLE failed!");
    while (1);
  }

  if (!drv.begin()) {
    Serial.println("Could not find DRV2605");
    while (1) delay(10);
  }
  

  BLE.setLocalName("LeftHand");
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
  Serial.println("Everything in setup worked"); 
  
//  // Set the waveform for a custom pulse
//  uint8_t waveform[] = {0x5E, 0x00}; // Customize the waveform data according to your requirements
//  drv.setWaveform(0, waveform, sizeof(waveform));
//
}

uint8_t effect = 15;
bool rcvdStartCalSignal = false; 
bool rcvdEndCalSignal = false; 

void loop() {
//  Serial.println("Entered loop"); 
  BLEDevice central = BLE.central();
  char incomingByte; 
  if (central) {
    Serial.print("Connected to central: ");
    Serial.println(central.address());
    byte incomingByte; 
    while (central.connected()) {
      customCharacteristic.readValue(incomingByte); // might be canRead() 
      
//      Serial.println(incomingByte); 
      if (incomingByte == '6' && !rcvdStartCalSignal) { // Calibration signal from BT to Arduino 
      // Activate the haptic motor (pulse, vibrate, etc.)
        Serial.println("START calibration signal received!"); 
        // Serial.println("incomingByte is: "); // should only print if canRead()
        // Serial.println(incomingByte);
        effect = 15; 
        if (effect == 8) {
          // Serial.println(F("8 − Soft Bump - 60%"));
        }
        drv.setWaveform(0, effect);  // play effect 
        drv.setWaveform(1, 0);       // end waveform

        // play the effect!
        drv.go(); 
        delay(1500); // play it for a bit 
        drv.stop(); // stop the effect 
        Serial.println("stopped first effect"); 
        rcvdStartCalSignal = true;
        
//        digitalWrite(motorPin, HIGH);
//        delay(1000); // Pulse duration (1 second)
//        digitalWrite(motorPin, LOW);
      }
      if (incomingByte == '7' && !rcvdEndCalSignal) { // "Sign detected" signal from BT to Arduino 
        effect = 15; 
        Serial.println("END calibration signal received!"); 
        // Serial.println("incomingByte is: "); // should only print if canRead()
        // Serial.println(incomingByte);
        if (effect == 104) {
          // Serial.println(F("104 − Transition Ramp Down Short Sharp 1 – 50 to 0%"));
        }
        
        // set the effect to play
        drv.setWaveform(0, effect);  // play effect 
        drv.setWaveform(1, 0);       // end waveform
      
        // play the effect!
        drv.go();
        delay(1500); // play it for a bit 
        drv.stop(); // stop the effect 
//        digitalWrite(motorPin, HIGH);
//        delay(500); // Pulse duration (1 second)
//        digitalWrite(motorPin, LOW);
        rcvdEndCalSignal = true; 
      }
      if (incomingByte == '8') {
        effect = 15; 
        Serial.println("SIGN DETECTED signal received!"); 
        // Serial.println("incomingByte is: ");
        // Serial.println(incomingByte);
        if (effect == 15) {
          // Serial.println(F("15 − 750-ms alert 100%"));
        }
        // set the effect to play
        drv.setWaveform(0, effect);  // play effect 
        drv.setWaveform(1, 0);       // end waveform
      
        // play the effect!
        drv.go();
        delay(10); // play it for a bit 
        drv.stop(); // stop the effect 
      }
    }

    Serial.print("Disconnected from central: ");
    Serial.println(central.address());
  }
  delay(10); // Delay a second between readings
}
