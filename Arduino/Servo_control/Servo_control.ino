#include <Servo.h>
byte inPin  = 2;
int servoState = 0;
int lastServoState = 0;

Servo myservo;  // create servo object to control a servo

void setup() {
  myservo.attach(6);  // attaches the servo on pin 9 to the servo object
  pinMode(inPin, INPUT); //Set pin 2 as input
  myservo.write(180);
}

void loop() {
  servoState = digitalRead(inPin);
  if (servoState != lastServoState) {
    //If state has changed, send PWM to servo
    if (servoState == HIGH){
      //If servoState is HIGH, send to 15 degrees
      myservo.write(15);
    } else{
      //If servoState is LOW, send to 190 degrees
      myservo.write(190);
    }
  }
  //Save last state
  lastServoState = servoState;
}
