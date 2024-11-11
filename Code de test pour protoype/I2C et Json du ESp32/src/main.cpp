/*********
  Rui Santos
  Complete project details at https://randomnerdtutorials.com  
*********/
#include <Arduino.h>
#include <Wire.h>
#include <WiFi.h>
#include <string.h>
#include <ArduinoJson.h>
#include <time.h>
#include <chrono>

#define I2C_DEV_ADDR 0x08


// NTP server to request epoch time
const char* ntpServer = "pool.ntp.org";

// Replace with your network credentials
const char* ssid = "m";
const char* password = "12345678";

uint32_t i = 0;

bool sw1State = 0;
bool sw2State = 0;
bool btn1State = 0;

const int sw1Pin = 7;
const int sw2Pin = 15;
const int btn1Pin = 16;

String sw1Name = "sw1";
String sw2Name = "sw2";
String btn1Name = "btn1";

String myName = "enigmeTest1";

const char *mqtt_broker = "broker.emqx.io";
const char *topic = "emqx/esp32";
const char *mqtt_username = "emqx";
const char *mqtt_password = "public";
const int mqtt_port = 1883;

unsigned long getTime() {
  time_t now;
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)) {
    Serial.println("Failed to obtain time");
    return(0);
  }
  time(&now);
  return now;
}

// Initialize WiFi
void initWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi ..");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print('.');
    delay(1000);
  }
  Serial.println(WiFi.localIP());
}

void setup() {
  Serial.begin(115200);
  Wire.setPins(8,9);
  Wire.begin();
  pinMode(sw1Pin, INPUT);
  pinMode(sw2Pin, INPUT);
  pinMode(btn1Pin, INPUT);

  sw1State = digitalRead(sw1Pin);
  sw2State = digitalRead(sw2Pin);
  btn1State = digitalRead(btn1Pin);
  initWiFi();
  configTime(0, 0, ntpServer);
}

void loop() {

  while(sw1State == digitalRead(sw1Pin) && sw2State == digitalRead(sw2Pin) && btn1State == digitalRead(btn1Pin))
  {
    sw1State = digitalRead(sw1Pin);
    sw2State = digitalRead(sw2Pin);
    btn1State = digitalRead(btn1Pin);
  }
  String stringOfAllData = "";

  String stringOfInteractable = "{\"" + sw1Name + "\":\"" + sw1State + "\",\"" 
                                    + sw2Name + "\":\"" + sw2State + "\",\"" 
                                    + btn1Name + "\":\"" + btn1State +"\"}";

  stringOfAllData = "{\"timestamp\":" + String(getTime()) + ",\"NomEsp32\":\"" + myName + "\",\"JsonData\":" + stringOfInteractable + "}";

  Serial.println(stringOfAllData);

  delay(10);

  sw1State = digitalRead(sw1Pin);
  sw2State = digitalRead(sw2Pin);
  btn1State = digitalRead(btn1Pin);



// Write message to the slave
Wire.beginTransmission(I2C_DEV_ADDR);
Wire.printf("Hello World! %lu", i++);
uint8_t error = Wire.endTransmission(true);
Serial.printf("endTransmission: %u\n", error);

// Read 16 bytes from the slave
uint8_t bytesReceived = Wire.requestFrom(I2C_DEV_ADDR, 16);

Serial.printf("requestFrom: %u\n", bytesReceived);
if ((bool)bytesReceived) {  //If received more than zero bytes
  uint8_t temp[bytesReceived];
  Wire.readBytes(temp, bytesReceived);
  log_print_buf(temp, bytesReceived);
  }
}

