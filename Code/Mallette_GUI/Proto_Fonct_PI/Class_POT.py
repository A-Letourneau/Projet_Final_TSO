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
    #------------------- les variables qui dépendent du 'main.py' ou/et qui sont utilisés dans plus d'une fonction -------------------#
    def __init__(self, SLAVE_ADDRESS_POT, DEBUG, strip, GOAL_COR_ANSWER = 0):
        self.SLAVE_ADDRESS_POT = SLAVE_ADDRESS_POT
        self.DEBUG = DEBUG
        self.POTerror = False
        self.window_POT = None
        self.correctSin = True
        self.firstTime = True
        self.strip = strip
        self.curCorAnswer = 0
        self.GOAL_COR_ANSWER = GOAL_COR_ANSWER
        self.puzzleSolved = False
        
        self.MAX_POT_VAL = 4000
        self.POT_MIN_1 = 50
        self.POT_MIN_2 = 50
        self.POT_MIN_3 = 50
        
        self.MAX_AMPLITUDE = 50
        self.MIN_AMPLITUDE = 5
        
        self.MAX_PERIODE = 10
        self.MIN_PERIODE = 1
        
        self.MAX_POSY = 10
        self.MIN_POSY = -10
        
        #Pour le graph
        self.SIZE_X = 200
        self.SIZE_Y = 100
        self.NUMBER_MARKER_FREQUENCY = 50
        self.MARGINS = 2
        
        self.minDEL = 0
        self.maxDEL = 17
        
    def resetPuzzle(self):
        self.POTerror = False
        self.correctSin = True
        self.firstTime = True
        self.curCorAnswer = 0
        self.puzzleSolved = False
        
    def scale(self, val, src, dst):
        """
        self.scale the given value from the self.scale of src to the self.scale of dst.
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
                    [sg.VPush()],
                    [sg.Push(), sg.Text("",  key = "countDown", size=(17,1), font='Algerian 15', justification = "center"), sg.Push()],
                    [sg.Push(), sg.Text(f"Forme la fonction sine correspondante {self.curCorAnswer}/{self.GOAL_COR_ANSWER}", size=(42,1), key = 'titlePOT', font='Algerian 20', justification = "center"), sg.Push()],
                    [sg.Push(), sg.Text("Utilise les trois potentiomètres glissants\npour ajuster l'amplitude, la période et la position en y", size=(70,2), key = 'titlePOT', font='Algerian 18', justification = "center"), sg.Push()],                        
                    [sg.Push(), sg.Graph(canvas_size=(600, 600), graph_bottom_left=(-(self.SIZE_X+5), -(self.SIZE_Y+5)), graph_top_right=(self.SIZE_X+5, self.SIZE_Y+5), background_color='white', key='graph'), sg.Push(),],
                    [sg.Push(), sg.Text('f(x)=a*sin(p*x)+pY', font='Algerian 18', key='equation', size=(30,1)), sg.Push()],
                    [sg.VPush()]
                ]
        return sg.Window('POT window', layout_POT, default_element_size=(12, 1), auto_size_text=False, finalize=True, keep_on_top=True)
    
    
    def POT_Json(self):
        self.msg_POT = ""
        global POTerror
        
        if self.window_POT:    
            try:
                self.msg_POT = I2c_Comm.sendRequest(self.SLAVE_ADDRESS_POT, self.DEBUG)
                self.POTerror = False
                self.window_POT["titlePOT"].update(text_color = None)
            except:
                self.window_POT["titlePOT"].update(text_color = "red")
                self.POTerror = True
                if self.DEBUG:
                    print("POT i2c ERROR")
        return self.msg_POT
    
    
    def doWinPot(self):
        
        #-----------Fenêtre Interface_POT-----------#
        if self.window_POT and not self.POTerror: #Detecte si la fenetre existe puis detecte si le i2c fonctionne. L'ordre est important car si la fenetre est None, le self.POTerror existe pas
            
            
            amplitude = self.scale(int(self.msg_POT['JsonData']['Pot2']), (self.POT_MIN_1, self.MAX_POT_VAL), (self.MIN_AMPLITUDE, self.MAX_AMPLITUDE))
            periode = self.scale(int(self.msg_POT['JsonData']['Pot3']), (self.POT_MIN_2, self.MAX_POT_VAL), (self.MIN_PERIODE, self.MAX_PERIODE)) / 100
            posY = self.scale(int(self.msg_POT['JsonData']['Pot1']), (self.POT_MIN_3, self.MAX_POT_VAL), (self.MIN_POSY, self.MAX_POSY))
            self.window_POT['titlePOT'].update(f"Forme la fonction sine correspondantes {self.curCorAnswer}/{self.GOAL_COR_ANSWER}")
            self.window_POT['equation'].update(f"f(x)={int(amplitude)}*sin({periode:.3f})*x)+{int(posY)}")
            self.window_POT['graph'].erase()
            self.draw_axis()

            if self.correctSin or self.firstTime:
                self.amplitudeGoal = randint(self.MIN_AMPLITUDE, self.MAX_AMPLITUDE)
                self.periodeGoal = randint(self.MIN_PERIODE, self.MAX_PERIODE)
                self.posYGoal = randint(self.MIN_POSY, self.MAX_POSY)
                if self.DEBUG:
                    print(self.amplitudeGoal, self.periodeGoal, self.posYGoal)
                self.correctSin = False
                if not self.firstTime:
                    
                    prev_x = prev_y = None
                    for x in range(int(-self.SIZE_X),int(self.SIZE_X)):
                        #f(x)=a*sin(p(x))+pY
                        y = amplitude * math.sin(periode * x) + posY
                        if prev_x is not None:
                            self.window_POT['graph'].draw_line((prev_x, prev_y), (x,y), color='green', width=5)
                        prev_x, prev_y = x, y
                        
                    self.window_POT.read(timeout=0)
                    time.sleep(3)
#                     moduleDEL.colorWipe(self.strip, Color(0, 0, 0), 0)  # change la couleur des strips à vert
                    self.curCorAnswer += 1
                    if self.GOAL_COR_ANSWER == self.curCorAnswer:
                        self.puzzleSolved = True
                        moduleDEL.colorInBetween(self.strip, Color(0, 255, 0),self.minDEL,self.maxDEL) 
                        sg.popup_auto_close('Énigme réussi!!', auto_close_duration=3, font='Algerian 20')
                else:
                    self.firstTime = False
            
            if self.amplitudeGoal - self.MARGINS <= amplitude <= self.amplitudeGoal + self.MARGINS:
                if self.periodeGoal - self.MARGINS <= periode * 100 <= self.periodeGoal  + self.MARGINS:
                    if self.posYGoal - self.MARGINS <= posY <= self.posYGoal + self.MARGINS:
                        self.correctSin = True


            prev_x_goal = prev_y_goal = None
            for x in range(int(-self.SIZE_X),int(self.SIZE_X)):
                #f(x)=a*sin(p(x−pX))+pY
                #y = math.sin(x)
                y = self.amplitudeGoal * math.sin((self.periodeGoal/100)*(x)) + self.posYGoal
                if prev_x_goal is not None:
                    self.window_POT['graph'].draw_line((prev_x_goal, prev_y_goal), (x,y), color='black', width=10)
                prev_x_goal, prev_y_goal = x, y


            prev_x = prev_y = None
            for x in range(int(-self.SIZE_X),int(self.SIZE_X)):
                #f(x)=a*sin(p(x))+pY
                y = amplitude * math.sin(periode * x) + posY
                if prev_x is not None:
                    self.window_POT['graph'].draw_line((prev_x, prev_y), (x,y), color='red', width=5)
                prev_x, prev_y = x, y
