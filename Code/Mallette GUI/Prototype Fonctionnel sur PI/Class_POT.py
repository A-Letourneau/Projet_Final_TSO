"""
Auteur : Louis Boisvert & Alexis Létourneau
Date : 2025-03-12
Environnement : Python, Thonny, raspberry pi 4, ESP32-C3-WROOM-02 Devkit, 
Brief : Cette classe représente les parties de code servant au fonctionnement
de l'énigme des potentiomètre. Elle consiste à reproduire l'onde qui est afficher
à l'écran pour la réussite de cette énigme.

- Make_WinPOT:   permet de créer l'affichage
- POT_Json :     permet de demander l'envoie d'un Json au Esp32 lié.
- Start_WinPOT : sert à la fonctionnalité de l'énigme et au calcule.

"""

#importation des library standard
from smbus2 import SMBus, i2c_msg   #Pour la communication i2c
import PySimpleGUI as sg            #Pour l'interface graphique
import json                         #Pour la manipulation des json
# Pour la generation de nombre aleatoire pour les equations et les calcules mathématiques
from random import randint          
import math
# library pour les strips de dels
import time
from rpi_ws281x import PixelStrip, Color

#importation des library créer
import I2c_Comm
import moduleDEL


class POT:
    
    #------------------- les variables statiques utilisés par l'énigme des potentiomètres -------------------#
    #Pour le graph
    SIZE_X = 200
    SIZE_Y = 100
    NUMBER_MARKER_FREQUENCY = 25
    MARGINS = 2
    
    #Valeur max des potentiomètres		Variables pas utilisé, mais toujours pratique à savoir
    MAX_POT_VAL = 4095
    
    #------------------- les varibles qui dépendent du 'main.py' ou/et qui sont utilisés dans plus d'une fonction -------------------#
    def __init__(self, SLAVE_ADDRESS_POT, DEBUG, strip):
        self.SLAVE_ADDRESS_POT = SLAVE_ADDRESS_POT
        self.DEBUG = DEBUG
        self.POTerror = False
        self.window_POT = None
        self.correctSin = True
        self.strip = strip
        
    
    def scale(self, val, src, dst):
        """
        scale the given value from the scale of src to the scale of dst.
        """
        return ((val - src[0]) / (src[1]-src[0])) * (dst[1]-dst[0]) + dst[0]

    
    def draw_axis(self):
        self.window_POT['graph'].draw_line((-self.SIZE_X,0), (self.SIZE_X, 0))                # axis lines
        self.window_POT['graph'].draw_line((0,-self.SIZE_Y), (0,self.SIZE_Y))

        for x in range(-self.SIZE_X, self.SIZE_X+1, self.NUMBER_MARKER_FREQUENCY):
            self.window_POT['graph'].draw_line((x,-3), (x,3))                       # tick marks
            if x != 0:
                self.window_POT['graph'].draw_text( str(x), (x,-10), color='green', font='Algerian 10')      # numeric labels

        for y in range(-self.SIZE_Y, self.SIZE_Y+1, self.NUMBER_MARKER_FREQUENCY):
            self.window_POT['graph'].draw_line((-3,y), (3,y))
            if y != 0:
                self.window_POT['graph'].draw_text( str(y), (-10,y), color='blue')
    
    
    def Make_WinPOT(self):
        layout_POT =[
                    [sg.Text("Forme la fonction sine correspondantes", size=(40,1), key = 'titlePOT')],
                    [sg.Graph(canvas_size=(400, 400),
                      graph_bottom_left=(-(self.SIZE_X+5), -(self.SIZE_Y+5)),
                      graph_top_right=(self.SIZE_X+5, self.SIZE_Y+5),
                      background_color='white',
                      key='graph')],
                    [sg.Text('f(x)=a*sin(p*x)+pY', font='Algerian 18')],
                    [sg.Text('a')],
                    [sg.Text('p')],
                    [sg.Text('pY')],
                ]
        return sg.Window('POT window', layout_POT, default_element_size=(12, 1), auto_size_text=False, finalize=True)
    
    
    def POT_Json(self):
        self.msg_POT = ""
        global POTerror
        
        if self.window_POT:    
            try:
                self.msg_POT = I2c_Comm.sendRequest(self.SLAVE_ADDRESS_POT, self.DEBUG)
                self.POTerror = False
                self.window_POT["titlePOT"].update(text_color = "white")
            except:
                self.window_POT["titlePOT"].update(text_color = "red")
                self.POTerror = True
                if self.DEBUG:
                    print("POT i2c ERROR")
        return self.msg_POT
    
    
    def Start_WinPOT(self):
        
        #-----------Fenêtre Interface_POT-----------#
        if self.window_POT and not self.POTerror: #Detecte si la fenetre existe puis detecte si le i2c fonctionne. L'ordre est important car si la fenetre est None, le self.POTerror existe pas
            self.window_POT['graph'].erase()
            self.draw_axis()
        
            if self.correctSin:
                sg.popup_auto_close("Find the corresponding sine wave")
                self.amplitudeGoal = randint(0,50)
                self.periodeGoal = randint(10,25)
                self.posYGoal = randint(-10,10)
                if self.DEBUG:
                    print(self.amplitudeGoal, self.periodeGoal, self.posYGoal)
                self.correctSin = False

            prev_x = prev_y = None
            for x in range(int(-self.SIZE_X/2),int(self.SIZE_X/2)):
                #f(x)=a*sin(p(x))+pY
                y = self.scale(int(self.msg_POT['JsonData']['Pot1']), (0, 4096), (0, 50)) * math.sin(self.scale(int(self.msg_POT['JsonData']['Pot2']), (0, 4096), (10, 25))/100 * x) + self.scale(int(self.msg_POT['JsonData']['Pot3']), (0, 4096), (-10, 10))
                if prev_x is not None:
                    self.window_POT['graph'].draw_line((prev_x, prev_y), (x,y), color='red')
                prev_x, prev_y = x, y
                
                #if self.amplitudeGoal-self.MARGINS <= self.scale(int(self.msg_POT['JsonData']['Pot1']), (0, 4096), (0, 50)) <= self.amplitudeGoal+self.MARGINS and self.periodeGoal-self.MARGINS <= self.scale(int(self.msg_POT['JsonData']['Pot2'], (0, 4096), (10, 25)) <= self.periodeGoal+self.MARGINS and self.posYGoal-self.MARGINS <= self.scale(int(self.msg_POT['JsonData']['Pot3']), (0, 4096), (-10, 10)) <= self.posYGoal+self.MARGINS:
                if self.amplitudeGoal-self.MARGINS <= self.scale(int(self.msg_POT['JsonData']['Pot1']), (0, 4096), (0, 50)) <= self.amplitudeGoal+self.MARGINS:
                    if self.periodeGoal-self.MARGINS <= self.scale(int(self.msg_POT['JsonData']['Pot2']), (0, 4096), (10, 25)) <= self.periodeGoal+self.MARGINS:
                        if self.posYGoal-self.MARGINS <= self.scale(int(self.msg_POT['JsonData']['Pot3']), (0, 4096), (-10, 10)) <= self.posYGoal+self.MARGINS:
                            self.correctSin = True
                            moduleDEL.colorWipe(self.strip, Color(0, 255, 0), 0)  # change la couleur des strips à vert
                            

            prev_x_goal = prev_y_goal = None
            for x in range(int(-self.SIZE_X/2),int(self.SIZE_X/2)):
                #f(x)=a*sin(p(x−pX))+pY
                #y = math.sin(x)
                y = self.amplitudeGoal * math.sin((self.periodeGoal/100)*(x)) + self.posYGoal
                if prev_x_goal is not None:
                    self.window_POT['graph'].draw_line((prev_x_goal, prev_y_goal), (x,y), color='black')
                prev_x_goal, prev_y_goal = x, y


