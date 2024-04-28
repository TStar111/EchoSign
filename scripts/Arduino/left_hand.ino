#include "Arduino_BMI270_BMM150.h"
#include <Adafruit_DRV2605.h>
#include <ArduinoBLE.h>

float x, y, z;
float dx, dy, dz;
float mx, my, mz;
int degreesX = 0;
int degreesY = 0;

Adafruit_DRV2605 drv; // haptic motor driver object

BLEService customService("19B10000-E8F2-537E-4F6C-D104768A1214"); // define a custom service UUID
BLECharacteristic customCharacteristic("19B10001-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify | BLEWriteWithoutResponse | BLEWrite, 500); // define a custom characteristic UUID

void setup() {
  Serial.begin(9600);
  // while (!Serial);
  // Serial.println("Started");
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }
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

  uint8_t effect = 15;
  bool rcvdStartCalSignal = false; 
  bool rcvdEndCalSignal = false;


}

void loop() {
  BLEDevice central = BLE.central();

  if (central) {
    Serial.print("Connected to central: ");
    Serial.println(central.address());
    byte incomingByte;
    while (central.connected()) {
      /* Start of haptic code */ 
      customCharacteristic.readValue(incomingByte);
      if (incomingByte == '6' && !rcvdStartCalSignal) { // Start calibration signal from BT to Arduino 
      
        // Serial.println("START calibration signal received!"); 
        
        effect = 15; 
        drv.setWaveform(0, effect);  // play effect 
        drv.setWaveform(1, 0);       // end waveform

        drv.go(); // play the effect!
        delay(1500); // play it for a bit 
        drv.stop(); // stop the effect 
       
        rcvdStartCalSignal = true;
        
      }
      if (incomingByte == '7' && !rcvdEndCalSignal) { // End calibration from BT to Arduino 
        effect = 15; 
        // Serial.println("END calibration signal received!"); 
  
        drv.setWaveform(0, effect);  // set the effect to play
        drv.setWaveform(1, 0);       // end waveform
      
        
        drv.go(); // play the effect!
        delay(1500); // play it for a bit 
        drv.stop(); // stop the effect 

        rcvdEndCalSignal = true; 
      }
      if (incomingByte == '8') {
        effect = 15; 
        // Serial.println("SIGN DETECTED signal received!"); 

        drv.setWaveform(0, effect);  // set the effect to play
        drv.setWaveform(1, 0);       // end waveform
        
        drv.go(); // play the effect!
        delay(10); // play it for a bit 
        drv.stop(); // stop the effect 
      }
      /* End of haptic code */ 
      
      
      double voltageThumb = analogRead(A3); // Read the analog input on pin A0
      double voltagePoint = analogRead(A4); // Read the analog input on pin A0
      double voltageMiddle = analogRead(A5); // Read the analog input on pin A0
      double voltageRing = analogRead(A6); // Read the analog input on pin A0
      double voltagePinky = analogRead(A7); // Read the analog input on pin A0

      if (IMU.accelerationAvailable()) {
        IMU.readAcceleration(x, y, z);
      }
      if (IMU.gyroscopeAvailable()) {
        IMU.readGyroscope(dx, dy, dz);
      }
      if (IMU.magneticFieldAvailable()) {
        IMU.readMagneticField(mx, my, mz);
      }

      float floatArray[14] = {voltageThumb, voltagePoint, voltageMiddle, voltageRing, voltagePinky, x, y, z, dx, dy, dz, mx, my, mz};
      // Buffer to hold bytes
      uint8_t byteArray[sizeof(floatArray)];
      
      // Convert float array to byte array
      memcpy(byteArray, floatArray, sizeof(floatArray));
      
      // Send byte array over BLE
      customCharacteristic.writeValue(byteArray, sizeof(floatArray));
      
    }

    Serial.print("Disconnected from central: ");
    Serial.println(central.address());
  }
  delay(10); // Delay a second between readings
}#include "Arduino_BMI270_BMM150.h"
#include <ArduinoBLE.h>

float x, y, z;
float dx, dy, dz;
float mx, my, mz;
int degreesX = 0;
int degreesY = 0;

BLEService customService("19B10000-E8F2-537E-4F6C-D104768A1214"); // define a custom service UUID
BLECharacteristic customCharacteristic("19B10001-E8F2-537E-4F6C-D104768A1214", BLERead | BLEWrite, 500); // define a custom characteristic UUID

void setup() {
  Serial.begin(9600);
  // while (!Serial);
  // Serial.println("Started");
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }
  if (!BLE.begin()) {
    Serial.println("Starting BLE failed!");
    while (1);
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

}

void loop() {
  BLEDevice central = BLE.central();

  if (central) {
    Serial.print("Connected to central: ");
    Serial.println(central.address());

    while (central.connected()) {

      double voltageThumb = analogRead(A3); // Read the analog input on pin A0
      double voltagePoint = analogRead(A4); // Read the analog input on pin A0
      double voltageMiddle = analogRead(A5); // Read the analog input on pin A0
      double voltageRing = analogRead(A6); // Read the analog input on pin A0
      double voltagePinky = analogRead(A7); // Read the analog input on pin A0

      if (IMU.accelerationAvailable()) {
        IMU.readAcceleration(x, y, z);
      }
      if (IMU.gyroscopeAvailable()) {
        IMU.readGyroscope(dx, dy, dz);
      }
      if (IMU.magneticFieldAvailable()) {
        IMU.readMagneticField(mx, my, mz);
      }

      float floatArray[14] = {voltageThumb, voltagePoint, voltageMiddle, voltageRing, voltagePinky, x, y, z, dx, dy, dz, mx, my, mz};
      // Buffer to hold bytes
      uint8_t byteArray[sizeof(floatArray)];
      
      // Convert float array to byte array
      memcpy(byteArray, floatArray, sizeof(floatArray));
      
      // Send byte array over BLE
      customCharacteristic.writeValue(byteArray, sizeof(floatArray));
      
    }

    Serial.print("Disconnected from central: ");
    Serial.println(central.address());
  }
  delay(10); // Delay a second between readings
}