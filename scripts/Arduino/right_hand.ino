#include "Arduino_BMI270_BMM150.h"
#include <ArduinoBLE.h>

float x, y, z;
float dx, dy, dz;
float mx, my, mz;
int degreesX = 0;
int degreesY = 0;
int motorPin = 9;

BLEService customService("19B10000-E8F2-537E-4F6C-D104768A1214"); // define a custom service UUID
BLECharacteristic customCharacteristic("19B10001-E8F2-537E-4F6C-D104768A1214", BLERead | BLEWrite, 500); // define a custom characteristic UUID

void setup() {
  pinMode(motorPin, OUTPUT);
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

}

void loop() {
  BLEDevice central = BLE.central();

  if (central) {
    Serial.print("Connected to central: ");
    Serial.println(central.address());

    while (central.connected()) {
      char incomingByte = central.read();
      if (incomingByte == '1') { // Calibration signal from BT to Arduino 
      // Activate the haptic motor (pulse, vibrate, etc.)
        digitalWrite(motorPin, HIGH);
        delay(1000); // Pulse duration (1 second)
        digitalWrite(motorPin, LOW);
      }
      if (incomingByte == '2') { // "Sign detected" signal from BT to Arduino 
        digitalWrite(motorPin, HIGH);
        delay(500); // Pulse duration (1 second)
        digitalWrite(motorPin, LOW);
      }
      double voltageThumb = analogRead(A3); // Read the analog input on pin A0
      double voltagePoint = analogRead(A5); // Read the analog input on pin A0
      double voltageMiddle = analogRead(A7); // Read the analog input on pin A0
      double voltageRing = analogRead(A6); // Read the analog input on pin A0
      double voltagePinky = analogRead(A4); // Read the analog input on pin A0

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