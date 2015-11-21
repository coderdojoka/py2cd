#               _____         _
#              / __  \       | |
#  _ __  _   _ `' / /' ___ __| |
# | '_ \| | | |  / /  / __/ _` |
# | |_) | |_| |./ /__| (_| (_| |
# | .__/ \__, |\_____/\___\__,_|
# | |     __/ |
# |_|    |___/

"""
py2cd ist ein (hoffentlich) einfach zu verwendendes "2D-Framework" in Deutsch.

Es können graphische Objekte, wie Rechtecke, Linien, Kreise, Polygone gezeichnet werden.
Außerdem wird das Anzeigen von Bilder und Animationen, als schnelle Abfolge von Bilder, angeboten.


"""
from py2cd.farben import *

__all__ = ['EreignisBearbeiter', 'Spiel', 'ZeichenFlaeche', 'Linie', 'Linien', 'AALinien',
           'Polygon', 'Dreieck', 'Rechteck', 'Kreis', 'Oval', 'Bogen', 'Plot', 'Text',
           'Schrift', 'Bild', 'Animation', 'AnimationenKette', 'AnimierteLinie',
           'BildSpeicher', 'BildWechsler', 'BildAnimation',
           'BildAnimationSpeicher']

import pygame

# Initialisiert pygame
pygame.init()

# Ereignisse
from py2cd.ereignis import *
# Das Haupt-Spiel
from py2cd.spiel import Spiel
from py2cd.flaeche import *
# Formen und so
from py2cd.linie import *
from py2cd.poly import *
from py2cd.rechteck import *
from py2cd.kreis import *
from py2cd.mathe import *
from py2cd.animation import *
# Text
from py2cd.text import *
# Bilder
from py2cd.bild import *
# Animationen
from py2cd.anim import *

# from py2cd.farben import *

version = "0.2.4"
