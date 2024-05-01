#include "Arduino_BMI270_BMM150.h"

void setup() {
  Serial.begin(9600);
  while (!Serial);

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  // Serial.println("IMU initialized successfully!");
}

void loop() {
  if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable() && IMU.magneticFieldAvailable()) {
    // Read accelerometer data
    float accelX, accelY, accelZ;
    IMU.readAcceleration(accelX, accelY, accelZ);

    // Read gyroscope data
    float gyroX, gyroY, gyroZ;
    IMU.readGyroscope(gyroX, gyroY, gyroZ);

    // Read magnetometer data
    float magX, magY, magZ;
    IMU.readMagneticField(magX, magY, magZ);
    // Read analog pins (PCB: 6,0,2,1,3)
    double thumb = analogRead(A6); // Read the analog input on pin A0
    double pointer = analogRead(A0); // Read the analog input on pin A0
    double middle = analogRead(A2); // Read the analog input on pin A0
    double ring = analogRead(A1); // Read the analog input on pin A0
    double pinky = analogRead(A3); // Read the analog input on pin A0
    
    // Format should be Thumb, Index, Middle, Ring, Pinky, 
    // Format the data into a single string for CSV
    String data = String(thumb) + "," + String(pointer) + "," + String(middle) + "," + String(ring) + "," + String(pinky) + ",";
    data += String(accelX) + "," + String(accelY) + "," + String(accelZ) + ",";
    data += String(gyroX) + "," + String(gyroY) + "," + String(gyroZ) + ",";
    data += String(magX) + "," + String(magY) + "," + String(magZ);
    
    // Send data over serial
    Serial.println(data);
    
    // Delay for some time before reading again
    delay(5);

}
}
