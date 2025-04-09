/*
Auteurs : Alexis Létourneau et Louis Boisvert
Date : 2024-11-25
Nom du fichier : main.cpp
Environnement : ESP32-C3-WROOM-02 Devkit, Platformio, C++ arduino, raspberry pi 4
Brief : Un programme pour l'envoit un json d'information en I2C à un Master sur un Raspberry PI 4. 
Ce code prend l'état de 3 potentiomètres et le met dans un dictionnaire.
Finalement, on envoit ce dictionnaire au Raspberry PI 4 en forme de Json.

CE CODE A UN AJUSTEMENT TEMPORAIRE À CAUSE D'UN PROBLÈME DE PCB
Il faut rerouter les pin 9, 8 et 5 à 0, 1 et 2, donc il faut désactiver les pattes 9, 8 et 5 comme décrit à la ligne 57
*/

#include <Wire.h> //Communication I2C entre les esp32 et le PI
#include <Arduino.h> //Pour la programmation arduino
#include <string.h> //Pour la manipulation des string
#include <Adafruit_NeoPixel.h> 

#define SLAVE_ADDR 0x09 

#define SDA_PIN 6
#define SCL_PIN 7

#define NUM_POT 3  

#define BRIGHTNESS 50 

#define DEBUG true

void requestData(); //Prototype de fonction

const int POT_PINS[NUM_POT] = {0, 1, 2}; // Pins des pot en ordre
const String POT_NAMES[NUM_POT] = {"Pot1", "Pot2", "Pot3"}; // Noms des interrupteurs dans le meme ordre que POT_PINS

const String ESP32_NAME = "I2C_Pot"; //L'ID du ESP 32
  
int potStates[NUM_POT] = {0};  //Init toutes les valeurs à 0

String stringOfAllData = "";

Adafruit_NeoPixel uniDEL(1, 8, NEO_GRBW + NEO_KHZ800);

void setup() { 

  // Initialisation du port série pour le debug 
  Serial.begin(115200); 

  // Initialisation de l'I2C en tant qu'esclave avec l'adresse définie 
  Wire.setPins(SDA_PIN, SCL_PIN);
  Wire.begin(SLAVE_ADDR); 

  // Attacher une fonction de demande (request) pour le maître 
  Wire.onRequest(requestData); 

  Serial.println("Slave prêt, en attente de requêtes du maître..."); 

  //Hearbeat qui indique que le esp32 à bien démarré
  for (int i = 0; i < 3; i++)
  {
    uniDEL.setPixelColor(0, 0, 255, 0);
    uniDEL.show();
    delay(250);
    uniDEL.setPixelColor(0, 0, 0, 0);
    uniDEL.show();
    delay(250);
  }
  //Initialise les pattes en entrée
  for (int i = 0; i <NUM_POT; i++)
  {
    pinMode(POT_PINS[i], INPUT);
  }
  /*TEMPORAIRE, parce que le PCB est mauvais, il faut rerouter les pin 9, 8 et 5 à 0,1 et 2, donc il faut désactiver ces pattes*/
  pinMode(9, INPUT);
  pinMode(8, INPUT);
  pinMode(5, INPUT);
} 
 
void loop() 
{} 
 
/*
Brief : Fonction appelée lorsque le maître fait la demande des données. 
Renvoit un JSON contenant les état des interrupteurs et des potentiomètres connectés au esp32 sur la ligne i2c.
*/
void requestData() { 
  //Indique avec la DEL que le esp32 est entrain de résoudre une requête, s'éteint à la fin de la requête
  uniDEL.setPixelColor(0, 0, 0, 255);
  uniDEL.show();
  for (int i = 0; i < NUM_POT; i++)
    potStates[i] = analogRead(POT_PINS[i]);

  //cette boucle crée une string json pour contenir les interrupteurs et potentiomètres
  String stringOfInteractable = "{";
  for (int i = 0; i < NUM_POT; i++) 
  {
    if( i == NUM_POT-1) //permet de ne pas avoir de virgule à la fin du json
    {
      stringOfInteractable += "\"" + POT_NAMES[i] + "\":\"" + potStates[i] +"\"";
    }
    else
    {
      stringOfInteractable += "\"" + POT_NAMES[i] + "\":\"" + potStates[i] +"\",";
    }
  }

  //Crée une string json pour contenir le nom du esp32 et les objets
  stringOfAllData = "{\"NomEsp32\":\"" + ESP32_NAME 
                   + "\",\"JsonData\":" + stringOfInteractable + " } }";

  if (DEBUG)
    Serial.print(stringOfAllData);
    
  // Envoyer les données du tableau `dataToSend` au maître 
  for (int i = 0; i < stringOfAllData.length(); i++)
    Wire.write(stringOfAllData[i]);  // Envoyer chaque caractère en byte
  
  Wire.write(0x00);  // Le Master repete le dernier byte recu, donc le dernier byte est NULL pour signaler la fin de la string
  uniDEL.setPixelColor(0, 0, 0, 0);
  uniDEL.show();
} 
