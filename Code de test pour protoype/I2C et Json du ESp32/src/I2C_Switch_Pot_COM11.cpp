/*
Auteurs : Alexis Létourneau et Louis Boisvert
Date : 2024-11-25
Brief : Un programme pré-configurer pour l'envoit un json personnalisé en I2C à un Master sur un 
    Raspberry PI 4. sa configuration présente est pour une suite de 2 switch et 3 potentiomètres.
    
    il  vous suffit de remplacer le code dans le main par celui-ci pour configurer l'un des esp32.
*/

#include <Wire.h> 
#include <Arduino.h>
#include <string.h>
#include <time.h>

#define SLAVE_ADDR 0x09  // Adresse de l'esclave 

#define SDA_Pin 6
#define SCL_Pin 7

#define Sw1Pin 19   //Les pins des objet interactifs (button, potentiometre, etc..)
#define Sw2Pin 18
#define Pot1Pin 0
#define Pot2Pin 1
#define Pot3Pin 2

String const Sw1Name = "Sw1"; //Les noms des objet interactifs (button, potentiometre, etc..)
String const Sw2Name = "Sw2";
String const Pot1Name = "Pot1";
String const Pot2Name = "Pot2";
String const Pot3Name = "Pot3";

String const myName = "I2C_Switch_Pot_COM11"; //L'ID du ESP 32

void requestData(); //Prototype de fonction

bool Sw1State = 0;
bool Sw2State = 0;
int Pot1State = 0;
int Pot2State = 0;
int Pot3State = 0;

String stringOfAllData = "";


void setup() { 

  // Initialisation du port série pour le debug 
  Serial.begin(115200); 

  // Initialisation de l'I2C en tant qu'esclave avec l'adresse définie 
  Wire.setPins(SDA_Pin, SCL_Pin);
  Wire.begin(SLAVE_ADDR); 

  // Attacher une fonction de demande (request) pour le maître 
  Wire.onRequest(requestData); 

  Serial.println("Slave prêt, en attente de requêtes du maître..."); 

  pinMode(Sw1Pin, INPUT);
  pinMode(Sw2Pin, INPUT);
  pinMode(Pot1Pin, INPUT);
  pinMode(Pot2Pin, INPUT);
  pinMode(Pot3Pin, INPUT);
} 
 

void loop() 
{ } 

 
// Fonction appelée lorsque le maître demande des données 

void requestData() { 

  Sw1State = digitalRead(Sw1Pin);
  Sw2State = digitalRead(Sw2Pin);
  Pot1State = analogRead(Pot1Pin);
  Pot2State = analogRead(Pot2Pin);
  Pot3State = analogRead(Pot3Pin);

  String stringOfInteractable = "{\"" + Sw1Name + "\":\"" + Sw1State + "\",\"" 
                                      + Sw2Name + "\":\"" + Sw2State + "\",\""
                                      + Pot1Name + "\":\"" + Pot1State + "\",\""
                                      + Pot2Name + "\":\"" + Pot2State + "\",\"" 
                                      + Pot3Name + "\":\"" + Pot3State +"\"}";

  stringOfAllData = "{\"NomEsp32\":\"" + myName 
                   + "\",\"JsonData\":" + stringOfInteractable + "}";

  // Envoyer les données du tableau `dataToSend` au maître 
  for (int i = 0; i < stringOfAllData.length(); i++)
    Wire.write(stringOfAllData[i]);  // Envoyer chaque caractère 
  
  Wire.write(0x00);  // Le Master repete le dernier byte recu, donc le dernier byte est NULL
} 