#include <ArduinoJson.h>
#include <WebServer.h>
#include <FastLED.h>
#include <WiFi.h>
#include <WiFiUdp.h>
#include <iostream>
#include <string>
// const char* SSID = "Buffalo-G-6110";
// const char* PASSWD = "17709934";
// const char* SSID = "SIAF-FREE-WiFi";
// const char* PASSWD = "siafsiaf";
#define NUM_LED 600
#define DATA_PIN 0
CRGB leds[NUM_LED];

const char* SSID = "kouheki";
const char* PASSWD = "kouheki0000";
#define port 10001
int to_port = 11001;
IPAddress ip(192, 168, 0, 121);


IPAddress gateway(192,168, 0, 1);
IPAddress subnet(255, 255, 255, 0);
IPAddress DNS(192, 168, 0, 90); 
char *to_ip = "192.168.0.120";

WiFiUDP udp;
WiFiServer server(port);
void setup(){
  Serial.begin(115200);
  FastLED.addLeds<WS2812B, DATA_PIN>(leds, NUM_LED);
  FastLED.setBrightness(128);
  allOff();
  wifi_connect(SSID, PASSWD);
  WiFi.mode(WIFI_STA);
  udp.begin(port);
  Serial.println("Server started");
}

//疑似OSCのチェック
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
      rcv_video(msg);
    }
    else if(msg.startsWith("/init/")){
      msg.replace("/init/", "");
      Serial.println(msg);
      rcv_init(msg);
      send_vrf();
    }
  }
}

void prnt(String str = "", int i = 0){
  if(str != ""){
    Serial.println(str);
  }
  if(i != 0){
    Serial.println(i);
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

void send_vrf(){
  udp.beginPacket(to_ip, to_port);
  udp.write('1');
  udp.endPacket();  
}

void allOff(){
  for(int i = 0; i < NUM_LED; i++){
    leds[i] = 0x000000;
  }
  FastLED.show();
}

void rcv_init(String msg){
  if(msg == "off"){
    allOff();
  }
  else{
    on_init(msg);
  }
  FastLED.show();
}

void rcv_video(String msg){
  if(msg == "off"){
    allOff();
  }
  else{
    on_video(msg);
  }
  FastLED.show();
}

void on_init(String msg){
  const size_t capacity = JSON_ARRAY_SIZE(1024);
  DynamicJsonDocument doc(capacity);
  deserializeJson(doc, msg);
  Serial.println(measureMsgPack(doc));
  for(int i = 0; i < doc.size(); i++){
    int num = doc[i];
    leds[num] = 0x0e0e0e;
  }
}

void on_video(String msg){
  const size_t capacity = JSON_ARRAY_SIZE(1125);
  DynamicJsonDocument doc(capacity);
  deserializeJson(doc, msg);
  for(int i = 0; i < doc.size(); i += 2){
    int num = doc[i];
    int r = doc[i+1][0];
    int g = doc[i+1][1];
    int b = doc[i+1][2];
    Serial.print("R: ");Serial.print(r);Serial.print(" G: "); Serial.print(g);Serial.print(" B: "); Serial.println(b);
    leds[num] = CRGB(r, g, b);
  }
}