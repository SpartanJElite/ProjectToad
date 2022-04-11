int A = 12;
int B = 11;
int I = 10;

float countTick = 0;
float countIndex = 0;
float precTick = 0;
float precIndex = 0;
float tick = 0;
float tickB = 0;
float index = 0;

#include <SPI.h>
#include <WiFiNINA.h>
#include <WiFiUdp.h>
#include <Servo.h>
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
Servo myServo;

void setup() {

  //Initialize serial and wait for port to open:
  Serial.begin(115200);
//  while (!Serial) {
//    ; // wait for serial port to connect. Needed for native USB port only
//  }
  
  pinMode(A, INPUT);
  pinMode(B, INPUT);
  pinMode(I, INPUT);

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

  myServo.attach(9);
  

}

void loop() {

  // if there's data available, read a packet
  int packetSize = Udp.parsePacket();
  
  if (packetSize) {
    // read the packet into packetBufffer
    float start = millis();
//    if(encoderOrTime == 1) {
      Udp.read(packetBuffer, UDP_TX_PACKET_MAX_SIZE);
      String datReq(packetBuffer);
      Serial.println(datReq);
      myServo.write(datReq.toFloat());
      memset(packetBuffer,0,UDP_TX_PACKET_MAX_SIZE);
      // send a reply, to the IP address and port that sent us the packet we received
      Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());

      tick = digitalRead(A);
  tickB = digitalRead(B);
  index = digitalRead(I);

  
  if(tick != precTick)
  {
    if(tick != tickB)
    {
      countTick = countTick + tick;
      precTick = tick;
    }
    else
    {
      countTick = countTick - tick;
      precTick = tick;
    }
    Serial.print("tick :");
    Serial.println(countTick);
  }
  
  if(index != precIndex)
  {
    if(countTick > 0)
    {
      countIndex = countIndex + index;
      precIndex = index;
    }
    else
    {
      countIndex = countIndex - index;
      precIndex = index;
    }
    countTick = 0;
    Serial.print("turn :");
    Serial.println(countIndex);
    
  }
      
//      encoder = encoderRead();
  encoder = countTick;
//      float start = millis();
      String temp(encoder);
      temp.toCharArray(relyBuffer,UDP_TX_PACKET_MAX_SIZE);
      Udp.write(relyBuffer);
      Udp.endPacket();
      

      
//    } else {
//      Udp.read(packetBuffer, UDP_TX_PACKET_MAX_SIZE);
//      String datReq(packetBuffer);
//      Serial.println(datReq);
//      myServo.write(datReq.toFloat());
//      memset(packetBuffer,0,UDP_TX_PACKET_MAX_SIZE);
//      Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
//      String temp2(start); 
//      temp2.toCharArray(relyBuffer,UDP_TX_PACKET_MAX_SIZE);
//      Udp.write(relyBuffer);
//      Udp.endPacket();
//
//    }
//    encoderOrTime *= -1;


  }else{
    //Serial.println("Outside loop");
  }
}


float encoderRead(){
  tick = digitalRead(A);
  tickB = digitalRead(B);
  index = digitalRead(I);

  
  if(tick != precTick)
  {
    if(tick != tickB)
    {
      countTick = countTick + tick;
      precTick = tick;
    }
    else
    {
      countTick = countTick - tick;
      precTick = tick;
    }
    Serial.print("tick :");
    Serial.println(countTick);
  }
  
  if(index != precIndex)
  {
    if(countTick > 0)
    {
      countIndex = countIndex + index;
      precIndex = index;
    }
    else
    {
      countIndex = countIndex - index;
      precIndex = index;
    }
    countTick = 0;
    Serial.print("turn :");
    Serial.println(countIndex);
    
  }
  return countTick;
  
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
