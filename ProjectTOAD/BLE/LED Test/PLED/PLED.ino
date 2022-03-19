#include <ArduinoBLE.h>
//#define BLEaddress "19b10000-e8f2-537e-4f6c-d104768a1214"
#define BLEaddress "181A"
#define BLEencoder "2A6E"

BLEService ledService(BLEaddress); // BLE LED Service

// BLE LED Switch Characteristic - custom 128-bit UUID, read and writable by central
BLEByteCharacteristic switchCharacteristic(BLEencoder, BLERead | BLEWrite);

const int ledPin = LED_BUILTIN; // pin to use for the LED
int delaynum = 10;
int counter = 0;
void setup() {
  Serial.begin(9600);
//  while (!Serial);

  // set LED pin to output mode
  pinMode(ledPin, OUTPUT);

  // begin initialization
  if (!BLE.begin()) {
    //Serial.println("starting BLE failed!");

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
  int Val;
  int counter = 0;
  switchCharacteristic.readValue(Val);
  if(Val == 54)
  {
    counter = 1;
  }
  // if a central is connected to peripheral:
  if ((central)&&(counter == 1)) {
    
    while (central.connected()) {
      // if the remote device wrote to the characteristic,
      // use the value to control the LED:
      delay(delaynum);
      if(counter == 0){
        digitalWrite(ledPin,HIGH);
        
        switchCharacteristic.writeValue(1);
        counter = 1;
      }
      else{
        digitalWrite(ledPin,LOW);
        
        switchCharacteristic.writeValue(0);
        counter = 0;
      }
    }

    // when the central disconnects, print it out:
    //Serial.print(F("Disconnected from central: "));
    //Serial.println(central.address());
  }
}
