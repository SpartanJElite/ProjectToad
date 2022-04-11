#include <AccelStepper.h>
#include <WiFiNINA.h>
#include <WiFiUdp.h>


int status = WL_IDLE_STATUS;
#include "arduino_secrets.h" 
///////please enter your sensitive data in the Secret tab/arduino_secrets.h
char ssid[] = SECRET_SSID;        // your network SSID (name)
char pass[] = SECRET_PASS;    // your network password (use for WPA, or use as key for WEP)
int keyIndex = 0;            // your network key index number (needed only for WEP)

unsigned int localPort = 2390;      // local port to listen on

char packetBuffer[UDP_TX_PACKET_MAX_SIZE]; //buffer to hold incoming packet
float encoder = 0;
char relyBuffer[UDP_TX_PACKET_MAX_SIZE] = "100.0";
int encoderOrTime = 1;

WiFiUDP Udp;
 
//User-defined values
long receivedSteps = 0; //Number of steps
long receivedSpeed = 0; //Steps / second
long receivedAcceleration = 0; //Steps / second^2
char receivedCommand;
//-------------------------------------------------------------------------------
int directionMultiplier = 1; // = 1: positive direction, = -1: negative direction
bool newData, runallowed = false; // booleans for new data from serial, and runallowed flag
AccelStepper stepper(1, 8, 9);// direction Digital 9 (CCW), pulses Digital 8 (CLK)
 
void setup()
{

    
    Serial.begin(9600); //define baud rate

    // check for the WiFi module:
    if (WiFi.status() == WL_NO_MODULE) {
      Serial.println("Communication with WiFi module failed!");
      // don't continue
      while (true);
    }
  
    String fv = WiFi.firmwareVersion();
    if (fv < WIFI_FIRMWARE_LATEST_VERSION) {
      Serial.println("Please upgrade the firmware");
    }
  
    // attempt to connect to WiFi network:
    while (status != WL_CONNECTED) {
      Serial.print("Attempting to connect to SSID: ");
      Serial.println(ssid);
      // Connect to WPA/WPA2 network. Change this line if using open or WEP network:
      status = WiFi.begin(ssid, pass);
  
      // wait 10 seconds for connection:
      delay(1000);
    }
    Serial.println("Connected to WiFi");
    printWifiStatus();
  
    Serial.println("\nStarting connection to server...");
    // if you get a connection, report back via serial:
    Udp.begin(localPort);
    
    WiFiUDP Udp;
    
    Serial.println("Demonstration of AccelStepper Library"); //print a messages
    Serial.println("Send 'C' for printing the commands.");
 
    //setting up some default values for maximum speed and maximum acceleration
    Serial.println("Default speed: 400 steps/s, default acceleration: 800 steps/s^2.");
    stepper.setMaxSpeed(400); //SPEED = Steps / second
    stepper.setAcceleration(800); //ACCELERATION = Steps /(second)^2
 
    stepper.disableOutputs(); //disable outputs
}
 
void loop()
{
    // if there's data available, read a packet
    int packetSize = Udp.parsePacket();

    if(packetSize){
      Udp.read(packetBuffer, UDP_TX_PACKET_MAX_SIZE);
      String datReq(packetBuffer);
      Serial.println(datReq);
      receivedSteps = datReq.toFloat();
      receivedSpeed = 400;
      RotateRelative();
      memset(packetBuffer,0,UDP_TX_PACKET_MAX_SIZE);
      // send a reply, to the IP address and port that sent us the packet we received
      Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
      encoder = stepper.currentPosition();
      String temp(encoder);
      temp.toCharArray(relyBuffer,UDP_TX_PACKET_MAX_SIZE);
      Udp.write(relyBuffer);
      Udp.endPacket();
    }else{
      stepper.disableOutputs();
    }
 
}
 
 
void RunTheMotor() //function for the motor
{
    if (runallowed == true)
    {
        stepper.enableOutputs(); //enable pins
        stepper.run(); //step the motor (this will step the motor by 1 step at each loop)  
    }
    else //program enters this part if the runallowed is FALSE, we do not do anything
    {
        stepper.disableOutputs(); //disable outputs
        return;
    }
}

void RotateRelative()
{
    //We move X steps from the current position of the stepper motor in a given direction.
    //The direction is determined by the multiplier (+1 or -1)
   
    runallowed = true; //allow running - this allows entering the RunTheMotor() function.
    stepper.setMaxSpeed(receivedSpeed); //set speed
    stepper.move(directionMultiplier * receivedSteps); //set relative distance and direction
    RunTheMotor();
}

void printWifiStatus() {
  // print the SSID of the network you're attached to:
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your board's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  // print the received signal strength:
  long rssi = WiFi.RSSI();
  Serial.print("signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");
 }
