#include <Servo.h>
byte inPin  = 2;

Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int pos = 0;    // variable to store the servo position

void setup() {
  myservo.attach(6);  // attaches the servo on pin 9 to the servo object
  pinMode(inPin, INPUT); //Set pin 2 as input
  myservo.write(pos); //Servo goes to default position
}

void loop() {
bool pinVal = digitalRead(inPin);
if (pinVal == HIGH){
  myservo.write(180);             // tell servo to go to cutting position
}
else{
myservo.write(0);             // tell servo to go to neutral position
}
}
