"""
Auteur : Alexis Létourneau
Date : 2024-12-03
Environnement : Python, Thonny, raspberry pi 4, ESP32-C3-WROOM-02 Devkit, 
Brief : Programme qui affiche les données reçu par la communication i2c de 3 esp32 externes en mode Sub et qui affiche leurs donnees avec interface PySimpleGUI.
Ce programme communique en i2c en mode Main avec les 3 esp32 en mode Sub. 
Les 3 esp32 ont des objets interactifs (potentiomètres, boutons, interrupteurs) différents, 
Celui nommé SW contient quatre boutons
Celui nommé POT contient 3 potentiomètres et 2 interrupteurs.
Celui nomme Croco est 8 entrees qui transmet si deux des entrees sont interconnecte.
Les lectures de ces objets sont transmises par JSON à la demande du Main à toutes les 75ms (25ms par esp32).


Les 3 esp32 ont une interface chaque, qui contient des "widget" qui représentent leurs états.
L'interface POT utilise deux images d'interrupteurs pointant vers la gauche ou la droite fait en base64, ce qui permet d'avoir le fichier de l'image dans le fichier py directement. 
et utilise des "ProgressBar" pour montrer l'état des potentiomètres.
L'interface SW utilise des cercles de couleur rouge et vert pour démontrer l'état des boutons.
L'interface Croco utilise des cercles de couleurs pour montrer qu'elle entrees du esp32 est interconnectee.
Quand on ferme une des fenêtres, les deux se ferme.

"""

from smbus2 import SMBus, i2c_msg   #Pour la communication i2c
import PySimpleGUI as sg            #Pour l'interface graphique
import json                         #Pour la manipulation des json
from time import sleep

#Les deux images d'interrupteurs en base 64
TOGGLE_SW_OFF = b'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'
TOGGLE_SW_ON = b'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'

#Les addresses des Sub
SLAVE_ADDRESS_Croco = 0x0b
SLAVE_ADDRESS_SW = 0x0a
SLAVE_ADDRESS_POT = 0x09

#Valeur max des potentiomètres
MAX_POT_VAL = 4095

#Nombre d'entrées Croco
NB_CROCO = 4
#Couleur des paires de Croco
listColor = ["green","pink","yellow","cyan"]

#Nombre de Switch
NB_SW = 8

#La valeur de refresh en ms
REFRESH_RATE = 50

DEBUG = False
#Crée un graph pour contenir un rond de couleur
def LEDIndicator(key=None, radius=30):
    return sg.Graph(canvas_size=(radius, radius),
             graph_bottom_left=(-radius, -radius),
             graph_top_right=(radius, radius),
             pad=(0, 0), key=key)

#Efface puis crée un rond de couleur pour représenter l'état des boutons
def SetLED(window, key, color):
    graph = window[key]
    graph.erase()
    graph.draw_circle((0, 0), 35, fill_color=color, line_color=color)



#Les layout et activation des fenêtres
layout_SW = [
                [sg.Text('My SW Status Indicators', size=(20,1), key = "titleSW")],
                [sg.Text('Sw1'),  sg.Text('Sw2'),  sg.Text('Sw3'),  sg.Text('Sw4'),   sg.Text('Sw5'),   sg.Text('Sw6'),   sg.Text('Sw7'),   sg.Text('Sw8'),],
                [
                    sg.Image(source=TOGGLE_SW_OFF, key="Sw1"),sg.Image(source=TOGGLE_SW_OFF, key="Sw2"),sg.Image(source=TOGGLE_SW_OFF, key="Sw3"),sg.Image(source=TOGGLE_SW_OFF, key="Sw4"),
                    sg.Image(source=TOGGLE_SW_OFF, key="Sw5"),sg.Image(source=TOGGLE_SW_OFF, key="Sw6"),sg.Image(source=TOGGLE_SW_OFF, key="Sw7"),sg.Image(source=TOGGLE_SW_OFF, key="Sw8")
                ],
                [sg.Button('Exit')]
             ]


window_SW = sg.Window('SW window', layout_SW, default_element_size=(12, 1), auto_size_text=False, finalize=True)
window_SW.BackgroundColor = "red"

layout_POT =    [
                    [sg.Text('My Pot Indicators', size=(20,1), key = "titlePOT")],
                    [sg.Text('Pot1'), sg.Text('Pot2')],
                    [sg.ProgressBar(MAX_POT_VAL, key='Pot1'), sg.ProgressBar(MAX_POT_VAL, key='Pot2')],
                    [sg.Button('Exit')]
                ]


window_POT = sg.Window('POT window', layout_POT, default_element_size=(12, 1), auto_size_text=False, finalize=True)

layout_Croco =[
                [sg.Text('My croco indicator', size=(20,1), key = "titleCroco")],
                [sg.Text('Croco 1'),  sg.Text('Croco 2'),  sg.Text('Croco 3'), sg.Text('Croco 4')],
                [LEDIndicator('0'), LEDIndicator('1'), LEDIndicator('2'), LEDIndicator('3')],
                [LEDIndicator('4'), LEDIndicator('5'), LEDIndicator('6'), LEDIndicator('7')],          
                [sg.Text('Croco 5'),  sg.Text('Croco 6'),  sg.Text('Croco 7'), sg.Text('Croco 8')],
                [sg.Button('Exit')]
              ]

window_Croco = sg.Window('Croco window', layout_Croco, default_element_size=(12, 1), auto_size_text=False, finalize=True)

#Brief : Une fonction qui envoit une demande de donnée à l'adresse d'un esp32 
#Param : L'adresse i2c du esp32
def sendRequest(SlaveAddresse):
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

#Boucle principale
while True: 

#Essaye de lire les json des esp32 et met un message d'erreur s'il n'y parvient pas
    try:
        msg_SW = sendRequest(SLAVE_ADDRESS_SW)
        SWerror = False
        window_SW["titleSW"].update(text_color = "white")
    except:
        window_SW["titleSW"].update(text_color = "red")
        SWerror = True
        if DEBUG:
            print("SW i2c ERROR")
              
    try:
        msg_POT = sendRequest(SLAVE_ADDRESS_POT)
        POTerror = False
        window_POT["titlePOT"].update(text_color = "white")
    except:
        window_POT["titlePOT"].update(text_color = "red")
        POTerror = True
        if DEBUG:
            print("POT i2c ERROR")
        
    try:
        msg_Croco = sendRequest(SLAVE_ADDRESS_Croco)
        Crocoerror = False
        window_Croco["titleCroco"].update(text_color = "white")
    except:
        window_Croco["titleCroco"].update(text_color = "red")
        Crocoerror = True
        if DEBUG:
            print("Croco i2c ERROR")    
    
    #-------------Lcture des boutons des fenetres--------------#
    window, event, value = sg.read_all_windows(timeout = REFRESH_RATE)
    
    if event == 'Exit' or event == sg.WIN_CLOSED: #Si on ferme une fenetre on ferme toutes les fenetres
        break
    
    #-----------Fenêtre Interface Croco-----------#
    if not Crocoerror:
        cpt = 0 #La paire de Croco actuel
        colorCpt = 0 #la couleur de paire actuel
        dictOfPairsColor = {} #Pour mettre la couleur en memoire pour la deuxieme fois qu'on voit la paire
        #Pour chaque connection du Json, on met un rond de couleur pour l'associer avec sa paire
        for pairs in msg_Croco['JsonData']:
            if int(pairs) == NB_CROCO: #Le 8 signifit qu'il n'y pas de connection
                SetLED(window_Croco, str(cpt), 'black')
            elif cpt < int(pairs): #Si c'est la premiere fois qu'on voit cette paire
                SetLED(window_Croco, str(cpt), listColor[colorCpt]) #On met le rond de couleur a la position cpt en une des 4 couleurs possible en ordre
                dictOfPairsColor[str(cpt)] = listColor[colorCpt]	#On met la couleur en memoire pour la deuxieme fois qu'on voit la paire
                colorCpt = colorCpt + 1 #On passe a la prochaine couleur
            else:  #Si c'est la deuxieme fois qu'on voit cette paire
                SetLED(window_Croco, str(cpt), dictOfPairsColor[pairs])

            cpt = cpt + 1

    #-----------Fenêtre Interface_POT-----------#
    if not POTerror:
        #Met à jour le progrèe du "ProgressBar" selon l'état des potentiomètes
        window_POT["Pot1"].update(current_count = int(msg_POT['JsonData']['Pot1']))
        window_POT["Pot2"].update(current_count = int(msg_POT['JsonData']['Pot2']))


        #-----------Fenêtre Interface_SW-----------#
    if not SWerror:
        for curSw in range(NB_SW): #Pour chaque switch, on change l'image de la switch selon son état
            if msg_SW['JsonData'][f'Sw{curSw + 1}'] == '1':
                window_SW[f'Sw{curSw + 1}'].update(source=TOGGLE_SW_ON)
            else:
                window_SW[f'Sw{curSw + 1}'].update(source=TOGGLE_SW_OFF)

    
#À la fin du programme, on ferme les fenêtres
window_SW.close()
window_POT.close()
window_Croco.close()
