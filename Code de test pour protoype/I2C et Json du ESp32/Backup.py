#include <Wire.h> 
#include <Arduino.h>
#include <WiFi.h>
#include <string.h>
#include <time.h>

#define SLAVE_ADDR 0x0a  // Adresse de l'esclave 

void requestData();

// Tableau de données à envoyer au maître 
char dataToSend[] = "Bonjour Master!"; 
char charToSend[100] = "";
 
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
String stringOfAllData = "";

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
    delay(500);
  }
  Serial.println(WiFi.localIP());
}

void setup() { 

  // Initialisation du port série pour le debug 
  Serial.begin(115200); 

  // Initialisation de l'I2C en tant qu'esclave avec l'adresse définie 
  Wire.setPins(17, 18);
  Wire.begin(SLAVE_ADDR); 

  // Attacher une fonction de demande (request) pour le maître 
  Wire.onRequest(requestData); 

  Serial.println("Slave prêt, en attente de requêtes du maître..."); 

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
  
  /*while(true)
  {
    sw1State = digitalRead(sw1Pin);
    sw2State = digitalRead(sw2Pin);
    btn1State = digitalRead(btn1Pin);

    if (sw1State == digitalRead(sw1Pin) && sw2State == digitalRead(sw2Pin) && btn1State == digitalRead(btn1Pin))
      	break;
  }


  String stringOfInteractable = "{\"" + sw1Name + "\":\"" + sw1State + "\",\"" 
                                    + sw2Name + "\":\"" + sw2State + "\",\"" 
                                    + btn1Name + "\":\"" + btn1State +"\"}";

  stringOfAllData = "{\"timestamp\":" + String(getTime()) + ",\"NomEsp32\":\"" + myName + "\",\"JsonData\":" + stringOfInteractable + "}";

  for (int i = 0; i < 100; i++) {
    charToSend[i] = stringOfAllData[i];
    Serial.print(charToSend[i]);
    Serial.print(" ");
  }


  delay(10);

  sw1State = digitalRead(sw1Pin);
  sw2State = digitalRead(sw2Pin);
  btn1State = digitalRead(btn1Pin);*/
} 

 
// Fonction appelée lorsque le maître demande des données 

void requestData() { 

  sw1State = digitalRead(sw1Pin);
  sw2State = digitalRead(sw2Pin);
  btn1State = digitalRead(btn1Pin);

  String stringOfInteractable = "{\"" + sw1Name + "\":\"" + sw1State + "\",\"" 
                                      + sw2Name + "\":\"" + sw2State + "\",\"" 
                                      + btn1Name + "\":\"" + btn1State +"\"}";
  stringOfAllData = "{\"timestamp\":" + String(getTime()) 
                   + ",\"NomEsp32\":\"" + myName 
                   + "\",\"JsonData\":" + stringOfInteractable + "}";

  // Envoyer les données du tableau `dataToSend` au maître 
  for (int i = 0; i < stringOfAllData.length(); i++) { 
    Wire.write(stringOfAllData[i]);  // Envoyer chaque caractère 
  }
  Wire.write(0x00);  // Envoyer chaque caractère 

  /*Serial.println("request");
  // Envoyer les données du tableau `dataToSend` au maître 
  Serial.println(sizeof(charToSend));
  for (int i = 0; i < sizeof(charToSend); i++) { 
    Serial.println(charToSend[i]);
    Wire.write(charToSend[i]);  // Envoyer chaque caractère 
  } */
  // Vous pouvez aussi envoyer d'autres types de données comme des entiers, des flottants, etc. 

} 