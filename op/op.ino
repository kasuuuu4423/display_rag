//WIFI&OSC
#include <WiFi.h>
#include <WiFiUdp.h>
#include <OSCMessage.h>

//fastLED
#include <FastLED.h>
#define LED_PIN     0
#define LED_PIN_2     5
#define LED_PIN_3     13
#define LED_PIN_4     14
#define COLOR_ORDER GRB
#define CHIPSET     WS2812
#define NUM_LEDS    600
#define BRIGHTNESS  128
#define FRAMES_PER_SECOND 60

CRGB leds[NUM_LEDS];
CRGB leds_2[NUM_LEDS];
CRGB leds_3[NUM_LEDS];
CRGB leds_4[NUM_LEDS];


const char ssid[] = "Buffalo-G-6110";
const char pass[] = "17709934";
//const char ssid[] = "S_HOUSE_WI-FI_2.4G";
//const char pass[] = "s8r2621ya66tm";
//const char ssid[] = "baka";
//const char pass[] = "12341234";
//const char ssid[] = "gagaopi";
//const char pass[] = "penipeni";
//const char ssid[] = "aterm-358916-gw";
//const char pass[] = "164fd0997b4b0";

// A UDP instance to let us send and receive packets over UDP
WiFiUDP Udp;
const unsigned int localPort = 8888;


OSCErrorCode error;
void setup() {
  Serial.begin(115200);

  wifi_connect();
  udp();
  FastLED.addLeds<CHIPSET, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection( TypicalLEDStrip );
  FastLED.addLeds<CHIPSET, LED_PIN_2, COLOR_ORDER>(leds_2, NUM_LEDS).setCorrection( TypicalLEDStrip );
  FastLED.addLeds<CHIPSET, LED_PIN_3, COLOR_ORDER>(leds_3, NUM_LEDS).setCorrection( TypicalLEDStrip );
  FastLED.addLeds<CHIPSET, LED_PIN_4, COLOR_ORDER>(leds_4, NUM_LEDS).setCorrection( TypicalLEDStrip );
  FastLED.setBrightness( BRIGHTNESS );
}



void loop() {
 OSCMessage msg;
  int size = Udp.parsePacket();

  if (size > 0) {
    while (size--) {
      msg.fill(Udp.read());
    }
    msg.dispatch("/led", led);
    msg.dispatch("/led_2", led_2);
    msg.dispatch("/led_3", led_3);
    msg.dispatch("/led_4", led_4);
    msg.dispatch("/init", init);
    msg.dispatch("/init_2", init_2);
    msg.dispatch("/init_3", init_3);
    msg.dispatch("/init_4", init_4);
  }
}


void led(OSCMessage &msg) {
  int msg_size = msg.size();
  for(int i=0;i<msg_size/2;i++){
    color(leds, msg.getInt(i*2), msg.getInt(i*2+1));
  }
  FastLED.show();
}
void led_2(OSCMessage &msg) {
  int msg_size = msg.size();
  for(int i=0;i<msg_size/2;i++){
    color(leds_2, msg.getInt(i*2), msg.getInt(i*2+1));
  }
  FastLED.show();
}
void led_3(OSCMessage &msg) {
  int msg_size = msg.size();
  for(int i=0;i<msg_size/2;i++){
    color(leds, msg.getInt(i*2), msg.getInt(i*2+1));
  }
  FastLED.show();
}
void led_4(OSCMessage &msg) {
  int msg_size = msg.size();
  for(int i=0;i<msg_size/2;i++){
    color(leds_2, msg.getInt(i*2), msg.getInt(i*2+1));
  }
  FastLED.show();
}


void color(CRGB rin[], int pixel, int color_num){
   switch( color_num ){
    case 0:
      setPixel(rin,pixel,0,0,0);
      break;
    case 1:
      setPixel(rin,pixel,128,0,0);
      break;
    case 2:
      setPixel(rin,pixel,0,128,0);
      break;
    case 3:
      setPixel(rin,pixel,0,0,128);
      break;
    case 4:
      setPixel(rin,pixel,128,128,0);
      break;
    case 5:
      setPixel(rin,pixel,0,128,128);
      break;
    case 6:
      setPixel(rin,pixel,128,0,128);
      break;
    case 7:
      setPixel(rin,pixel,128,128,128);
      break;
    case 8:
      setPixel(rin,pixel,255,0,0);
      break;
    case 9:
      setPixel(rin,pixel,0,255,0);
      break;
    case 10:
      setPixel(rin,pixel,0,0,255);
      break;
    case 11:
      setPixel(rin,pixel,255,255,0);
      break;
    case 12:
      setPixel(rin,pixel,0,255,255);
      break;
    case 13:
      setPixel(rin,pixel,255,0,255);
      break;
    case 14:
      setPixel(rin,pixel,255,255,255);
      break;
    case 15:
      setPixel(rin,pixel,0,128,255);
      break;
    case 16:
      setPixel(rin,pixel,0,255,128);
      break;
    case 17:
      setPixel(rin,pixel,255,128,0);
      break;
    case 18:
      setPixel(rin,pixel,128,255,0);
      break;
    case 19:
      setPixel(rin,pixel,128,0,255);
      break;
    case 20:
      setPixel(rin,pixel,255,0,128);
      break;
    case 21:
      setPixel(rin,pixel,128,128,255);
      break;
    case 22:
      setPixel(rin,pixel,128,255,128);
      break;
    case 23:
      setPixel(rin,pixel,255,128,128);
      break;
    case 24:
      setPixel(rin,pixel,255,128,255);
      break;
    case 25:
      setPixel(rin,pixel,255,255,128);
      break;
    case 26:
      setPixel(rin,pixel,128,255,255);
      break;

    //0, 128, 255
    //0~83, 84~167, 168~255
  }
}


void init(OSCMessage &msg) {
  int led_num = msg.getInt(0);
  if(led_num == 0){
    allZero(leds);
    allZero(leds_2);
    allZero(leds_3);
    allZero(leds_4);
  }
  int onoff = msg.getInt(1);
  if(onoff == 1){
    setPixelWhite(leds, led_num);
  }else if(onoff == 0){
    allZero(leds);
  }
  FastLED.show();
}
void init_2(OSCMessage &msg) {
  int led_num = msg.getInt(0);
  if(led_num == 600){
    allZero(leds);
    allZero(leds_2);
    allZero(leds_3);
    allZero(leds_4);
  }
  int onoff = msg.getInt(1);
  if(onoff == 1){
    setPixelWhite(leds_2, led_num);
  }else if(onoff == 0){
    allZero(leds_2);
  }
  FastLED.show();
}
void init_3(OSCMessage &msg) {
  int led_num = msg.getInt(0);
  if(led_num == 1800){
    allZero(leds);
    allZero(leds_2);
    allZero(leds_2);
    allZero(leds_2);
  }
  int onoff = msg.getInt(1);
  if(onoff == 1){
    setPixelWhite(leds_3, led_num);
  }else if(onoff == 0){
    allZero(leds_3);
  }
  FastLED.show();
}
void init_4(OSCMessage &msg) {
  int led_num = msg.getInt(0);
  if(led_num == 2400){
    allZero(leds);
    allZero(leds_2);
    allZero(leds_3);
    allZero(leds_4);
  }
  int onoff = msg.getInt(1);
  if(onoff == 1){
    setPixelWhite(leds_4, led_num);
  }else if(onoff == 0){
    allZero(leds_4);
  }
  FastLED.show();
}


void setPixelWhite(CRGB rin[], int num){
  rin[num].r = 20;
  rin[num].g = 20;
  rin[num].b = 20;
}


void setPixelZero(CRGB rin[], int num){
  rin[num].r = 0;
  rin[num].g = 0;
  rin[num].b = 0;
}


void allZero(CRGB rin[]){
  for(int i=0;i<NUM_LEDS;i++){
    rin[i].r = 0;
    rin[i].g = 0;
    rin[i].b = 0;
  }
}


void setPixel(CRGB rin[], int Pixel, int red, int green, int blue) {
  rin[Pixel].r = red;
  rin[Pixel].g = green;
  rin[Pixel].b = blue;
}


void wifi_connect(){
  // Connect to WiFi network
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, pass);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}


void udp(){
  delay(3000);
  Serial.println("Starting UDP");
  Udp.begin(localPort);
  Serial.println("Local port: ");
  Serial.println(localPort);
}
