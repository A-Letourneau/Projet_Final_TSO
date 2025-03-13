# Auteur: Alexis Letourneau
# Editeur: Louis Boisvert
# Brief : NeoPixel librairie utilisant rpi_ws281x directement au lieu de NeoPixel
# Permet d'init des strip de DEL et de faire quelques animations
# DOIT ETRE LANCE EN SUDO AVEC LA COMMANDE "sudo thonny" DANS LE CMD


import time
from rpi_ws281x import PixelStrip, Color

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)

# ne pas utilisés, parce qu'il bloque la fonction jusqu'à la fin de l'animation
def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)


def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

# ne pas utilisés, parce qu'il bloque la fonction jusqu'à la fin de l'animation
def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)

# ne pas utilisés, parce qu'il bloque la fonction jusqu'à la fin de l'animation
def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel(
                (int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)

# ne pas utilisés, parce qu'il bloque la fonction jusqu'à la fin de l'animation    peut être utile en cas de victoires
def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, wheel((i + j) % 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)

def initStrip(LED_PIN, LED_COUNT, LED_BRIGHTNESS, IS_GPIO_13_OR_19):
    """return the Init a strip of DEL with the right arguments"""
    # LED strip configuration:
    LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA = 10          # DMA channel to use for generating signal (try 10)
    LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
    
    return PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, IS_GPIO_13_OR_19)


# Main program logic follows:
if __name__ == '__main__':
    print("start")
    # Create NeoPixel object with appropriate configuration.
    # set to 'True' for GPIOs 13, 19, 41, 45 or 53
    strip1 = initStrip(19, 12, 50, True)
    strip2 = initStrip(12, 12, 50, False)
    strip3 = initStrip(18, 12, 50, False)
    strip4 = initStrip(21, 12, 50, False)
    
    strip1.begin()
    strip2.begin()
    strip3.begin()
    strip4.begin()

    while True:
        colorWipe(strip1, Color(255, 0, 0), 0)  # Red wipe
        colorWipe(strip2, Color(255, 0, 0), 0)  # Red wipe
        colorWipe(strip3, Color(255, 0, 0), 0)  # Red wipe
        colorWipe(strip4, Color(255, 0, 0), 0)  # Red wipe
        time.sleep(0.5)
        colorWipe(strip1, Color(0, 255, 0), 0)  # Green wipe
        colorWipe(strip2, Color(0, 255, 0), 0)  # Green wipe
        colorWipe(strip3, Color(0, 255, 0), 0)  # Green wipe
        colorWipe(strip4, Color(0, 255, 0), 0)  # Green wipe
        time.sleep(0.5)

