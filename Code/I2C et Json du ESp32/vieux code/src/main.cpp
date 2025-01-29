/*
Auteurs : Alexis Létourneau et Louis Boisvert
Date : 2024-11-25
Brief : Un programme qui envoit un json personnalisé en I2C à un Master sur un Raspberry PI 4.
Pour configurer un nouveau module d'enigme avec un autre ESP32, il faut :
- Prendre un SLAVE_ADDR différent des autres ESP32 connecté au PI.
- Changer la ligne Wire.Setpin() au pin désiré ou l'enlevé si le ESP32 a déjà des pins I2C.
- Changer la variable myName.
*/

#include <Wire.h> 
#include <Arduino.h>
#include <string.h>
#include <time.h>

#define SLAVE_ADDR 0x0a  // Adresse de l'esclave 

#define sw1Pin 7    //Les pins des objet interactifs (button, potentiometre, etc..)
#define sw2Pin 15
#define btn1Pin 16

String const sw1Name = "sw1"; //Les noms des objet interactifs (button, potentiometre, etc..)
String const sw2Name = "sw2";
String const btn1Name = "btn1";

String const myName = "enigmeTest1"; //L'ID du ESP 32

void requestData(); //Prototype de fonction

bool sw1State = 0;
bool sw2State = 0;
bool btn1State = 0;

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
 

void loop() 
{ } 

 
// Fonction appelée lorsque le maître demande des données 

void requestData() { 

  sw1State = digitalRead(sw1Pin);
  sw2State = digitalRead(sw2Pin);
  btn1State = digitalRead(btn1Pin);

  String stringOfInteractable = "{\"" + sw1Name + "\":\"" + sw1State + "\",\"" 
                                      + sw2Name + "\":\"" + sw2State + "\",\"" 
                                      + btn1Name + "\":\"" + btn1State +"\"}";

  stringOfAllData = "{\"NomESP32\":\"" + myName 
                   + "\",\"JsonData\":" + stringOfInteractable + "}";

  // Envoyer les données du tableau `dataToSend` au maître 
  for (int i = 0; i < stringOfAllData.length(); i++)
    Wire.write(stringOfAllData[i]);  // Envoyer chaque caractère 
  
  Wire.write(0x00);  // Le Master repete le dernier byte recu, donc le dernier byte est NULL
} 