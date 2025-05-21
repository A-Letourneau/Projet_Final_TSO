# Programme de Communication I2C avec JSON pour ESP32

Ce fichier contient tous les codes fait en rapport avec les esp32 en c++

Les programmes de CODE_ESP32_POT, CODE_ESP32_SW et CODE_ESP32_CROCO permet d’envoyer les états des objets interactifs (interrupteur, potentiomètre et fils banane/croco) dans un JSON via communication I2C à un maître.  
Le maître utilisé dans notre projet est un **Raspberry Pi 4**.  
Les sub (esclaves) utilisés dans notre projet est le **esp32 c3 devkit 02**

## Configuration d’un Nouveau Module d’Énigme avec un ESP32  

Pour ajouter un nouveau module, suivez ces étapes :  

1. **Définir une adresse différente pour chaque module :**  
   Attribuez une valeur unique à **`SLAVE_ADDR`**, différente de celles des autres ESP32 connectés au Raspberry Pi.  

2. **Configurer les broches I2C (si nécessaire) :**  
   - Modifiez la ligne **`Wire.setPins()`** pour définir les broches I2C souhaitées.  
   - Si l’ESP32 utilise déjà des broches par défaut, cette ligne peut être supprimée.  
   - Les pattes arbitraires pour le i2c que nous avons choisi est le 6 pour SDA et 7 pour SCL.

3. **Personnaliser l’identifiant du module :**  
   Changez la valeur de la variable **`ESP32_NAME`** pour identifier le module.  

4. **Adapter le fichier `platformio.ini` :**  
   - Vérifiez que le fichier **`platformio.ini`** correspond à la carte ESP32 utilisée.  
   - Si vous utilisez une carte différente (par ex. **ESP32-WROOM** ou **ESP32C3 DevKit2**), adaptez les configurations en conséquence.  

---

### Remarque  
Assurez-vous que tous les modules sont correctement configurés pour éviter les conflits d’adresse sur le bus I2C.
Utilisez i2cdetect -i 0 sur le cmd du pi pour détecter les connections i2c
