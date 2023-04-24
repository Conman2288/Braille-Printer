#include <Servo.h>

Servo servo;
int servo_pin = 3;
int motor_pin = 5;
int servo_rotation_count = 0; // variable to count the number of times the servo has rotated

void setup() {
  // initialize serial communication
  Serial.begin(9600);

  // attach servo to pin
  servo.attach(servo_pin);

  // set motor pin as output
  pinMode(motor_pin, OUTPUT);

  // set pin 5 as output
  pinMode(5, OUTPUT);
}

void loop() {
  // wait for input from Python program
  if (Serial.available() > 0) {
    // read input from Python program
    String input = Serial.readString();

    // if input is a position, move servo to that position
    if (input.toInt() >= 0 && input.toInt() <= 180) {
      servo.write(input.toInt());
      servo_rotation_count++;

      // check if the servo has rotated 5 times
      if (servo_rotation_count == 5) {
        digitalWrite(motor_pin, HIGH); // activate motor pin
        delay(1200); // delay for a short period of time
        digitalWrite(motor_pin, LOW); // deactivate motor pin
        delay(1200); // delay for a short period of time
        servo_rotation_count = 0;
      }
    }
  }
}
