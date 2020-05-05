#include <ArduinoJson.h>
#include <WebServer.h>
#include <WiFi.h>
#include <WiFiUdp.h>
#include <string>
#include <SoftwareSerial.h>

#define numLeds1 600
#define numLeds2 600
#define numLeds3 600
#define numLeds4 600

const char* SSID = "kouheki";
const char* PASSWD = "kouheki0000";
#define port 10001
int to_port = 11001;
IPAddress ip(192, 168, 0, 121);

IPAddress gateway(192,168, 0, 1);
IPAddress subnet(255, 255, 255, 0);
IPAddress DNS(192, 168, 0, 90); 
const char *to_ip = "192.168.0.120";
WiFiUDP udp;
WiFiServer server(port);

SoftwareSerial serials[4];
int serial_pin[4][2];
serial_pin[0] = {0,2};
serial_pin[1] = {4,5};
serial_pin[2] = {12,13};
serial_pin[3] = {22,23};

void setup(){
  for(int i = 0; i < sizeof(serials); i++){
    serials[i].begin(115200, serial_pin[i][0], serial_pin[i][1], SWSERIAL_8N1, false, 256);
  }
  sendAllOff();
  wifi_connect(SSID, PASSWD);
  WiFi.mode(WIFI_STA);
  udp.begin(port);
}

void loop() {
  char packetBuffer[512];
  int packetSize = udp.parsePacket();
  if(packetSize){
    int len = udp.read(packetBuffer, packetSize);
    if(len > 0){
      packetBuffer[len] = '\0';
    }
    String msg = packetBuffer;
    if(msg.startsWith("/video/")){
      msg.replace("/video/", "");
    }
    else if(msg.startsWith("/init/")){
      msg.replace("/init/", "");
    }
  }
}

void send_rcv(){
  udp.beginPacket(to_ip, to_port);
  udp.write('1');
  udp.endPacket();  
}

void sendAllOff(){
  for(int i = 0; i < sizeof(serials); i++){
    serials[i].write(0x00);
  }
}

String sendPixVal(json){
  const size_t capacity = JSON_ARRAY_SIZE(2048);
  DynamicJsonDocument doc(capacity);
  deserializeJson(doc, msg);
  for(int i = 0; i < doc.size(); i += 2){
    int num = doc[i];
    int r = doc[i+1][0];
    int g = doc[i+1][1];
    int b = doc[i+1][2];
    sort(num, r, g, b);
  }
}

void sendInit(){
  const size_t capacity = JSON_ARRAY_SIZE(1024);
  DynamicJsonDocument doc(capacity);
  deserializeJson(doc, msg);
  for(int i = 0; i < doc.size(); i++){
    int num = i;
    int r = 128;
    int g = 128;
    int b = 128;
    sort(num, r, g, b);
  }
}

void sort(int num, int r, int g, int b){
  if(0 < num && num <= numLeds1){
    String msg = String(num) ',' + String(r) + ',' + String(g) + ',' + String(b);
    serial1.print(msg);
  }
  else if(numLeds1 < num && num <= numLeds1 + numLeds2){
    String msg = String(num - 600) ',' + String(r) + ',' + String(g) + ',' + String(b);
    serial2.print(msg);
  }
  else if(numLeds1 + numLeds2 < num && num <= numLeds1 + numLeds2 + numLeds3){
    String msg = String(num - 1200) ',' + String(r) + ',' + String(g) + ',' + String(b);
    serial3.print(msg);
  }
  else if(numLeds1 + numLeds2 + numLeds3 < num && num <= numLeds1 + numLeds2 + numLeds3 + numLeds4){
    String msg = String(num - 1800) ',' + String(r) + ',' + String(g) + ',' + String(b);
    serial4.print(msg);
  }
}

void wifi_connect(const char* ssid, const char* password){
  WiFi.config(ip, gateway, subnet, DNS);
  WiFi.begin(ssid, password);
  while(WiFi.status() != WL_CONNECTED){
    Serial.println(".");
    delay(100);
  }
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}