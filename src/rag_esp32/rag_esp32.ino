#include <ArduinoJson.h>
#include <WebServer.h>
#include <FastLED.h>
#include <WiFi.h>
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

void setup(){
  Serial.begin(115200);
  FastLED.addLeds<WS2812B, DATA_PIN>(leds, NUM_LED);
  FastLED.setBrightness(255);
  wifi_connect(SSID, PASSWD);
  server.begin();
  Serial.println("Server started");
}

void loop() {
  WiFiClient client = server.available();
  String msg;
  if (client.connected()) {
    //Serial.println("Connected to client");
    msg = client.readStringUntil('\r');
    // Serial.print("[");
    Serial.print(msg);
    // Serial.println("]");
    if(msg == "off"){
      allOff();
    }
    else{
      on_init(msg);
    }
    FastLED.show();
    client.print("1");
    client.stop();
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

void on_init(String msg){
  const size_t capacity = JSON_ARRAY_SIZE(1024);
  DynamicJsonDocument doc(capacity);
  deserializeJson(doc, msg);
  Serial.println(sizeof(doc));
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

void allOff(){
  for(int i = 0; i < NUM_LED; i++){
    leds[i] = 0x000000;
  }
}