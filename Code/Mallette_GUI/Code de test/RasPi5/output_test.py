#!/home/tge/Documents/venv/bin/python3
"""
Code: Initialisation GPIO Style library
Auteur: Louis Boisvert
Date: 2025-05-20
Description:
 ceci est la version que j'ai pris du site internet suivant. elle est supposer fonctionner, mais
 comme beaucoup de library comme celle-ci qui est supposer fonctionner, elle marche sur une version
 de GPIOD qui est souvent pas la plus récente et même rarement dit la verion qu'ils utilisent de
 GPIOD, ce qui apporte à des problèmes de fonction non-existante dans les versions plus récentes
 ou encore des fonctions qui ne fonctionnes plus comme les versions précédentes.
 
 https://pypi.org/project/gpiod/2.3.0/
"""
import time
import gpiod

LINE = 17
chip = "/dev/gpiochip0"

with gpiod.Chip.request_lines(
    chip,
    consumer="blink-example",
    config={
        LINE: gpiod.LineSettings(
            direction = gpiod.line.Direction.OUTPUT,
            output_value = gpiod.line.Value.ACTIVE
        )
    },
) as request:
    while True:
        request.set_value(LINE, Value.ACTIVE)
        time.sleep(1)
        request.set_value(LINE, Value.INACTIVE)
        time.sleep(1)