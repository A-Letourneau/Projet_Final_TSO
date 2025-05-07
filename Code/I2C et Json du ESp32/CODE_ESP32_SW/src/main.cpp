/*
Auteurs : Alexis Létourneau et Louis Boisvert
Date : 2024-11-25
Nom du fichier : main.cpp
Environnement : ESP32-C3-WROOM-02 Devkit, Platformio, C++ arduino, raspberry pi 4
Brief : Un programme pour l'envoit un json d'information en I2C à un Master sur un Raspberry PI 4. 
Ce code prend l'état de 8 interrupteurs et le met dans un dictionnaire.
Finalement, on envoit ce dictionnaire au Raspberry PI 4 en forme de Json.
*/

#include <Wire.h> //Communication I2C entre les esp32 et le PI
#include <Arduino.h> //Pour la programmation arduino
#include <string.h> //Pour la manipulation des string
#include <Adafruit_NeoPixel.h> 

#define SLAVE_ADDR 0x0a  // Adresse de l'esclave 

#define SDA_PIN 6
#define SCL_PIN 7

#define NUM_SWITCHES 8  // Number of switches

#define BRIGHTNESS 50 

void requestData(); //Prototype de fonction

// l'ordre des interrupteurs est de gauche à droites de haut en bas 
//const int SWITCH_PINS[NUM_SWITCHES] = {0, 2, 4, 19, 1, 3, 18, 5}; // Pins des interrupteurs
const int SWITCH_PINS[NUM_SWITCHES] = {5, 4, 19, 18, 1, 0, 3, 2}; // Pins des interrupteurs
const String SWITCH_NAMES[NUM_SWITCHES] = {"Sw1", "Sw2", "Sw3", "Sw4", "Sw5", "Sw6", "Sw7", "Sw8"}; // Noms des interrupteurs

String const ESP32_NAME = "I2C_Sw"; //L'ID du ESP 32

bool switchStates[NUM_SWITCHES] = {0}; 

String stringOfAllData = "";

Adafruit_NeoPixel uniDEL(1, 8, NEO_GRBW + NEO_KHZ800);

void setup() { 

  // Initialisation du port série pour le debug 
  Serial.begin(9600); 

  // Initialisation de l'I2C en tant qu'esclave avec l'adresse définie 
  Wire.setPins(6, 7);
  Wire.begin(SLAVE_ADDR); 

  // Attacher une fonction de demande (request) pour le maître 
  Wire.onRequest(requestData); 

  Serial.println("Slave prêt, en attente de requêtes du maître..."); 

  for(int i = 0; i < NUM_SWITCHES; i++) 
    pinMode(SWITCH_PINS[i], INPUT); // Initialise les pins des interrupteurs en entrée


  //Hearbeat qui indique que le esp32 à bien démarré
  for (int i = 0; i < 3; i++)
    {
      uniDEL.setPixelColor(0, 0, 0, 255);
      uniDEL.show();
      delay(100);
      uniDEL.setPixelColor(0, 0, 0, 0);
      uniDEL.show();
      delay(100);
    }
  } 
 

void loop() 
{ } 

 
/*
Brief : Fonction appelée lorsque le maître fait la demande des données. 
Renvoit un JSON contenant les état des boutons connectés au esp32 sur la ligne i2c.
*/
void requestData() { 
  //Indique avec la DEL que le esp32 est entrain de résoudre une requête, s'éteint à la fin de la requête
  uniDEL.setPixelColor(0, 255, 0, 0);
  uniDEL.show();
  
  for(int i = 0; i < NUM_SWITCHES; i++)
    switchStates[i] = digitalRead(SWITCH_PINS[i]); // Lit l'état du bouton et le stocke dans le tableau

  //Crée une string json pour contenir les boutons
  String stringOfInteractable = "{";
  for (int i = 0; i < NUM_SWITCHES; i++)  //cette boucle ajoute toutes les interrupteurs et leurs états à une string
  {
    if(i == NUM_SWITCHES-1)
    {
      stringOfInteractable += "\"" + SWITCH_NAMES[i] + "\":\"" + switchStates[i] + "\""; //enlève la virgule à la fin
    }
    else
    {
      stringOfInteractable += "\"" + SWITCH_NAMES[i] + "\":\"" + switchStates[i] + "\",";
    }
  }

  //Crée une string json pour contenir le nom du esp32 et les objets
  stringOfAllData = "{\"NomEsp32\":\"" + ESP32_NAME 
                   + "\",\"JsonData\":" + stringOfInteractable + "}}";

  // Envoyer les données du tableau `dataToSend` au maître 
  for (int i = 0; i < stringOfAllData.length(); i++)
    Wire.write(stringOfAllData[i]);  // Envoyer chaque caractère en byte

  Wire.write(0x00);  // Le Master repete le dernier byte recu, donc le dernier byte est NULL pour signaler la fin de la string
  uniDEL.setPixelColor(0, 0, 0, 0);
  uniDEL.show();
} 
