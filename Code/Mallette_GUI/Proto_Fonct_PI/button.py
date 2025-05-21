"""
Auteur : Louis Boisvert & Alexis Létourneau
Date : 2025-03-12
Environnement : Python, Thonny, raspberry pi 4, ESP32-C3-WROOM-02 Devkit, 
Brief : Cette class permet d'afficher la position des switch à l'écran.
Elle est constituer de quelques fonctions simples.

- Make_WinSW  : cette fonction permet de créer l'affichage de ce module
- SW_Json     : cette fonction permet de demander un Json au ESP32 liée, puis de
               modifier l'affichage en fonction de la positions des intérupteurs
- Start_WinSW : (WORK IN PROGRESS)


Cette class ne possède pas encore son énigmes. Elle sera un labyrinthe
où les intérupteurs (switch) ouvrirons ou/et fermeront des passages. (Louis)
"""
#importation des library standard
from smbus2 import SMBus, i2c_msg   #Pour la communication i2c
import PySimpleGUI as sg            #Pour l'interface graphique
import json                         #Pour la manipulation des json
# library pour les strips de del pas encore utilisé
import time
from rpi_ws281x import PixelStrip, Color

#importation des library créer
import I2c_Comm
import moduleDEL


class BTN_CLASS:

    #------------------- les varibles qui dépendent du 'main.py' ou/et qui sont utilisés dans plus d'une fonction -------------------#
    def __init__(self, switch, led, DEBUG, strip = None):
        self.DEBUG = DEBUG
        self.window = None
        self.switch = switch
        self.SIZE_X = 600
        self.SIZE_Y = 600
        self.puzzleSolved = False
        self.led = led
        self.startTime = 0
        self.strip = strip
        self.flash = True
        self.maxTime = 8

    # Crée l'interface des interrupteurs.       va futurement faire le labyrinthe
    def Make_WinBTN(self):
        self.startTime = int(time.time())
        layout_SW = [
                        [sg.VPush()],
                        [sg.Push(), sg.Text("",  key = "countDown", size=(17,1), font='Algerian 15', justification = "center"), sg.Push()],
                        [sg.Push(), sg.Text("Appuyez sur le bouton, vous avez :", size=(50,1), font='Algerian 20', justification = "center") ,sg.Push()],
                        [sg.Push(), sg.Text("", key = "countDownBTN", size=(10,1), font='Algerian 20', justification = "center") ,sg.Push()],
                        [sg.Push(), sg.Graph(canvas_size=(self.SIZE_X, self.SIZE_Y), graph_bottom_left=(0,0), graph_top_right=(self.SIZE_X, self.SIZE_Y), key='button'), sg.Push()],
                        [sg.VPush()]
                     ]

        return sg.Window('Fenetre interrupteurs', layout_SW, default_element_size=(12, 1), auto_size_text=False, no_titlebar = True, finalize=True)
        

    #lecture de Json et Update de l'affichage
    def doButton(self):
        if self.window:
            self.led.value = True
            
            if (self.startTime - int(time.time()) + self.maxTime) < 0:
                self.puzzleSolved = "Fail"
            
            self.window['countDownBTN'].update(str((self.startTime - int(time.time()) + 8)))
            if self.switch.value:
                self.window['button'].draw_circle((self.SIZE_X/2, self.SIZE_Y/2), 100 , fill_color="dark red", line_color="black", line_width=10)
                self.window['button'].draw_text( "STOP" , (self.SIZE_X/2, self.SIZE_Y/2), font=20)
                
                
                if self.flash:
                    moduleDEL.colorWipe(self.strip, Color(255, 0, 0), 0)  # Red wipe
                    self.flash = False
                else:
                    moduleDEL.colorWipe(self.strip, Color(0, 255, 0), 0)  # Red wipe
                    self.flash = True
            else:
                self.window['button'].draw_circle((self.SIZE_X/2, self.SIZE_Y/2), 100 , fill_color="red", line_color="black", line_width=10)
                self.window['button'].draw_text( "STOP" , (self.SIZE_X/2, self.SIZE_Y/2), font=20)
                self.puzzleSolved = True
            
            
        

                    
                        

           

