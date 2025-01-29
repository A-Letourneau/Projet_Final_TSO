"""
Auteur : Alexis Létourneau
Date : 2024-12-03
Environnement : Python, Thorny, raspberry pi 4, ESP32-C3-WROOM-02 Devkit, 
Brief : Programme qui affiche les données reçu par la communication i2c de un esp32 externe en mode Sub et qui affiche le résultat dans une interface PySimpleGUI.
Ce programme communique en i2c en mode Main avec l'esp32 en mode Sub. 
Le ESP32 est configuré pour envoyé une liste qui dit si une de ses pattes est connectées à une autre de ses pattes.


Le ESP32 a une interface, qui contient des "widget" qui représentent l'états des connections entre les pattes.
Si le ESP32 détecte une connection, alors on affiche les deux pattes avec la même couleur, sinon, on affiche du noir pour signifier aucune connection.

Le programme peut aussi transmettre le JSON des esp32 en MQTT à toutes les secondes pour faire la collecte de données.
Pour ce faire, enlever les # des entêtes MQTT.

"""
import PySimpleGUI as sg #Pour l'affichage utilisateur
import json #Pour la manipulation des JSON
from smbus2 import SMBus, i2c_msg #Pour la communication i2c pi

slave_address_Croco = 0x0b

listOfByte = [] #Pour la reception des messages i2c
listColor = ['green','pink', 'yellow', 'cyan'] #Pour la couleur des paires

#Crée un "Widget" de rond de couleur pour l'état des Croco
def LEDIndicator(key=None, radius=30): 
    return sg.Graph(canvas_size=(radius, radius),
             graph_bottom_left=(-radius, -radius),
             graph_top_right=(radius, radius),
             pad=(0, 0), key=key)

#Change la couleur d'un "Widget" de rond de couleur pour associer des paires de Croco
def SetLED(window, key, color):
    graph = window[key]
    graph.erase()
    graph.draw_circle((0, 0), 25, fill_color=color, line_color=color)

#Les layout et activation de la fenêtre Croco
layout = [[sg.Text('My croco indicator', size=(20,1))],
          [sg.Text('Croco 1'),  sg.Text('Croco 2'),  sg.Text('Croco 3'), sg.Text('Croco 4')],
          [LEDIndicator('0'), LEDIndicator('1'), LEDIndicator('2'), LEDIndicator('3')],
          [LEDIndicator('4'), LEDIndicator('5'), LEDIndicator('6'), LEDIndicator('7')],          
          [sg.Text('Croco 5'),  sg.Text('Croco 6'),  sg.Text('Croco 7'), sg.Text('Croco 8')],
          [sg.Button('Exit')]]


window_Croco = sg.Window('My new window', layout, default_element_size=(12, 1), auto_size_text=False, finalize=True)

while True:  # Event Loop
    strReceived_Croco = ''

    #Demande le json du esp32 et reçoit une liste de byte
    with SMBus(1) as bus:
        msg_Croco = i2c_msg.read(slave_address_Croco, 110)
        bus.i2c_rdwr(msg_Croco)
    
    #Transforme la ligne de byte en string
    for value in msg_Croco:
        if(value == 0x00):
            break
        else:
            strReceived_Croco += chr(value)
    
    msg_Croco = json.loads(strReceived_Croco) #Transforme la string JSON en dict pour l'utiliser en dictionnaire



    cpt = 0
    colorCpt = 0
    dictOfPairsColor = {}

    #Pour chaque connection du Json, on met un rond de couleur pour l'associer avec sa paire
    for pairs in msg_Croco['JsonData']:
        if int(pairs) == 8: #Le 8 signifit que le
            SetLED(window_Croco, str(cpt), 'black')
        elif cpt < int(pairs):
            SetLED(window_Croco, str(cpt), listColor[colorCpt])
            dictOfPairsColor[str(cpt)] = listColor[colorCpt]
            colorCpt = colorCpt + 1
        else:
            SetLED(window_Croco, str(cpt), dictOfPairsColor[pairs])

        cpt = cpt + 1
        
    event, value = window_Croco.read(timeout=400)
    if event == 'Exit' or event == sg.WIN_CLOSED:
        break
    if value is None:
        break


window_Croco.close()






