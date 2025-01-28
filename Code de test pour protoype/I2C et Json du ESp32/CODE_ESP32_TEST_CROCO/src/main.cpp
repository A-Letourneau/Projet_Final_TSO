/*
Auteurs : Alexis Létourneau et Louis Boisvert
Date : 2024-11-25
Nom du fichier : main.cpp
Environnement : ESP32-C3-WROOM-02 Devkit, Platformio, C++ arduino, raspberry pi 4
Brief : Un programme pré-configurer pour l'envoit un json personnalisé en I2C à un Master sur un 
    Raspberry PI 4. La configuration initial de ce code est pour une lecture digitales de 8 sortie pour savoir si elles sont relie entre elles.
    et on l'envoit par json a un raspberry pi 4.
*/

#include <Wire.h> //Communication I2C entre les esp32 et le PI
#include <Arduino.h> //Pour la programmation arduino
#include <string.h> //Pour la manipulation des string

#define SLAVE_ADDR 0x0b  // Adresse de l'esclave 

#define SDA_Pin 6
#define SCL_Pin 7

#define pinCroco0 0
#define pinCroco1 1
#define pinCroco2 2
#define pinCroco3 3
#define pinCroco4 4
#define pinCroco5 5
#define pinCroco6 18
#define pinCroco7 19

#define nbDeCroco 8

#define noConnectionFound nbDeCroco //Si on ne trouve pas de connection, on met un nombre qui est plus que le nombre de Croco

String const myName = "I2C_Croco"; //L'ID du ESP 32

void requestData(); //Prototype de fonction

int g_listDeCrocoPin[nbDeCroco] = {pinCroco0, pinCroco1, pinCroco2, pinCroco3, pinCroco4, pinCroco5, pinCroco6, pinCroco7};
int g_pairDeCroco[nbDeCroco] = {};

String stringOfAllData = "";

void setup() { 

  for(int curCroco = 0; curCroco < nbDeCroco; curCroco++)   
      pinMode(g_listDeCrocoPin[curCroco], INPUT_PULLDOWN);

  // Initialisation du port série pour le debug 
  Serial.begin(9600); 

  // Initialisation de l'I2C en tant qu'esclave avec l'adresse définie 
  Wire.setPins(6, 7);
  Wire.begin(SLAVE_ADDR); 

  // Attacher une fonction de demande (request) pour le maître 
  Wire.onRequest(requestData); 

  Serial.println("Slave prêt, en attente de requêtes du maître..."); 
  //Initialise les patte en entrée
} 
 
void loop() 
{ } 

/*
Brief : Fonction appelée lorsque le maître demande des données. 
Renvoit un JSON contenant les informations du esp32.
*/
void requestData() { 

  bool foundConnection = false; //Flag si on a detecte une connection

  //Chaques pattes "Croco" va être mit en sortie pour sondées les autres pattes en entrée
  for(int curOut = 0; curOut < nbDeCroco; curOut++) 
  { 
    pinMode(g_listDeCrocoPin[curOut], OUTPUT); //Patte "Croco" pour envoyer un signal
    digitalWrite(g_listDeCrocoPin[curOut], HIGH); //Le signal

    //Tout les autre pattes "Croco" en entrée vont être lu pour savoir s'ils ont reçu un signal
    for(int curIn = 0; curIn < nbDeCroco; curIn++)
    { 
      if(curIn != curOut)  //Si c'est pas la patte "Croco" en sortie
      {
        pinMode(g_listDeCrocoPin[curIn], INPUT_PULLDOWN); //On met la patte "Croco" en mode entrée
        if (digitalRead(g_listDeCrocoPin[curIn])) //Si on trouve une connection
        {
          g_pairDeCroco[curOut] = curIn; //On enregistre la pair dans une liste, l'index est la sortie et le numéro à l'index est l'entrée
          foundConnection = true; 
        }
      }      
    }
    if (!foundConnection) //Si on trouve pas de connection, on met 99 dans la liste pour l'indiquer 
      g_pairDeCroco[curOut] = noConnectionFound;
      
    digitalWrite(g_listDeCrocoPin[curOut], LOW); //On remet la patte "Croco" sortie en mode entrée
    foundConnection = false;
  }

  for(int cur = 0; cur < nbDeCroco; cur++) 
  {
    Serial.print(g_pairDeCroco[cur]);
    Serial.print(" ");
  }
  Serial.println();

  //Crée une string json pour contenir les paires de patte croco
  String stringOfInteractable = "[\"" + String(g_pairDeCroco[0]) + "\",\"" + String(g_pairDeCroco[1]) + "\",\"" 
                                      + String(g_pairDeCroco[2]) + "\",\"" + String(g_pairDeCroco[3]) + "\",\""
                                      + String(g_pairDeCroco[4]) + "\",\"" + String(g_pairDeCroco[5]) + "\",\"" 
                                      + String(g_pairDeCroco[6]) + "\",\"" + String(g_pairDeCroco[7]) +"\"]";

  //Crée une string json pour contenir le nom du esp32 et les objets
  stringOfAllData = "{\"NomEsp32\":\"" + myName 
                   + "\",\"JsonData\":" + stringOfInteractable + "}";

  // Envoyer les données du tableau `dataToSend` au maître 
  for (int i = 0; i < stringOfAllData.length(); i++)
    Wire.write(stringOfAllData[i]);  // Envoyer chaque caractère en byte
  
  Wire.write(0x00);  // Le Master repete le dernier byte recu, donc le dernier byte est NULL pour signaler la fin de la string

} 

