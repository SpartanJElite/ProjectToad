#include <Servo.h>
Servo servo1;
int servoPin = 9;
void setup() {
  servo1.attach(servoPin);
}
void loop() {
  // Notes on integer being writen to servo:
    // 0-89 is CW rotation (0 fastest  to 89 slowest)
    // 91-180 is CCW rotation (91 slowest to 180 fastest)
    // 90 is stationary
  //delay(2000);
  servo1.write(81);
  delay(3350);
  servo1.write(90);
  delay(3000);
  servo1.write(102);
  delay(3580);
  servo1.write(90);
  delay(3000);
}
