/* PROJECT TOAD: Client Central Bluetooth Controller
 * 
 */

//Libaries
#include <ArduinoBLE.h>

//Defined
#define BLEaddress "181A"
#define BLEencoder "2A6E"

//Setup Function
void setup() {
  Serial.begin(9600);
  while (!Serial);
  // initialize the BLE hardware
  BLE.begin();
  Serial.println("BLE Central - LED control");
  // start scanning for peripherals
  BLE.scanForUuid(BLEaddress);
}

void loop() {
  // check if a peripheral has been discovered
  BLEDevice peripheral = BLE.available();
  if (peripheral) {
    // discovered a peripheral, print out address, local name, and advertised service
    Serial.print("Found ");
    Serial.print(peripheral.address());
    Serial.print(" '");
    Serial.print(peripheral.localName());
    Serial.print("' ");
    Serial.print(peripheral.advertisedServiceUuid());
    Serial.println();
    if (peripheral.localName() != "LED") {
      return;
    }
    // stop scanning
    BLE.stopScan();
    controlLed(peripheral);
    // peripheral disconnected, start scanning again
    BLE.scanForUuid(BLEaddress);
  }
}

void controlLed(BLEDevice peripheral) {
  // connect to the peripheral
  Serial.println("Connecting ...");
  if (peripheral.connect()) {
    Serial.println("Connected");
  } else {
    Serial.println("Failed to connect!");
    return;
  }
  // discover peripheral attributes
  Serial.println("Discovering attributes ...");
  if (peripheral.discoverAttributes()) {
    Serial.println("Attributes discovered");
  } else {
    Serial.println("Attribute discovery failed!");
    peripheral.disconnect();
    return;
  }
  // retrieve the LED characteristic
  BLECharacteristic ledCharacteristic = peripheral.characteristic(BLEencoder);
  
  if (!ledCharacteristic) {
    Serial.println("Peripheral does not have LED characteristic!");
    peripheral.disconnect();
    return;
  } else if (!ledCharacteristic.canWrite()) {
    Serial.println("Peripheral does not have a writable LED characteristic!");
    peripheral.disconnect();
    return;
  }
  Serial.println("Everything is good!");
  ledCharacteristic.writeValue(54);
  int lednum;
  while (peripheral.connected()) {
    ledCharacteristic.readValue(lednum);
    Serial.println(lednum);
  }
  Serial.println("Peripheral disconnected");
}
