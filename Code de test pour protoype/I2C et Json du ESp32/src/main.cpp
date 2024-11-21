#include <Wire.h> 
#include <Arduino.h>
#include <string.h>
#include <time.h>

#define SLAVE_ADDR 0x0a  // Adresse de l'esclave 

void requestData();

uint32_t i = 0;

int oldTime = millis();

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
} 
 

void loop() { 
} 

 
// Fonction appelée lorsque le maître demande des données 

void requestData() { 

  
  Serial.println(oldTime - millis());
  oldTime = millis();

  sw1State = digitalRead(sw1Pin);
  sw2State = digitalRead(sw2Pin);
  btn1State = digitalRead(btn1Pin);

  String stringOfInteractable = "{\"" + sw1Name + "\":\"" + sw1State + "\",\"" 
                                      + sw2Name + "\":\"" + sw2State + "\",\"" 
                                      + btn1Name + "\":\"" + btn1State +"\"}";
  stringOfAllData = "{\"NomEsp32\":\"" + myName 
                   + "\",\"JsonData\":" + stringOfInteractable + "}";

  // Envoyer les données du tableau `dataToSend` au maître 
  for (int i = 0; i < stringOfAllData.length(); i++) { 
    Wire.write(stringOfAllData[i]);  // Envoyer chaque caractère 
  }
  Wire.write(0x00);  // Le PI repete le dernier byte recu, donc le dernier byte est NULL
} 