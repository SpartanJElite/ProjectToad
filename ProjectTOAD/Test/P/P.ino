/*
  This example creates a BLE peripheral with a Environmental Sensing Service (ESS)
  that contains a temperature and a humidity characteristic.
  The yellow LED shows the BLE module is initialized.
  The green LED shows RSSI of zero. The more it blinks the worse the connection.

  The circuit:
  - Arduino Nano 33 BLE Sense board.

  You can use a generic BLE central app, like LightBlue (iOS and Android) or
  nRF Connect (Android), to interact with the services and characteristics
  created in this sketch.

  This example code is in the public domain.
*/

#include <ArduinoBLE.h>
//#include <Arduino_HTS221.h>

//----------------------------------------------------------------------------------------------------------------------
// BLE UUIDs
//----------------------------------------------------------------------------------------------------------------------

// https://www.bluetooth.com/specifications/assigned-numbers/environmental-sensing-service-characteristics/

#define BLE_UUID_ENVIRONMENTAL_SENSING_SERVICE    "181A"
#define BLE_UUID_TEMPERATURE                      "2A6E"
#define BLE_UUID_HUMIDITY                         "2A6F"

//----------------------------------------------------------------------------------------------------------------------
// BLE
//----------------------------------------------------------------------------------------------------------------------

BLEService environmentalSensingService( BLE_UUID_ENVIRONMENTAL_SENSING_SERVICE );
BLEShortCharacteristic temperatureCharacteristic( BLE_UUID_TEMPERATURE, BLERead | BLENotify );
BLEUnsignedShortCharacteristic humidityCharacteristic( BLE_UUID_HUMIDITY, BLERead | BLENotify );

//const int BLE_LED_PIN = LED_BUILTIN;
//const int RSSI_LED_PIN = LED_PWR;


void setup()
{
  Serial.begin( 9600 );
  // while ( !Serial );

  //pinMode( BLE_LED_PIN, OUTPUT );
  //pinMode( RSSI_LED_PIN, OUTPUT );

  // Without Serial when using USB power bank HTS sensor seems to needs some time for setup
  delay( 10 );

  //  if ( !HTS.begin() )
  //  {
  //    Serial.println( "Failed to initialize Humidity Temperature Sensor!" );
  //    while ( 1 )
  //    {
  //      digitalWrite( BLE_LED_PIN, HIGH );
  //      delay(100);
  //      digitalWrite( BLE_LED_PIN, LOW );
  //      delay(1000);
  //    }
  //  }

  if ( setupBleMode() )
  {
    //digitalWrite( BLE_LED_PIN, HIGH );
  }
} // setup


void loop()
{
  static long previousMillis = 0;

  // listen for BLE peripherals to connect:
  BLEDevice central = BLE.central();
  Serial.println("Here");
  if ( central )
  {
    Serial.print( "Connected to central: " );
    Serial.println( central.address() );
    
    while ( central.connected() )
    {
      long interval = 1000;
      unsigned long currentMillis = millis();
      if ( currentMillis - previousMillis > interval )
      {
        previousMillis = currentMillis;

        Serial.print( "Central RSSI: " );
        Serial.println( central.rssi() );

        if ( central.rssi() != 0 )
        {
          //digitalWrite( RSSI_LED_PIN, LOW );

          // BLE defines Temperature UUID 2A6E Type sint16
          // Unit is in degrees Celsius with a resolution of 0.01 degrees Celsius
          int16_t temperature = round( 1 * 100.0 );
          temperatureCharacteristic.writeValue( temperature );

          // BLE defines Humidity UUID 2A6F Type uint16
          // Unit is in percent with a resolution of 0.01 percent
          uint16_t humidity = round( 1 * 100.0 );
          humidityCharacteristic.writeValue( humidity );
        }
        else
        {
          //digitalWrite( RSSI_LED_PIN, HIGH );
        }
      } // intervall
    } // while connected

    Serial.print( F( "Disconnected from central: " ) );
    Serial.println( central.address() );
  } // if central
} // loop



bool setupBleMode()
{
//  if ( !BLE.begin() )
//  {
//    return false;
//  }

  // set advertised local name and service UUID:
  BLE.setDeviceName( "Arduino Nano 33 BLE" );
  BLE.setLocalName( "Arduino Nano 33 BLE" );
  BLE.setAdvertisedService( environmentalSensingService );

  // BLE add characteristics
  environmentalSensingService.addCharacteristic( temperatureCharacteristic );
  environmentalSensingService.addCharacteristic( humidityCharacteristic );

  // add service
  BLE.addService( environmentalSensingService );

  // set the initial value for the characeristic:
  temperatureCharacteristic.writeValue( 0 );
  humidityCharacteristic.writeValue( 0 );

  // start advertising
  BLE.advertise();

  return true;
}
