import PySimpleGUI as sg            #Pour l'interface graphique
import json                         #Pour la manipulation des json
from time import sleep
from random import randint



#Nombre d'entrées Croco
NB_CROCO = 8
#Couleur des paires de Croco
listColor = ["green","pink","yellow","cyan"]

NB_GOOD_ANSWER_REQ = 3

#Crée un graph pour contenir un rond de couleur
def LEDIndicator(key=None, radius=100):
    return sg.Graph(canvas_size=(radius, radius),
             graph_bottom_left=(-radius, -radius),
             graph_top_right=(radius, radius),
             pad=(0, 0), key=key)

#Efface puis crée un rond de couleur pour représenter l'état des boutons
def SetLED(window, key, color):
    graph = window[key]
    graph.erase()
    graph.draw_circle((0, 0), 75, fill_color=color, line_color=color)
    graph.draw_text( str((int(key) + 1)) , (0, 0), font=14)


layout_Croco =[
                [sg.Text('My croco indicator', size=(20,1))],

                [sg.Graph(canvas_size=(400, 100),
                    graph_bottom_left=(0, 0),
                    graph_top_right=(400, 100),
                    pad=(0, 0), key="equationGraph")],
                 
                [sg.Text('Croco 1'),  sg.Text('Croco 2'),  sg.Text('Croco 3'), sg.Text('Croco 4')],
                [LEDIndicator('0'), LEDIndicator('1'), LEDIndicator('2'), LEDIndicator('3')],
                [LEDIndicator('4'), LEDIndicator('5'), LEDIndicator('6'), LEDIndicator('7')],          
                [sg.Text('Croco 5'),  sg.Text('Croco 6'),  sg.Text('Croco 7'), sg.Text('Croco 8')],
                [sg.Button('Exit')]
              ]

window_Croco = sg.Window('Croco window', layout_Croco, default_element_size=(12, 1), auto_size_text=False, finalize=True)


randomInt1 = randint(1,8)
randomInt2 = randint(1,7)
goodAnswer = 0
#Boucle principale
while True: 

    answer = 0
    msg_Croco = {"JsonData" : ['1','0','3','2','5','4','7','6']}
    event, value = window_Croco.read(timeout=25) #Attend 25ms pour voir si on appuis sur le bouton "exit". Si oui, on quitte la boucle
    if event == 'Exit' or event == sg.WIN_CLOSED:
        break
    if value is None:
        break

    #-----------Fenêtre Interface Croco-----------#
    cpt = 0 #La paire de Croco actuel
    colorCpt = 0 #la couleur de paire actuel
    dictOfPairsColor = {} #Pour mettre la couleur en memoire pour la deuxieme fois qu'on voit la paire
    #Pour chaque connection du Json, on met un rond de couleur pour l'associer avec sa paire
    for pairs in msg_Croco['JsonData']:
        if int(pairs) == NB_CROCO: #Le 8 signifit qu'il n'y pas de connection
            SetLED(window_Croco, str(cpt), 'white')
        elif cpt < int(pairs): #Si c'est la premiere fois qu'on voit cette paire
            SetLED(window_Croco, str(cpt), listColor[colorCpt]) #On met le rond de couleur a la position cpt en une des 4 couleurs possible en ordre
            dictOfPairsColor[str(cpt)] = listColor[colorCpt]	#On met la couleur en memoire pour la deuxieme fois qu'on voit la paire
            colorCpt = colorCpt + 1 #On passe a la prochaine couleur
            answer += (cpt + 1) + (int(pairs) + 1)
        else:  #Si c'est la deuxieme fois qu'on voit cette paire
            SetLED(window_Croco, str(cpt), dictOfPairsColor[pairs])
        cpt = cpt + 1

    window_Croco["equationGraph"].erase()
    window_Croco["equationGraph"].draw_text(f"{randomInt1}+{randomInt2}={answer}", (150,50), font=("Comic", 50))
    
    
    if answer == randomInt1 + randomInt2:
        sg.popup('CORRECT')
        randomInt1 = randint(1,8)
        randomInt2 = randint(1,7)
        goodAnswer += 1
        if goodAnswer < NB_GOOD_ANSWER_REQ:
            break
#À la fin du programme, on ferme les fenêtres

        sg.popup('CORRECT', image="congratulations-evangelion.gif")
window_Croco.close()
