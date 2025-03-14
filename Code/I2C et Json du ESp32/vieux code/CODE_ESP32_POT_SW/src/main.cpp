/*
Auteurs : Alexis Létourneau et Louis Boisvert
Date : 2024-11-25
Nom du fichier : main.cpp
Environnement : ESP32-C3-WROOM-02 Devkit, Platformio, C++ arduino, raspberry pi 4
Brief : Un programme pour l'envoit un json d'information en I2C à un Master sur un Raspberry PI 4. 
Ce code prend l'état de 2 interrupteurs et 3 potentiomètres et le met dans un dictionnaire.
Finalement, on envoit ce dictionnaire au Raspberry PI 4 en forme de Json.
*/

#include <Wire.h> //Communication I2C entre les esp32 et le PI
#include <Arduino.h> //Pour la programmation arduino
#include <string.h> //Pour la manipulation des string

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

String const myName = "I2C_Pot_Sw"; //L'ID du ESP 32

void requestData(); //Prototype de fonction

bool g_Sw1State = 0;
bool g_Sw2State = 0;
int g_Pot1State = 0;
int g_Pot2State = 0;
int g_Pot3State = 0;

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

  //Initialise les patte en entrée
  pinMode(Sw1Pin, INPUT);
  pinMode(Sw2Pin, INPUT);
  pinMode(Pot1Pin, INPUT);
  pinMode(Pot2Pin, INPUT);
  pinMode(Pot3Pin, INPUT);
} 
 

void loop() 
{ } 

 
/*
Brief : Fonction appelée lorsque le maître fait la demande des données. 
Renvoit un JSON contenant les état des interrupteurs et des potentiomètres connectés au esp32 sur la ligne i2c.
*/
void requestData() { 

  //Lit l'état des objets
  g_Sw1State = digitalRead(Sw1Pin);
  g_Sw2State = digitalRead(Sw2Pin);
  g_Pot1State = analogRead(Pot1Pin);
  g_Pot2State = analogRead(Pot2Pin);
  g_Pot3State = analogRead(Pot3Pin);

  //Crée une string json pour contenir les interrupteurs et potentiomètres
  String stringOfInteractable = "{\"" + Sw1Name + "\":\"" + g_Sw1State + "\",\"" 
                                      + Sw2Name + "\":\"" + g_Sw2State + "\",\""
                                      + Pot1Name + "\":\"" + g_Pot1State + "\",\""
                                      + Pot2Name + "\":\"" + g_Pot2State + "\",\"" 
                                      + Pot3Name + "\":\"" + g_Pot3State +"\"}";

  //Crée une string json pour contenir le nom du esp32 et les objets
  stringOfAllData = "{\"NomEsp32\":\"" + myName 
                   + "\",\"JsonData\":" + stringOfInteractable + "}";

  // Envoyer les données du tableau `dataToSend` au maître 
  for (int i = 0; i < stringOfAllData.length(); i++)
    Wire.write(stringOfAllData[i]);  // Envoyer chaque caractère en byte
  
  Wire.write(0x00);  // Le Master repete le dernier byte recu, donc le dernier byte est NULL pour signaler la fin de la string
} 
