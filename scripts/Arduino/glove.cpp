#include <SoftwareSerial.h>

void initIMU() {

}

void initFlex() {

}

// Example sensor reading functions
int readIMUSensor() {
  // Placeholder for reading an IMU sensor
  return analogRead(A0); // Example reading
}

int readFlexSensor() {
  // Placeholder for reading a flex sensor
  return analogRead(A1); // Example reading
}

void setup() {
  // Initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  initIMU();
  initFlex();

}

void loop() {
  // Read sensors
  int imuReading = readIMUSensor();
  int flexReading = readFlexSensor();
  
  // Get the current time
  unsigned long currentTime = millis();
  
  // Send data to the computer in CSV format
  Serial.print(currentTime);
  Serial.print(",");
  Serial.print(imuReading);
  Serial.print(",");
  Serial.println(flexReading);
  
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
