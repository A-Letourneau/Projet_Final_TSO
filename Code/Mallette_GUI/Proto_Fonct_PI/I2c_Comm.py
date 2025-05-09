"""
Auteur : Louis Boisvert & Alexis Létourneau
Date : 2025-03-11
Environnement : Python, Thonny, raspberry pi 4, ESP32-C3-WROOM-02 Devkit, 
Brief : Cette library permet d'envoyer une demande de données au ESP32 et de recevoir un JSON contenant les données des objets interactifs.

"""

from smbus2 import SMBus, i2c_msg   #Pour la communication i2c
import json                         #Pour la manipulation des json

#Brief : Une fonction qui envoit une demande de donnée à l'adresse d'un esp32 
#Param : L'adresse i2c du esp32
def sendRequest(SlaveAddresse, DEBUG):
    strReceived = ''
    #Demande le json du esp32 et reçoit une liste de byte
    with SMBus(1) as bus:
        msg = i2c_msg.read(SlaveAddresse, 125) #Demande 125 bytes à l'addresse du sub
        bus.i2c_rdwr(msg) #retourne par pointer la liste de byte dans msg
    #Transforme la ligne de byte en string
    for value in msg:
        if(value == 0x00): #Signifie la fin de la string
            break
        else:
            strReceived += chr(value) #Accumule les caractères pour faire un string Json complet
    if DEBUG:
        print(strReceived)
    return json.loads(strReceived) #Transforme la string JSON en dict pour l'utiliser en dictionnaire
