#include "Arduino_BMI270_BMM150.h"

void setup() {
  Serial.begin(9600);
  while (!Serial);

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  Serial.println("IMU initialized successfully!");
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
    // Read analog pins
    float analog1 = analogRead(A0);
    float analog2 = analogRead(A1);
    float analog3 = analogRead(A2);
    float analog4 = analogRead(A3);
    float analog5 = analogRead(A4);
    
    // Format should be Thumb, Index, Middle, Ring, Pinky, 
    // Format the data into a single string for CSV
    String data = String(analog1) + "," + String(analog2) + "," + String(analog3) + "," + String(analog4) + "," + String(analog5) + ",";
    data += String(accelX) + "," + String(accelY) + "," + String(accelZ) + ",";
    data += String(gyroX) + "," + String(gyroY) + "," + String(gyroZ) + ",";
    data += String(magX) + "," + String(magY) + "," + String(magZ);
    
    // Send data over serial
    Serial.println(data);
    
    // Delay for some time before reading again
    delay(1000);

}
}
