# Programme de Communication I2C avec JSON pour ESP32

Ce programme permet d’envoyer un JSON personnalisé via communication I2C à un maître.  
Le maître utilisé dans notre projet est un **Raspberry Pi 4**.  

## Configuration d’un Nouveau Module d’Énigme avec un ESP32  

Pour ajouter un nouveau module, suivez ces étapes :  

1. **Définir une adresse différente pour chaque module :**  
   Attribuez une valeur unique à **`SLAVE_ADDR`**, différente de celles des autres ESP32 connectés au Raspberry Pi.  

2. **Configurer les broches I2C (si nécessaire) :**  
   - Modifiez la ligne **`Wire.setPins()`** pour définir les broches I2C souhaitées.  
   - Si l’ESP32 utilise déjà des broches par défaut, cette ligne peut être supprimée.  

3. **Personnaliser l’identifiant du module :**  
   Changez la valeur de la variable **`myName`** pour identifier le module.  

4. **Adapter le fichier `platformio.ini` :**  
   - Vérifiez que le fichier **`platformio.ini`** correspond à la carte ESP32 utilisée.  
   - Si vous utilisez une carte différente (par ex. **ESP32-WROOM** ou **ESP32C3 DevKit2**), adaptez les configurations en conséquence.  

---

### Remarque  
Assurez-vous que tous les modules sont correctement configurés pour éviter les conflits d’adresse sur le bus I2C.
