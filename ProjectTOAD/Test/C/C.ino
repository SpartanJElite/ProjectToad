/*
  This example creates a BLE central that scans for a peripheral with a Environmental Sensing Service (ESS).
  If that contains temperature and humidity characteristics the values are displayed.

  The circuit:
  - Arduino Nano 33 BLE or Arduino Nano 33 IoT board.

  This example code is in the public domain.
*/

#include <ArduinoBLE.h>

//----------------------------------------------------------------------------------------------------------------------
// BLE UUIDs
//----------------------------------------------------------------------------------------------------------------------

// https://www.bluetooth.com/specifications/assigned-numbers/environmental-sensing-service-characteristics/

#define BLE_UUID_ENVIRONMENTAL_SENSING_SERVICE    "181A"
#define BLE_UUID_TEMPERATURE                      "2A6E"
#define BLE_UUID_HUMIDITY                         "2A6F"

void setup()
{
  Serial.begin( 9600 );
  while ( !Serial );

  BLE.begin();

  BLE.scanForUuid( BLE_UUID_ENVIRONMENTAL_SENSING_SERVICE );
} // setup


void loop()
{
  static long previousMillis = 0;

  long interval = 5000;
  unsigned long currentMillis = millis();
  
  if ( currentMillis - previousMillis > interval )
  {
    previousMillis = currentMillis;
   
    
    BLEDevice peripheral = BLE.available();

    if ( peripheral )
    {
      if ( peripheral.localName() != "Arduino Nano 33 BLE" )
      {
        return;
      }

      BLE.stopScan();

      explorePeripheral( peripheral );

      BLE.scanForUuid( BLE_UUID_ENVIRONMENTAL_SENSING_SERVICE );
    }
  }
} // loop


bool explorePeripheral( BLEDevice peripheral )
{
  if ( !peripheral.connect() )
  {
    Serial.println("DID NOT CONNECT");
    return false;
  }

  if ( !peripheral.discoverAttributes() )
  {
    Serial.println("FUCK YOU");
    peripheral.disconnect();
    return false;
  }

  BLECharacteristic temperatureCharacterisic = peripheral.characteristic( BLE_UUID_TEMPERATURE );
  if ( temperatureCharacterisic )
  {
    int16_t temperature;
    temperatureCharacterisic.readValue( temperature );
    Serial.print( "Temperature: " );
    Serial.print( temperature / 100.0 );
    Serial.println( "°C" );
  }

  BLECharacteristic humidityCharacterisic = peripheral.characteristic( BLE_UUID_HUMIDITY );
  if ( humidityCharacterisic )
  {
    uint16_t humidity;
    humidityCharacterisic.readValue( humidity );
    Serial.print( "Humidity: " );
    Serial.print( humidity / 100.0 );
    Serial.println( "%" );
  }

  peripheral.disconnect();
  return true;
} // explorePeripheral
