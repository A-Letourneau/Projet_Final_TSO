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

#define Btn1Pin 0
#define Btn2Pin 1
#define Btn3Pin 2
#define Btn4Pin 3

#define DelPin 18

String const Btn1Name = "Btn1"; //Les noms des objet interactifs (button, potentiometre, etc..)
String const Btn2Name = "Btn2";
String const Btn3Name = "Btn3";
String const Btn4Name = "Btn4";

String const myName = "I2C_Btn"; //L'ID du ESP 32

void requestData(); //Prototype de fonction
void receiveData(int nbByte);

bool g_Btn1State = 0;
bool g_Btn2State = 0;
bool g_Btn3State = 0;
bool g_Btn4State = 0;

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
  pinMode(Btn1Pin, INPUT);
  pinMode(Btn2Pin, INPUT);
  pinMode(Btn3Pin, INPUT);
  pinMode(Btn4Pin, INPUT);

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
  g_Btn1State = digitalRead(Btn1Pin);
  g_Btn2State = digitalRead(Btn2Pin);
  g_Btn3State = digitalRead(Btn3Pin);
  g_Btn4State = digitalRead(Btn4Pin);

  //Crée une string json pour contenir les boutons
  String stringOfInteractable = "{\"" + Btn1Name + "\":\"" + g_Btn1State + "\",\"" 
                                      + Btn2Name + "\":\"" + g_Btn2State + "\",\""
                                      + Btn3Name + "\":\"" + g_Btn3State + "\",\"" 
                                      + Btn4Name + "\":\"" + g_Btn4State +"\"}";

  //Crée une string json pour contenir le nom du esp32 et les objets
  stringOfAllData = "{\"NomEsp32\":\"" + myName 
                   + "\",\"JsonData\":" + stringOfInteractable + "}";

  // Envoyer les données du tableau `dataToSend` au maître 
  for (int i = 0; i < stringOfAllData.length(); i++)
    Wire.write(stringOfAllData[i]);  // Envoyer chaque caractère en byte
  
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