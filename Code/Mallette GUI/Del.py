"""
Auteur : Louis Boisvert & Alexis Létourneau
Date : 2025-03-11
Environnement : Python, Thonny, raspberry pi 4, ESP32-C3-WROOM-02 Devkit, 
Brief : library permettant l'utilisation des dels adressables et leurs fonctionnements

Commentaire : cette library va bientôt être obselète, car neopixel ne soutient
pas plusieurs dels addressables
(Louis)
"""

from smbus2 import SMBus, i2c_msg   #Pour la communication i2c
import PySimpleGUI as sg            #Pour l'interface graphique
from random import randint          #Pour la generation de nombre aleatoire pour les equations
import math
import board
import neopixel
from digitalio import DigitalInOut, Direction, Pull
from time import sleep



def ActiveLED(DEL_ACTIVE, num_pixels, pixel_pin, ORDER):
    if DEL_ACTIVE:
        pixels = neopixel.NeoPixel(
            pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
        )
        """pixels2 = neopixel.NeoPixel(
            pixel_pin2, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
        )"""
        #print("DEL ACTIVE")
        return pixels
    #print("DEL INACTIVE")
    
    
def RandLED(DEL_ACTIVE, pixels, pixels2):
    if DEL_ACTIVE:
        pixels.fill((randint(0,255), randint(0,255), randint(0,255)))
        pixels2.fill((randint(0,255), randint(0,255), randint(0,255)))
        pixels.show()
        pixels2.show()
        
        
        #pixels.clear()
        #pixels2.clear()
        
        #pixels.neopixel_cleanup()
        
    #sleep(0.1)