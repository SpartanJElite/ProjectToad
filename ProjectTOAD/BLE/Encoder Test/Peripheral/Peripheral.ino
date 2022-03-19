/* PROJECT TOAD: Client Peripheral Bluetooth Encoder
 * 
 */

#include <ArduinoBLE.h>
#include <Wire.h> 
//#define BLEaddress "19b10000-e8f2-537e-4f6c-d104768a1214"
#define BLEaddress "181A"
#define BLEencoder "2A6E"

BLEService ledService(BLEaddress); // BLE LED Service

// BLE LED Switch Characteristic - custom 128-bit UUID, read and writable by central
BLEByteCharacteristic switchCharacteristic(BLEencoder, BLERead | BLEWrite);

const int ledPin = LED_BUILTIN; // pin to use for the LED
int delaynum = 10;
int counter = 0;
//---------------------------------------------------------------------------
//Magnetic sensor things
int magnetStatus = 0; //value of the status register (MD, ML, MH)

int lowbyte; //raw angle 7:0
word highbyte; //raw angle 7:0 and 11:8
int rawAngle; //final raw angle 
float degAngle; //raw angle in degrees (360/4096 * [value between 0-4095])

int quadrantNumber, previousquadrantNumber; //quadrant IDs
float numberofTurns = 0; //number of turns
float correctedAngle = 0; //tared angle - based on the startup value
float startAngle = 0; //starting angle
float totalAngle = 0; //total absolute angular displacement
float previoustotalAngle = 0; //for the display printing




void setup() {
  Serial.begin(9600);
  while (!Serial);

  Wire.begin(); //start i2C  
  Wire.setClock(800000L); //fast clock
  BLE.begin();
  checkMagnetPresence(); //check the magnet (blocks until magnet is found)

  ReadRawAngle(); //make a reading so the degAngle gets updated
  startAngle = degAngle; //update startAngle with degAngle - for taring
  

  // begin initialization
  if (!BLE.begin()) {
    Serial.println("starting BLE failed!");

    while (1);
  }

  // set advertised local name and service UUID:
  BLE.setDeviceName("LED");
  BLE.setLocalName("LED");
  BLE.setAdvertisedService(ledService);

  // add the characteristic to the service
  ledService.addCharacteristic(switchCharacteristic);

  // add service
  BLE.addService(ledService);

  // set the initial value for the characeristic:
  switchCharacteristic.writeValue(0);

  // start advertising
  BLE.advertise();

  //Serial.println("BLE LED Peripheral");
}

void loop() {
  // listen for BLE peripherals to connect:
  BLEDevice central = BLE.central();
  int16_t Val;
  int counter = 0;
  switchCharacteristic.readValue(Val);
  if(Val == 54)
  {
    counter = 1;
  }
  // if a central is connected to peripheral:
  if ((central)&&(counter == 1)) {
    
    while (central.connected()) {
      ReadRawAngle(); //ask the value from the sensor
      correctAngle(); //tare the value
      checkQuadrant(); //check quadrant, check rotations, check absolute angular position
    }

    // when the central disconnects, print it out:
    Serial.print(F("Disconnected from central: "));
    Serial.println(central.address());
  }
}


void ReadRawAngle()
{ 
  //7:0 - bits
  Wire.beginTransmission(0x36); //connect to the sensor
  Wire.write(0x0D); //figure 21 - register map: Raw angle (7:0)
  Wire.endTransmission(); //end transmission
  Wire.requestFrom(0x36, 1); //request from the sensor
  
  while(Wire.available() == 0); //wait until it becomes available 
  lowbyte = Wire.read(); //Reading the data after the request
 
  //11:8 - 4 bits
  Wire.beginTransmission(0x36);
  Wire.write(0x0C); //figure 21 - register map: Raw angle (11:8)
  Wire.endTransmission();
  Wire.requestFrom(0x36, 1);
  
  while(Wire.available() == 0);  
  highbyte = Wire.read();
  
  //4 bits have to be shifted to its proper place as we want to build a 12-bit number
  highbyte = highbyte << 8; //shifting to left
  //What is happening here is the following: The variable is being shifted by 8 bits to the left:
  //Initial value: 00000000|00001111 (word = 16 bits or 2 bytes)
  //Left shifting by eight bits: 00001111|00000000 so, the high byte is filled in
  
  //Finally, we combine (bitwise OR) the two numbers:
  //High: 00001111|00000000
  //Low:  00000000|00001111
  //      -----------------
  //H|L:  00001111|00001111
  rawAngle = highbyte | lowbyte; //int is 16 bits (as well as the word)

  //We need to calculate the angle:
  //12 bit -> 4096 different levels: 360° is divided into 4096 equal parts:
  //360/4096 = 0.087890625
  //Multiply the output of the encoder with 0.087890625
  degAngle = rawAngle * 0.087890625; 
  
  Serial.print("Deg angle: ");
  Serial.println(degAngle, 2); //absolute position of the encoder within the 0-360 circle
  
}

void correctAngle()
{
  //recalculate angle
  correctedAngle = degAngle - startAngle; //this tares the position

  if(correctedAngle < 0) //if the calculated angle is negative, we need to "normalize" it
  {
  correctedAngle = correctedAngle + 360; //correction for negative numbers (i.e. -15 becomes +345)
  }
  else
  {
    //do nothing
  }
  int16_t tempAngle = correctedAngle;
  switchCharacteristic.writeValue(tempAngle);
  Serial.print("Corrected angle: ");
  Serial.println(correctedAngle, 2); //print the corrected/tared angle  
}

void checkQuadrant()
{
  /*
  //Quadrants:
  4  |  1
  ---|---
  3  |  2
  */

  //Quadrant 1
  if(correctedAngle >= 0 && correctedAngle <=90)
  {
    quadrantNumber = 1;
  }

  //Quadrant 2
  if(correctedAngle > 90 && correctedAngle <=180)
  {
    quadrantNumber = 2;
  }

  //Quadrant 3
  if(correctedAngle > 180 && correctedAngle <=270)
  {
    quadrantNumber = 3;
  }

  //Quadrant 4
  if(correctedAngle > 270 && correctedAngle <360)
  {
    quadrantNumber = 4;
  }
  //Serial.print("Quadrant: ");
  //Serial.println(quadrantNumber); //print our position "quadrant-wise"

  if(quadrantNumber != previousquadrantNumber) //if we changed quadrant
  {
    if(quadrantNumber == 1 && previousquadrantNumber == 4)
    {
      numberofTurns++; // 4 --> 1 transition: CW rotation
    }

    if(quadrantNumber == 4 && previousquadrantNumber == 1)
    {
      numberofTurns--; // 1 --> 4 transition: CCW rotation
    }
    //this could be done between every quadrants so one can count every 1/4th of transition

    previousquadrantNumber = quadrantNumber;  //update to the current quadrant
  
  }  
  //Serial.print("Turns: ");
  //Serial.println(numberofTurns,0); //number of turns in absolute terms (can be negative which indicates CCW turns)  

  //after we have the corrected angle and the turns, we can calculate the total absolute position
  totalAngle = (numberofTurns*360) + correctedAngle; //number of turns (+/-) plus the actual angle within the 0-360 range
  //Serial.print("Total angle: ");
  //Serial.println(totalAngle, 2); //absolute position of the motor expressed in degree angles, 2 digits
}

void checkMagnetPresence()
{  
  //This function runs in the setup() and it locks the MCU until the magnet is not positioned properly

  while((magnetStatus & 32) != 32) //while the magnet is not adjusted to the proper distance - 32: MD = 1
  {
    magnetStatus = 0; //reset reading

    Wire.beginTransmission(0x36); //connect to the sensor
    Wire.write(0x0B); //figure 21 - register map: Status: MD ML MH
    Wire.endTransmission(); //end transmission
    Wire.requestFrom(0x36, 1); //request from the sensor

    while(Wire.available() == 0); //wait until it becomes available 
    magnetStatus = Wire.read(); //Reading the data after the request

    Serial.print("Magnet status: ");
    Serial.println(magnetStatus, BIN); //print it in binary so you can compare it to the table (fig 21)
    delay(500);     
  }      
  
  //Status register output: 0 0 MD ML MH 0 0 0  
  //MH: Too strong magnet - 100111 - DEC: 39 
  //ML: Too weak magnet - 10111 - DEC: 23     
  //MD: OK magnet - 110111 - DEC: 55

  //Serial.println("Magnet found!");
  //delay(1000);  
}
