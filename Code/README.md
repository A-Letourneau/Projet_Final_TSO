# 📂 Code

Ce dépôt regroupe 4 ensembles de fichiers essentiels pour le fonctionnement du prototype. 

## 📂 I2C et JSON pour ESP32  
Ce dossier contient le code en C++ chargé dans les ESP32.  
Il permet à ces derniers d’envoyer des messages JSON en I2C contenant l'état des objets interactifs au Raspberry PI.  

---

## 📂 Interface Graphique (Mallette GUI)  
Ce dossier contient :
- Le code Python nécessaire pour afficher les données i2c reçues sous forme de JSON dans une interface.  
- L’affichage à l’écran est réalisé à l’aide de la bibliothèque **PySimpleGUI**. 

---

## 📂 Projet Final MQTT  
Ce dossier contient :  
- Les bases de données SQLite utilisées dans le projet.  
- Les codes Python responsables de la gestion de la réception des données via MQTT provenant du raspberry PI.  
Note : Même si le MQTT est disponible, nous avons décidé de ne pas l'utiliser.

---

## 📂 Clavier esp32
Ce dossier contient :  
- Le code "main.py" qui va dans un clavier esp32 qui utilise la librairie kmk_firmware .  

---

### 🛠️ Notes
Chaque dossier est structuré pour permettre une utilisation autonome des fonctionnalités qu’il contient. Consultez les fichiers README individuels dans chaque dossier pour plus de détails.

Correction

28 oct 5/5 


4 nov 5/5

11 nov 5/5 

24 nov 5/5 (Bravo pour le beau readme.md du dossier principal).

3 déc 5/5 
