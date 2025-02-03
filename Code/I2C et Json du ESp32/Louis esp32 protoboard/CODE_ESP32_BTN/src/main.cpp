/*
Auteurs : Alexis Létourneau et Louis Boisvert
Date : 2024-11-25
Nom du fichier : main.cpp
Environnement : ESP32-C3-WROOM-02 Devkit, Platformio, C++ arduino, raspberry pi 4
Brief : Un programme pour l'envoit un json d'information en I2C à un Master sur un Raspberry PI 4. 
Ce code prend l'état de 4 boutons et le met dans un dictionnaire.
Finalement, on envoit ce dictionnaire au Raspberry PI 4 en forme de Json.
*/

#include <Wire.h> //Communication I2C entre les esp32 et le PI
#include <Arduino.h> //Pour la programmation arduino
#include <string.h> //Pour la manipulation des string
 
#define SLAVE_ADDR 0x0a  // Adresse de l'esclave 

#define SDA_Pin 6
#define SCL_Pin 7

/*#define Sw1Pin 0
#define Sw2Pin 1
#define Sw3Pin 2
#define Sw4Pin 3*/

#define NUM_SWITCHES 8  // Number of switches

// l'ordre des interrupteurs est de gauche à droites de haunt en bas 
const int switchPins[NUM_SWITCHES] = {4, 5, 0, 8, 19, 3, 18, 2}; // Pins des interrupteurs
const String switchNames[NUM_SWITCHES] = {"Sw1", "Sw2", "Sw3", "Sw4", "Sw5", "Sw6", "Sw7", "Sw8"}; // Noms des interrupteurs

#define DelPin 18

/*String const Sw1Name = "Sw1"; //Les noms des objet interactifs (button, potentiometre, etc..)
String const Sw2Name = "Sw2";
String const Sw3Name = "Sw3";
String const Sw4Name = "Sw4";*/

String const myName = "I2C_Sw"; //L'ID du ESP 32

void requestData(); //Prototype de fonction
void receiveData(int nbByte);

/*bool g_Sw1State = 0;
bool g_Sw2State = 0;
bool g_Sw3State = 0;
bool g_Sw4State = 0;*/
bool switchstates[NUM_SWITCHES] = {0};  //met toutes les valeurs à 0

String stringOfAllData = "";

void setup() { 

  // Initialisation du port série pour le debug 
  Serial.begin(9600); 

  // Initialisation de l'I2C en tant qu'esclave avec l'adresse définie 
  Wire.setPins(6, 7);
  Wire.begin(SLAVE_ADDR); 

  // Attacher une fonction de demande (request) pour le maître 
  Wire.onRequest(requestData); 
  Wire.onReceive(receiveData);

  Serial.println("Slave prêt, en attente de requêtes du maître..."); 
  //Initialise les patte en entrée
  /*pinMode(Sw1Pin, INPUT);
  pinMode(Sw2Pin, INPUT);
  pinMode(Sw3Pin, INPUT);
  pinMode(Sw4Pin, INPUT);*/

  pinMode(DelPin, OUTPUT);
  
} 
 

void loop() 
{ } 

 
/*
Brief : Fonction appelée lorsque le maître fait la demande des données. 
Renvoit un JSON contenant les état des boutons connectés au esp32 sur la ligne i2c.
*/
void requestData() { 
  //Lit l'état des objets
  /*g_Sw1State = digitalRead(Sw1Pin);
  g_Sw2State = digitalRead(Sw2Pin);
  g_Sw3State = digitalRead(Sw3Pin);
  g_Sw4State = digitalRead(Sw4Pin);*/

  for(int i = 0; i < NUM_SWITCHES; i++) {
    switchstates[i] = digitalRead(switchPins[i]); // Lit l'état du bouton et le stocke dans le tableau
  }

  //Crée une string json pour contenir les boutons
  /*String stringOfInteractable = "{\"" + Sw1Name + "\":\"" + g_Sw1State + "\",\"" 
                                      + Sw2Name + "\":\"" + g_Sw2State + "\",\""
                                      + Sw3Name + "\":\"" + g_Sw3State + "\",\"" 
                                      + Sw4Name + "\":\"" + g_Sw4State +"\"}";*/
  String stringOfInteractable = "{";
  for (int i = 0; i < NUM_SWITCHES; i++)
  {
    stringOfInteractable += "\"" + switchNames[i] + "\":\"" + switchstates[i] + "\",";  //cette boucle devrait ajouter toutes les interrupteurs et leurs états à une string
  }

  //Crée une string json pour contenir le nom du esp32 et les objets
  stringOfAllData = "{\"NomEsp32\":\"" + myName 
                   + "\",\"JsonData\":" + stringOfInteractable + "}}";

  // Envoyer les données du tableau `dataToSend` au maître 
  for (int i = 0; i < stringOfAllData.length(); i++)
  {
    Wire.write(stringOfAllData[i]);  // Envoyer chaque caractère en byte
  }
  Wire.write(0x00);  // Le Master repete le dernier byte recu, donc le dernier byte est NULL pour signaler la fin de la string
} 

void receiveData(int nbByte) {

  Wire.read(); //On ignore la premiere donne car elle est inutile
  while(Wire.available()) // loop through all char
  {
    char c = Wire.read(); // receive byte as a character
    if (c == 'D') //Allume la DEL selon le byte recu
      digitalWrite(DelPin, HIGH);
    else
      digitalWrite(DelPin, LOW);
  }
}