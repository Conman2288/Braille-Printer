#include <Servo.h>

Servo servo;
int servo_pin = 3;
int motor_pin = 5;
int servo_rotation_count = 0; // variable to count the number of times the servo has rotated
int enA = 7;         // Motor A connections
int in1 = 8;
int in2 = 9;
int in3 = 10;
int in4 = 11;
int enB = 12;
int distance = 0;


void move_emb_left(){
    digitalWrite(in1, LOW); // moves embosser to left
    digitalWrite(in2, HIGH);
    delay(2000);
}

void move_emb_right(){
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    delay(2000);
}

void stop_emb(){
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
}

void move_wheel_left(){
    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);
    delay(2500);
}

void move_emb_all_left(){
    digitalWrite(in1, LOW); // moves embosser to left
    digitalWrite(in2, HIGH);
    delay(10000);
}

void move_emb_all_right(){
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    delay(10000);
}

void move_wheel_right(){

    digitalWrite(in4, LOW);
    digitalWrite(in3, HIGH);
    delay(2500);
}

void stop_wheel(){
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
}


void move_wheel_all_left(){
    digitalWrite(in3, LOW);
    digitalWrite(in4, HIGH);
    delay(10000);
}

   
void move_wheel_all_right(){
    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);
    delay(10000);
}

void setup() {
  // initialize serial communication
  Serial.begin(9600);

  
  // Set all the motor control pins to outputs
  pinMode(enA, OUTPUT);
  pinMode(enB, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  digitalWrite(in1, LOW);    // Turn off motors - Initial state
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);


  // attach servo to pin
  servo.attach(servo_pin);

  // set motor pin as output
  pinMode(motor_pin, OUTPUT);

  // set pin 5 as output
  pinMode(5, OUTPUT);

  
  // Set all the motor control pins to outputs
  pinMode(enA, OUTPUT);
  pinMode(enB, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  digitalWrite(in1, LOW);    // Turn off motors - Initial state
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
  
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

      // controls the main motors
      analogWrite(enA, 255);
      analogWrite(enB, 255);

      move_emb_right();
      stop_emb();

      digitalWrite(in4, LOW);
      digitalWrite(in3, HIGH);
      delay(2000);
      stop_wheel();
      //move_wheel_left();
      //stop_wheel();
      digitalWrite(in4, LOW);
      digitalWrite(in3, HIGH);
      delay(2000);

      
      
      // check if the servo has rotated 4 times
      if (servo_rotation_count == 20) {
        digitalWrite(motor_pin, HIGH); // activate motor pin
        delay(1200); // delay for a short period of time
        digitalWrite(motor_pin, LOW); // deactivate motor pin
        delay(1200); // delay for a short period of time
        servo_rotation_count = 0;
      }
    }
  }
}
