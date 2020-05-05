#include <ArduinoJson.h>
#include <WebServer.h>
#include <NeoPixelSegmentBus.h>
#include <NeoPixelBrightnessBus.h>
#include <NeoPixelBus.h>
#include <NeoPixelAnimator.h>
#include <WiFi.h>
#include <WiFiUdp.h>
#include <iostream>
#include <string>
#define NUM_LED 600
#define DATA_PIN 0
NeoPixelBus<NeoGrbFeature, Neo800KbpsMethod> strip(NUM_LED, DATA_PIN);

const char* SSID = "kouheki";
const char* PASSWD = "kouheki0000";
#define port 10004
int to_port = 11004;
IPAddress ip(192, 168, 0, 124);


IPAddress gateway(192,168, 0, 1);
IPAddress subnet(255, 255, 255, 0);
IPAddress DNS(192, 168, 0, 90); 
char *to_ip = "192.168.0.120";


WiFiUDP udp;
WiFiServer server(port);
void setup(){
  strip.Begin();
  allOff();
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
      rcv_video(msg);
    }
    else if(msg.startsWith("/init/")){
      msg.replace("/init/", "");
      rcv_init(msg);
      send_vrf();
    }
  }
}

void prnt(String str = "", int i = 0){
  if(str != ""){
  }
  if(i != 0){
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
    strip.SetPixelColor(i, RgbColor(0, 0, 0));
  }
  strip.Show();
}

void rcv_init(String msg){
  if(msg == "off"){
    allOff();
  }
  else{
    on_init(msg);
  }
  strip.Show();
}

void rcv_video(String msg){
  if(msg == "off"){
    allOff();
  }
  else{
    on_video(msg);
  }
  strip.Show();
}

void on_init(String msg){
  const size_t capacity = JSON_ARRAY_SIZE(1024);
  DynamicJsonDocument doc(capacity);
  deserializeJson(doc, msg);
  for(int i = 0; i < doc.size(); i++){
    int num = doc[i];
    strip.SetPixelColor(num, RgbColor(7, 7, 7));
  }
}

void on_video(String msg){
  const size_t capacity = JSON_ARRAY_SIZE(2048);
  DynamicJsonDocument doc(capacity);
  deserializeJson(doc, msg);
  for(int i = 0; i < doc.size(); i += 2){
    int num = doc[i];
    int r = doc[i+1][0];
    int g = doc[i+1][1];
    int b = doc[i+1][2];
    strip.SetPixelColor(num, RgbColor((int)(r/2), (int)(g/2), (int)(b/2)));
  }
}
