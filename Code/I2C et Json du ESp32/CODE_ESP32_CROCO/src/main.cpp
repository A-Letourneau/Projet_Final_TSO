/*
Auteurs : Alexis Létourneau et Louis Boisvert
Date : 2024-11-25
Nom du fichier : main.cpp
Environnement : ESP32-C3-WROOM-02 Devkit, Platformio, C++ arduino, raspberry pi 4
Brief : Un programme pour l'envoit un json d'information en I2C à un Master sur un Raspberry PI 4. 
Ce code prend 8 patte et détecte si cette patte est connectée avec une autre patte.
Le code prend cette l'information et on met cette pair dans une liste, l'index est la sortie et le numéro à l'index est l'entrée. 
Cette liste contient donc deux fois la même connections, mais inversée. Exemple {1,0,3,2}, 1 et 0 sont connecté et 2 et 3 sont connecté.
Finalement, on envoit cette liste au Raspberry PI 4 en forme de Json.

*/

#include <Wire.h> //Communication I2C entre les esp32 et le PI
#include <Arduino.h> //Pour la programmation arduino
#include <string.h> //Pour la manipulation des string
#include <Adafruit_NeoPixel.h> 

#define SLAVE_ADDR 0x0b  // Adresse de l'esclave 

#define SDA_PIN 6
#define SCL_PIN 7

#define PIN_CROCO_0 1
#define PIN_CROCO_1 0
#define PIN_CROCO_2 4
#define PIN_CROCO_3 5
#define PIN_CROCO_4 2
#define PIN_CROCO_5 3
#define PIN_CROCO_6 18
#define PIN_CROCO_7 19
 

#define NB_CROCO 8 

#define noConnectionFound NB_CROCO //Si on ne trouve pas de connection, on met un nombre qui est plus que le nombre total de Croco

#define BRIGHTNESS 50 

void requestData(); //Prototype de fonction de réception du i2c 

String const ESP32_NAME = "I2C_Croco"; //L'ID du ESP 32

int g_listDeCrocoPin[NB_CROCO] = {PIN_CROCO_0, PIN_CROCO_1, PIN_CROCO_2, PIN_CROCO_3, PIN_CROCO_4, PIN_CROCO_5, PIN_CROCO_6, PIN_CROCO_7};
int g_pairDeCroco[NB_CROCO] = {};

String g_stringOfAllData = "";

Adafruit_NeoPixel uniDEL(1, 8, NEO_GRBW + NEO_KHZ800);

void setup() { 

  for(int curCroco = 0; curCroco < NB_CROCO; curCroco++)   //Mettre toutes les pattes "Croco" en entrée avec une pull-down
      pinMode(g_listDeCrocoPin[curCroco], INPUT_PULLDOWN);

  // Initialisation du port série pour le debug 
  Serial.begin(9600); 

  uniDEL.setBrightness(BRIGHTNESS);
  uniDEL.begin();
  uniDEL.show(); // Initialize all pixels to 'off' only run once, it runs right when you turn it on

  // Initialisation de l'I2C en tant qu'esclave avec l'adresse définie 
  Wire.setPins(SDA_PIN, SCL_PIN);
  Wire.begin(SLAVE_ADDR); 

  // Attacher une fonction de demande (request) pour le maître 
  Wire.onRequest(requestData); 

  Serial.println("Slave prêt, en attente de requêtes du maître..."); 

  //Hearbeat qui indique que le esp32 à bien démarré
  for (int i = 0; i < 3; i++)
  {
    uniDEL.setPixelColor(0, 0, 0, 255);
    uniDEL.show();
    delay(250);
    uniDEL.setPixelColor(0, 0, 0, 0);
    uniDEL.show();
    delay(250);
  }
} 
 
void loop() 
{ } 

/*
Brief : Fonction appelée lorsque le maître fait la demande des données. 
Renvoit un JSON contenant les paires de connection sur les pattes "Croco" connectées au esp32 sur la ligne i2c.
*/
void requestData() { 
  //Indique avec la DEL que le esp32 est entrain de résoudre une requête, s'éteint à la fin de la requête
  uniDEL.setPixelColor(0, 0, 0, 255);
  uniDEL.show();
  bool foundConnection = false; //Flag si on a detecte une connection

  //Chaques pattes "Croco" va être mit en sortie pour sondées les autres pattes en entrée
  for(int curOut = 0; curOut < NB_CROCO; curOut++) 
  { 
    pinMode(g_listDeCrocoPin[curOut], OUTPUT); //Patte "Croco" en sortie pour envoyer un signal
    digitalWrite(g_listDeCrocoPin[curOut], HIGH); //Le signal haut à détecter

    //Tout les autre pattes "Croco" en entrée vont être lu pour savoir s'ils ont reçu un signal
    for(int curIn = 0; curIn < NB_CROCO; curIn++)
    { 
      if(curIn != curOut)  //Si c'est pas la patte "Croco" en sortie
      {
        pinMode(g_listDeCrocoPin[curIn], INPUT_PULLDOWN); //On met la patte "Croco" en mode entrée
        if (digitalRead(g_listDeCrocoPin[curIn])) //Si on détecte le signal haut du "Croco" en OUTPUT
        {
          g_pairDeCroco[curOut] = curIn; //On enregistre la pair dans une liste, l'index est la sortie et le numéro à l'index est l'entrée. 
          foundConnection = true; 
        }
      }      
    }
    if (!foundConnection) //Si on trouve pas de connection, on met un nombre qui est plus grand que le nombre de "Croco" dans la liste pour indiquer aucune connection
      g_pairDeCroco[curOut] = noConnectionFound;
      
    digitalWrite(g_listDeCrocoPin[curOut], LOW); //On remet la patte "Croco" sortie en mode entrée
    foundConnection = false;
  }

  //Crée une string json pour contenir les paires de patte croco
  String stringOfInteractable = "[\"" + String(g_pairDeCroco[0]) + "\",\"" + String(g_pairDeCroco[1]) + "\",\"" 
                                      + String(g_pairDeCroco[2]) + "\",\"" + String(g_pairDeCroco[3]) + "\",\""
                                      + String(g_pairDeCroco[4]) + "\",\"" + String(g_pairDeCroco[5]) + "\",\"" 
                                      + String(g_pairDeCroco[6]) + "\",\"" + String(g_pairDeCroco[7]) +"\"]";

  //Crée une string json pour contenir le nom du esp32 et les objets
  g_stringOfAllData = "{\"NomEsp32\":\"" + ESP32_NAME 
                   + "\",\"JsonData\":" + stringOfInteractable + "}";

  // Envoyer les données du tableau `dataToSend` au maître 
  for (int i = 0; i < g_stringOfAllData.length(); i++)
    Wire.write(g_stringOfAllData[i]);  // Envoyer chaque caractère en byte
  
  Wire.write(0x00);  // Le Master repete le dernier byte recu, donc le dernier byte est NULL pour signaler la fin de la string
  uniDEL.setPixelColor(0, 0, 0, 0);
  uniDEL.show();
} 

