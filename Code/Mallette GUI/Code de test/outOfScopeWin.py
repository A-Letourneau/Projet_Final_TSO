import PySimpleGUI as sg
import time
import random
import exempleModule

window = exempleModule.makeWin()

while True:
    exempleModule.doSw(window=window)
    event, value = window.read(timeout=50)
    if event == 'Exit' or event == sg.WIN_CLOSED:
        break
    if value is None:
        break
    
window.close()
