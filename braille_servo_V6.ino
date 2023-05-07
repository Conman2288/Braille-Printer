#include <Servo.h>

Servo servo;
int servo_pin = 3;
int motor_pin = 5;
int servo_rotation_count = 0; // variable to count the number of times the servo has rotated
int enA = 7;         // Motor connections
int in1 = 8;
int in2 = 9;
int in3 = 10;
int in4 = 11;
int enB = 12;
bool servo_moved = false; // boolean variable to keep track of whether the servo has moved
bool roller_setup = true;

void move_emb_left(){
    digitalWrite(in1, LOW); // moves embosser to left a character
    digitalWrite(in2, HIGH);
    delay(1850);
}

void move_emb_right(){
    digitalWrite(in1, HIGH); // moves the embosser to the right a character
    digitalWrite(in2, LOW);
    delay(1850);
}

void all_left(){
    digitalWrite(in1, LOW); // moves embosser from right margin to left 
    digitalWrite(in2, HIGH);
    delay(42000);
}

void all_right(){
    digitalWrite(in1, HIGH); // moves embosser from left margin to right
    digitalWrite(in2, LOW);
    delay(42000);
}

void stop_emb(){
    digitalWrite(in1, LOW); // stops the embosser
    digitalWrite(in2, LOW);
}


void move_up(){
    digitalWrite(in3, HIGH); // moves the embosser vertically up
    digitalWrite(in4, LOW);
    delay(250);
}

void move_down(){
    digitalWrite(in3, LOW); // moves the embosser into the paper
    digitalWrite(in4, HIGH);
    delay(250);
}

void stop_press(){
    digitalWrite(in3, LOW); // stops the presser
    digitalWrite(in4, LOW);
}

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
  if (roller_setup){
    digitalWrite(motor_pin, HIGH); // activate motor pin
    delay(2000); // delay for a short period of time
    digitalWrite(motor_pin, LOW); // deactivate motor pin
    delay(1200); // delay for a short period of time
    roller_setup = false;
  }
  
  // wait for input from Python program
  if (Serial.available() > 0) {
    // read input from Python program
    String input = Serial.readString();
  
    // if input is a position, move servo to that position
    if (input.toInt() >= 0 && input.toInt() <= 180) {
      // move servo to desired position
      servo.write(input.toInt());
      delay(400);
      
      // increment servo rotation count
      servo_rotation_count++;

      // check if the servo has rotated 20 times
      if (servo_rotation_count == 20) {
        digitalWrite(motor_pin, HIGH); // activate motor pin
        delay(950); // delay for a short period of time
        digitalWrite(motor_pin, LOW); // deactivate motor pin
        delay(950); // delay for a short period of time
        servo_rotation_count = 0;
        all_right(); // Moves the embosser back to left margin
      }

      // execute other functions
      analogWrite(enA, 255);
      analogWrite(enB, 255);
      move_emb_left();
      stop_emb();

     if (input.toInt() != 0){ // moves the embosser up and down into the paper
      move_down();
      stop_press();
      move_up();
      stop_press();
      }
    }
  }
}
