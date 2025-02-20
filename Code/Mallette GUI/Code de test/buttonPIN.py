import time
import board
from digitalio import DigitalInOut, Direction, Pull

# LED setup.
led = DigitalInOut(board.D14)
# For QT Py M0. QT Py M0 does not have a D13 LED, so you can connect an external LED instead.
# led = DigitalInOut(board.SCK)
led.direction = Direction.OUTPUT

# For Gemma M0, Trinket M0, Metro M0 Express, ItsyBitsy M0 Express, Itsy M4 Express, QT Py M0
switch = DigitalInOut(board.D4)
switch.direction = Direction.INPUT

while True:
    # We could also do "led.value = not switch.value"!
    if switch.value:
        print("off")
        led.value = False
    else:
        print("on")
        led.value = True

    time.sleep(0.1)  # debounce delay