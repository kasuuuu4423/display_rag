#include <ArduinoJson.h>
#include <WebServer.h>
#include <FastLED.h>
#include <WiFi.h>
#include <WiFiUdp.h>
// const char* SSID = "Buffalo-G-6110";
// const char* PASSWD = "17709934";
// const char* SSID = "SIAF-FREE-WiFi";
// const char* PASSWD = "siafsiaf";
const char* SSID = "kouheki";
const char* PASSWD = "kouheki0000";
WiFiServer server(37564);

#define NUM_LED 600
#define DATA_PIN 0
CRGB leds[NUM_LED];

WiFiUDP udp;

char *to_ip = "192.168.0.124";
int to_port = 18782;

void setup(){
  Serial.begin(115200);
  FastLED.addLeds<WS2812B, DATA_PIN>(leds, NUM_LED);
  FastLED.setBrightness(255);
  allOff();
  wifi_connect(SSID, PASSWD);
  WiFi.mode(WIFI_STA);
  udp.begin(37564);
  Serial.println("Server started");
}

//疑似OSCのチェック
void loop() {
  char packetBuffer[512];
  int packetSize = udp.parsePacket();
  if(packetSize){
    int len = udp.read(packetBuffer, packetSize);
    if (len > 0) packetBuffer[len] = '\0';
    String msg = packetBuffer;
    if(msg.startsWith("/video/")){
      msg = msg.replace("/video/", "");
      rcv_video(msg);
    }
    else if(msg.startsWith("/init/")){
      msg = msg.replace("/init/", "");
      rcv_init(msg);
      send_vrf();
    }
  }
}

void wifi_connect(const char* ssid, const char* password){
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

void rcv_init(msg){
  if(msg == "off"){
    allOff();
  }
  else{
    on_init(msg);
  }
  FastLED.show();
}

void rcv_video(msg){
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
  for(int i = 0; i < 64; i++){
    int num = doc[i];
    if(i == sizeof(doc) - 1){
      Serial.println(num);
    }
    else{
      Serial.print(num);
      Serial.print(",");
    }
    leds[num] = 0xffffff;
  }
}

//measureMsgPack(doc)のチェック
//on_init()でやると良い
void on_video(){
  const size_t capacity = JSON_ARRAY_SIZE(1125);
  DynamicJsonDocument doc(capacity);
  deserializeJson(doc, msg);
  for(int i = 0; i < measureMsgPack(doc); i += 2){
    int num = doc[i];
    int color = doc[i+1]
    leds[num] = color;
  }
}