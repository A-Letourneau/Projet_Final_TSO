"""
Test Créer par Louis Boisvert
Date : 2025-04-14
Objectif: changer la couleur des Frames

Résultats :
Il est UNIQUEMENT possible de changer la couleur des objets à l’intérieur des frames après la création de la fenêtre.
Il est possible d’établir une couleur d’arrière-plan de base pour un Frame,
mais il sera impossible de la modifier une fois que la fenêtre aura été créée (affichée à l’écran).

Donc, deux solutions s’offrent à nous :
1. Fermer la fenêtre et la recréer avec des couleurs différentes.
2. Changer uniquement la couleur des objets.
"""

import PySimpleGUI as sg

layout = [
    [sg.Frame("My Frame", [[sg.Text("Hi", key="Text1")]], key="Frame1")],
    [sg.Button("Change Color")]
]

window = sg.Window("Frame Color Test", layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == "Change Color":
        window["Text1"].update(background_color="lightgreen")
