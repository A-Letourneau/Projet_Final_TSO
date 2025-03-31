#!/usr/bin/env python
import PySimpleGUI as sg
import json

"""
    Demo program showing how to create your own "LED Indicators"
    The LEDIndicator function acts like a new Element that is directly placed in a window's layout
    After the Window is created, use the SetLED function to access the LED and set the color
    
    Copyright 2023 PySimpleSoft, Inc. and/or its licensors. All rights reserved.
    
    Redistribution, modification, or any other use of PySimpleGUI or any portion thereof is subject to the terms of the PySimpleGUI License Agreement available at https://eula.pysimplegui.com.
    
    You may not redistribute, modify or otherwise use PySimpleGUI or its contents except pursuant to the PySimpleGUI License Agreement.

"""

#strReceived_Croco = '{"NomEsp32":"I2C_Croco","JsonData":["3","7","5","0","2","8","8","1"]}'
strReceived_Croco = '{"NomEsp32":"I2C_Croco","JsonData":["8","8","8","8","8","8","8","8"]}'

listColor = ['green', 'pink', 'yellow', 'cyan']
def LEDIndicator(key=None, radius=30):
    return sg.Graph(canvas_size=(radius, radius),
             graph_bottom_left=(-radius, -radius),
             graph_top_right=(radius, radius),
             pad=(0, 0), key=key)

def SetLED(window, key, color):
    graph = window[key]
    graph.erase()
    graph.draw_circle((0, 0), 25, fill_color=color, line_color=color)

layout = [[sg.Text('My croco indicator', size=(20,1))],
          [sg.Text('Croco 1'),  sg.Text('Croco 2'),  sg.Text('Croco 3'), sg.Text('Croco 4')],
          [LEDIndicator('0'), LEDIndicator('1'), LEDIndicator('2'), LEDIndicator('3')],
          [LEDIndicator('4'), LEDIndicator('5'), LEDIndicator('6'), LEDIndicator('7')],          
          [sg.Text('Croco 5'),  sg.Text('Croco 6'),  sg.Text('Croco 7'), sg.Text('Croco 8')],
          [sg.Button('Exit')]]

window_Croco = sg.Window('My new window', layout, default_element_size=(12, 1), auto_size_text=False, finalize=True)

msg_Croco = json.loads(strReceived_Croco)

cpt = 0
colorCpt = 0
dictOfPairsColor = {}
for pairs in msg_Croco['JsonData']:
    if int(pairs) == 8:
        SetLED(window_Croco, str(cpt), 'black')
    elif cpt < int(pairs):
        SetLED(window_Croco, str(cpt), listColor[colorCpt])
        dictOfPairsColor[str(cpt)] = listColor[colorCpt]
        #SetLED(window_Croco, pairs, 'listColor[colorCpt]')
        colorCpt = colorCpt + 1 
    else:
        SetLED(window_Croco, str(cpt), dictOfPairsColor[pairs]) 

    cpt = cpt + 1

while True:  # Event Loop
    event, value = window_Croco.read(timeout=400)
    if event == 'Exit' or event == sg.WIN_CLOSED:
        break
    if value is None:
        break

window_Croco.close()
