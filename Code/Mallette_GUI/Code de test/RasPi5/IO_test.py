#!/home/tge/Documents/venv/bin/python3
"""
Code: Initialisation GPIO Style library
Auteur: Louis Boisvert
Date: 2025-05-20
Description:
 ceci est le test que j'ai créer essayant de reproduire le miracle que j'avais effectuer
 il y a de cela une semaine. il est de loin le code qui se rend le plus loin
 avant d'annoncer une erreur. le test présent est uniquement input, mais pourrait facilement
 être modifier pour devenir Input et Output.
Conseil:
 1: NE PAS FAIRE CONFIANCE À CHATGPT (il ne sait franchement pas ce qu'il raconte)
 2: gardez les libraries ouvertes pour permettre de consulté ce que chaque fonction fait
  et où les trouver. Bonne Chance!
 """
import gpiod
import time

chip = "/dev/gpiochip0"

LINE = 17
LINE2 = 13


#     
#     lignes = Pins(LINE, "Input")
# 
#     lignes.Output()
#     Pins.Input( LINE2)

#     
#     def __init__ (self, pins, direction) :
#         self.pins = pins
#         self.direction = direction
#          
#     


#     def input_conf (self) :
input_conf = {
    LINE: gpiod.LineSettings(
        direction=gpiod.line.Direction.INPUT, edge_detection = gpiod.line.Edge.BOTH
        )
    }
#          return settings

#     def output_conf (self):
output_conf ={
    LINE2: gpiod.LineSettings(
        direction=gpiod.line.Direction.OUTPUT,output_value=gpiod.line.Value.ACTIVE
        )
    }
#         return settings

"""
Initialisation des pins en INPUT
"""
#     def Input (self):
Intput_Settings = gpiod.request_lines(
    str(chip),
    consumer="line-input",
    config = input_conf, 
    )

"""
Initialisation des pins en OUTPUT
"""
#     def Output (self):
Output_Settings = gpiod.request_lines(
    str(chip),
    consumer="line-output",
    config = output_conf,
    )

while True:
#     Output_Settings.set_value(LINE, gpiod.line.Value.ACTIVE)

    time.sleep(1)
    print(Intput_Settings.get_value(LINE2))
#     Output_Settings.set_value(LINE, gpiod.line.Value.INACTIVE)
    time.sleep(1)
    print(Intput_Settings.get_value(LINE2))
    

