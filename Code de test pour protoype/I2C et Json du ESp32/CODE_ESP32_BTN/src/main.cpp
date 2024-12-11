/* Corrrection : 7/10
    Il manque la partie "nom de fichier" et "Environnement" au brief.
    Commentaires pour les #include
    Variables globales avec un g_
    Entêtes de fonction faible ou absente
*/
/*
Auteurs : Alexis Létourneau et Louis Boisvert
Date : 2024-11-25
Brief : Un programme pré-configurer pour l'envoit un json personnalisé en I2C à un Master sur un 
    Raspberry PI 4. La configuration initial de ce code est pour une lecture digitales de 4 bouttons.
    et l'envoit par json.

    il  vous suffit de remplacer le code dans le main par celui-ci pour configurer l'un des esp32.
*/

#include <Wire.h> 
#include <Arduino.h>
#include <string.h>
#include <time.h>

#define SLAVE_ADDR 0x0a  // Adresse de l'esclave 

#define SDA_Pin 6
#define SCL_Pin 7

#define Btn1Pin 0
#define Btn2Pin 1
#define Btn3Pin 2
#define Btn4Pin 3

String const Btn1Name = "Btn1"; //Les noms des objet interactifs (button, potentiometre, etc..)
String const Btn2Name = "Btn2";
String const Btn3Name = "Btn3";
String const Btn4Name = "Btn4";

String const myName = "I2C_Btn"; //L'ID du ESP 32

void requestData(); //Prototype de fonction

bool Btn1State = 0;
bool Btn2State = 0;
bool Btn3State = 0;
bool Btn4State = 0;

String stringOfAllData = "";


void setup() { 

  // Initialisation du port série pour le debug 
  Serial.begin(115200); 

  // Initialisation de l'I2C en tant qu'esclave avec l'adresse définie 
  Wire.setPins(6, 7);
  Wire.begin(SLAVE_ADDR); 

  // Attacher une fonction de demande (request) pour le maître 
  Wire.onRequest(requestData); 

  Serial.println("Slave prêt, en attente de requêtes du maître..."); 
  //Initialise les patte en entrée
  pinMode(Btn1Pin, INPUT);
  pinMode(Btn2Pin, INPUT);
  pinMode(Btn3Pin, INPUT);
  pinMode(Btn4Pin, INPUT);
  
} 
 

void loop() 
{ } 

 
// Fonction appelée lorsque le maître demande des données 
void requestData() { 
  //Lit l'état des objets
  Btn1State = digitalRead(Btn1Pin);
  Btn2State = digitalRead(Btn2Pin);
  Btn3State = digitalRead(Btn3Pin);
  Btn4State = digitalRead(Btn4Pin);

  //Crée une string json pour contenir les boutons
  String stringOfInteractable = "{\"" + Btn1Name + "\":\"" + Btn1State + "\",\"" 
                                      + Btn2Name + "\":\"" + Btn2State + "\",\""
                                      + Btn3Name + "\":\"" + Btn3State + "\",\"" 
                                      + Btn4Name + "\":\"" + Btn4State +"\"}";

  //Crée une string json pour contenir le nom du esp32 et les objets
  stringOfAllData = "{\"NomEsp32\":\"" + myName 
                   + "\",\"JsonData\":" + stringOfInteractable + "}";

  // Envoyer les données du tableau `dataToSend` au maître 
  for (int i = 0; i < stringOfAllData.length(); i++)
    Wire.write(stringOfAllData[i]);  // Envoyer chaque caractère en byte
  
  Wire.write(0x00);  // Le Master repete le dernier byte recu, donc le dernier byte est NULL pour signaler la fin de la string
} 
