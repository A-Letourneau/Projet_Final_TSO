"""
Auteur : Louis Boisvert & Alexis Létourneau
Date : 2025-03-11
Environnement : Python, Thonny, raspberry pi 4, ESP32-C3-WROOM-02 Devkit, 
Brief : Cette Class représentes l'énigmes des fils bananes que l'on a renommé à Croco
par simplicité.

- la fonction "Croco_Json" appel le fichier I2c_Comm ce qui permet de récupérer
les informations du esp32 servant à l'énigme Croco
- la fonction "Make_WinCroco" crée l'interface utilisateur
- la fonction "Start_WinCroco" est la portion de code qui va gérer l'énigme grâce au
information récupérer par "Croco_Json".

Commentaire : la vérification de la réussite des utilisateur pourrait être dans
sa propre fonction
(Louis)

"""

from smbus2 import SMBus, i2c_msg   #Pour la communication i2c
import PySimpleGUI as sg            #Pour l'interface graphique
import json                         #Pour la manipulation des json
from random import randint          #Pour la generation de nombre aleatoire pour les equations
import math
import board
import neopixel
from digitalio import DigitalInOut, Direction, Pull

import I2c_Comm



class Croco:
    
    #------------------- les variables statiques utilisés par l'énigme des fils bananes -------------------#
    #Nombre d'entrées Croco
    NB_CROCO = 8
    #Couleur des paires de Croco
    listColor = ["purple","pink","yellow","cyan"]
    
    #------------------- les varibles qui dépendent du 'main.py' ou/et qui sont utilisés dans plus d'une fonction -------------------#
    def __init__(self, LIST_OPERATIVE, SLAVE_ADDRESS_Croco, DEBUG):
        self.LIST_OPERATIVE = LIST_OPERATIVE
        self.SLAVE_ADDRESS_Croco = SLAVE_ADDRESS_Croco
        self.DEBUG = DEBUG
        self.Crocoerror = False
        self.window_Croco = None
    

    #Crée un graph pour contenir un rond de couleur
    def DrawRGB(self, key=None, radius=100):
        return sg.Graph(canvas_size=(radius, radius),
                 graph_bottom_left=(-radius, -radius),
                 graph_top_right=(radius, radius),
                 pad=(0, 0), key=key)


    #Efface puis crée un rond de couleur pour représenter l'état des boutons
    def SetRGB(self, window, key, color):
        graph = window[key]
        graph.erase()
        graph.draw_circle((0, 0), 75, fill_color=color, line_color=color)
        graph.draw_text( str((int(key) + 1)) , (0, 0), font=14)
     
     
    #essaie la communication I2c et la reception des donnees (louis)
    def Croco_Json(self):
        global Crocoerror
        self.msg_Croco = ""
        if self.window_Croco: 
            try:
                self.msg_Croco = I2c_Comm.sendRequest(self.SLAVE_ADDRESS_Croco, self.DEBUG)
                Crocoerror = False
                self.window_Croco["titleCroco"].update(text_color = "white")
            except:
                self.window_Croco["titleCroco"].update(text_color = "red")
                Crocoerror = True
                if self.DEBUG:
                    print("Croco i2c ERROR")
        return self.msg_Croco
   
   
    #crée l'interface utilisateur pour l'énigme Croco 
    def Make_WinCroco(self):
        layout_Croco =[
                        [sg.Text(f"Nombre d'équation restante 0/{len(self.LIST_OPERATIVE)}", size=(40,1), key = 'titleCroco')],
                        [sg.Graph(canvas_size=(500, 100),
                            graph_bottom_left=(0, 0),
                            graph_top_right=(500, 100),
                            pad=(0, 0), key="equationGraph")],
                        [sg.Text('Croco 1'),  sg.Text('Croco 2'),  sg.Text('Croco 3'), sg.Text('Croco 4')],
                        [self.DrawRGB('0'), self.DrawRGB('1'), self.DrawRGB('2'), self.DrawRGB('3')],
                        [self.DrawRGB('4'), self.DrawRGB('5'), self.DrawRGB('6'), self.DrawRGB('7')],          
                        [sg.Text('Croco 5'),  sg.Text('Croco 6'),  sg.Text('Croco 7'), sg.Text('Croco 8')],
                        [sg.Button('Exit')]
                      ]
        return sg.Window('Croco window', layout_Croco, default_element_size=(12, 1), auto_size_text=False, finalize=True)


    #cette fonction est le coeur de l'énigme. c'est ici que l'utilisateur va pouvoir essayer de résoudre l'énigme.
    def Start_WinCroco(self):
        global Crocoerror
       #-----------Fenêtre Interface Croco-----------#
        if self.window_Croco and not Crocoerror: #Detecte si la fenetre existe puis detecte si le i2c fonctionne. L'ordre est important car si la fenetre est None, le Crocoerror n'existe pas
            curCroco = 0 #La paire de Croco actuel
            colorCpt = 0 #la couleur de paire actuel
            dictOfPairsColor = {} #Pour mettre la couleur en memoire pour la deuxieme fois qu'on voit la paire
            answer = 0 #Reponse de l'usager
            
            #Initiation du jeu d'equation
            firstEquation = True #Pour savoir qu'il faut trouver une premiere reponse aleatoire
            randomAnswer = 0 #La reponse aleatoire
            goodAnswer = 0 #Nombre de bonnes reponses
            
            #Pour chaque connection du Json, on met un rond de couleur pour l'associer avec sa paire
            for pairs in self.msg_Croco['JsonData']:
                if int(pairs) == self.NB_CROCO: #Le 8 signifit qu'il n'y pas de connection
                    self.SetRGB(self.window_Croco, str(curCroco), 'white')
                elif curCroco < int(pairs): #Si c'est la premiere fois qu'on voit cette paire
                    self.SetRGB(self.window_Croco, str(curCroco), self.listColor[colorCpt]) #On met le rond de couleur a la position curCroco en une des 4 couleurs possible en ordre
                    dictOfPairsColor[str(curCroco)] = self.listColor[colorCpt]#On met la couleur en memoire pour la deuxieme fois qu'on voit la paire
                    colorCpt = colorCpt + 1 #On passe a la prochaine couleur
                    
                    if self.LIST_OPERATIVE[goodAnswer] == "+": #Fait la bonne operation selon l'operation, mais additionne toujours les paires
                        answer += (curCroco + 1) + (int(pairs) + 1)
                    elif self.LIST_OPERATIVE[goodAnswer] == "-":
                        answer += (int(pairs) + 1) - (curCroco + 1)
                    elif self.LIST_OPERATIVE[goodAnswer] == "x":
                        answer += (curCroco + 1) * (int(pairs) + 1)
                    elif self.LIST_OPERATIVE[goodAnswer] == "/":
                        answer += (int(pairs) + 1) / (curCroco + 1)
                    
                else:  #Si c'est la deuxieme fois qu'on voit cette paire
                    try: #
                        self.SetRGB(self.window_Croco, str(curCroco), dictOfPairsColor[pairs])
                    except:
                        if self.DEBUG:
                            self.SetRGB(self.window_Croco, str(curCroco), "red")
                            
                curCroco = curCroco + 1

            self.window_Croco["equationGraph"].erase()
            if self.LIST_OPERATIVE[goodAnswer] != "/": #Pour afficher la reponse voulu, la reponse de l'utilisateur et l'operation actuelle
                self.window_Croco["equationGraph"].draw_text(f"{randomAnswer}={answer} ({self.LIST_OPERATIVE[goodAnswer]})", (200,50), font=("Comic", 50))
            else: #Pour afficher un bon nombre de decimal des float
                self.window_Croco["equationGraph"].draw_text(f"{randomAnswer:5.3f}={answer:5.3f} ({self.LIST_OPERATIVE[goodAnswer]})", (200,50), font=("Comic", 30))        
                    
            if firstEquation or answer == randomAnswer: 
                if not firstEquation:
                    goodAnswer += 1
                    sg.popup_no_titlebar('CORRECT', auto_close_duration = 1, auto_close = True)
                    self.window_Croco["titleCroco"].update(f"Nombre d'équation restante {goodAnswer}/{len(self.LIST_OPERATIVE)}")
                else:
                    firstEquation = False

                if goodAnswer == len(self.LIST_OPERATIVE): #Lorsque l'user a finit les questions
                    sg.popup_no_titlebar('REUSSI', auto_close_duration = 1, auto_close = True)
                    goodAnswer = 0
                    firstEquation = True
                    self.window_Croco["titleCroco"].update(f"Nombre d'équation restante {goodAnswer}/{len(self.LIST_OPERATIVE)}")
                    
                #Tout les reponses aleatoires doivent etre different de l'ancien pour ne pas resoudre immediatement
                elif self.LIST_OPERATIVE[goodAnswer] == "+":
                    while True:
                        NewRandomAnswer = randint(3,15)
                        if NewRandomAnswer != randomAnswer:
                            randomAnswer = NewRandomAnswer
                            break
                        
                elif self.LIST_OPERATIVE[goodAnswer] == "-":
                    while True:
                        NewRandomAnswer = randint(1,7)
                        if NewRandomAnswer != randomAnswer:
                            randomAnswer = NewRandomAnswer
                            break
                        
                elif self.LIST_OPERATIVE[goodAnswer] == "x":
                    while True:
                        NewRandomAnswer = randint(1,8)
                        NewRandomAnswer2 = randint(1,8)
                        if randomAnswer != NewRandomAnswer * NewRandomAnswer2 and NewRandomAnswer != NewRandomAnswer2: #Un nombre qui n'est pas carre
                            randomAnswer = NewRandomAnswer * NewRandomAnswer2
                            break
                        
                elif self.LIST_OPERATIVE[goodAnswer] == "/":
                    while True:
                        NewRandomAnswer = randint(2,8)
                        NewRandomAnswer2 = randint(2,8)
                        if NewRandomAnswer2 < NewRandomAnswer and randomAnswer != NewRandomAnswer * NewRandomAnswer2 and NewRandomAnswer != NewRandomAnswer2: #Un nombre qui n'est pas 1 et pas plus petit que zero
                            randomAnswer = NewRandomAnswer / NewRandomAnswer2
                            break
