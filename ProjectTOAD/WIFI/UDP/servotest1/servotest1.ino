#include <Servo.h>
Servo servo1;
int servoPin = 9;
int val = 0;
void setup() {
  servo1.attach(servoPin);
}
void loop() {
  // Notes on integer being writen to servo:
    // 0-89 is CW rotation (0 fastest  to 89 slowest)
    // 91-180 is CCW rotation (91 slowest to 180 fastest)
    // 90 is stationary
  //delay(2000);
//  if(val >= 360){
//    val = 0;
//  }
//  servo1.write(val);
//  val++;
//  delay(100);
  servo1.write(85);
}
