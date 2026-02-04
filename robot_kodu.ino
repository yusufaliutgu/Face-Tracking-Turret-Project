/*
 * Project: Autonomous Face Tracking Turret Firmware
 * Platform: Arduino UNO
 * Description: Receives coordinates from Python (via Serial) to control 
 * Pan/Tilt servo mechanism and manages laser activation logic.
 */

#include <Servo.h>

// --- Pin Definitions ---
const int PIN_SERVO_PAN = 9;   // X-Axis Servo
const int PIN_SERVO_TILT = 10; // Y-Axis Servo
const int PIN_LASER = 11;      // Laser Module

// --- System Objects & Variables ---
Servo panServo;
Servo tiltServo;

unsigned long lastDataTimestamp = 0;   // For safety timeout logic
const int TIMEOUT_DURATION = 200;      // Deactivate laser if no data for 200ms

void setup() {
  // Initialize Serial Communication
  Serial.begin(9600);
  Serial.setTimeout(10); // Low timeout for low latency tracking

  // Hardware Initialization
  panServo.attach(PIN_SERVO_PAN);
  tiltServo.attach(PIN_SERVO_TILT);
  pinMode(PIN_LASER, OUTPUT);

  // Initial State (Safe Mode)
  digitalWrite(PIN_LASER, LOW); // Laser OFF initially
  panServo.write(90);           // Center Position
  tiltServo.write(90);
}

void loop() {
  // Check if tracking data is available from Host PC
  if (Serial.available() > 0) {
    
    // 1. Target Acquired: Activate Laser
    digitalWrite(PIN_LASER, HIGH);
    lastDataTimestamp = millis(); // Reset safety timer

    // 2. Parse Incoming Data Packet (Format: "X,Y\n")
    String inputData = Serial.readStringUntil('\n');
    int delimiterIndex = inputData.indexOf(',');

    if (delimiterIndex > 0) {
      String xVal = inputData.substring(0, delimiterIndex);
      String yVal = inputData.substring(delimiterIndex + 1);

      // Update Servo Actuators
      panServo.write(xVal.toInt());
      tiltServo.write(yVal.toInt());
    }
  }

  // 3. Safety Protocol: Auto-OFF if target is lost
  // If no new data is received within the timeout duration, turn off the laser.
  if (millis() - lastDataTimestamp > TIMEOUT_DURATION) {
    digitalWrite(PIN_LASER, LOW);
  }
}