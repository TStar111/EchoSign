#include <SoftwareSerial.h>
#include <Arduino_LSM9DS1.h>

void initIMU() {
    if (!IMU.begin()) {
        Serial.print("IMU failed to initialize!");
    }
    Serial.print("IMU initialized");
}

void initFlex() {

}

float accelerationX, accelerationY, accelerationZ;
int flex1, flex2, flex3, flex4, flex5;

// Example sensor reading functions
void readIMUSensor() {
  // Placeholder for reading an IMU sensor
  IMU.readAcceleration(accelerationX, accelerationY, accelerationZ);
}

void readFlexSensor() {
  // Placeholder for reading a flex sensor
  flex1 = analogRead(A0);
  flex2 = analogRead(A1);
  flex3 = analogRead(A2);
  flex4 = analogRead(A3);
  flex5 = analogRead(A4);
}

void setup() {
  // Initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  initIMU();
  initFlex();

}

void loop() {
  // Read sensors
  readIMUSensor();
  readFlexSensor();
  
  // Get the current time
  unsigned long currentTime = millis();
  
  // Send data to the computer in CSV format
  Serial.print(currentTime);
  Serial.print(",");
  Serial.print(accelerationX);
  Serial.print(",");
  Serial.print(accelerationY);
  Serial.print(",");
  Serial.print(accelerationZ);
  Serial.print(",");
  Serial.println(flex1);
  Serial.print(",");
  Serial.println(flex2);
  Serial.print(",");
  Serial.println(flex3);
  Serial.print(",");
  Serial.println(flex4);
  Serial.print(",");
  Serial.println(flex5);

  
  
  // Check if data is available to read from the Python script
  if (Serial.available() > 0) {
    // Read the incoming byte:
    String command = Serial.readStringUntil('\n');
    
    Serial.print("Received command: ");
    Serial.println(command); // if this is a gesture, light up an LED
  }
  
  // Delay a bit for stability and to match the data rate
  delay(40);
}
