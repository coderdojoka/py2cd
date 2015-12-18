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
import pygame
from pygame.constants import *
pygame.init() # wir initialisieren hier schon pygame

from py2cd.farben import *

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
from py2cd.vektor import *

from py2cd.tasten import *

__all__ = ['EreignisBearbeiter', 'Spiel', 'ZeichenFlaeche', 'Linie', 'Linien', 'AALinien',
           'Polygon', 'Dreieck', 'Rechteck', 'Kreis', 'Oval', 'Bogen', 'Plot', 'Text',
           'Schrift', 'Bild', 'Animation', 'AnimationenKette', 'AnimierteLinie',
           'BildSpeicher', 'BildWechsler', 'BildAnimation',
           'BildAnimationSpeicher', 'Vektor2', 'Taste',

           "T_0",
           "T_1",
           "T_2",
           "T_3",
           "T_4",
           "T_5",
           "T_6",
           "T_7",
           "T_8",
           "T_9",
           "T_a",
           "T_b",
           "T_c",
           "T_d",
           "T_e",
           "T_f",
           "T_g",
           "T_h",
           "T_i",
           "T_j",
           "T_k",
           "T_l",
           "T_m",
           "T_n",
           "T_o",
           "T_p",
           "T_q",
           "T_r",
           "T_s",
           "T_t",
           "T_u",
           "T_v",
           "T_w",
           "T_x",
           "T_y",
           "T_z",
           "T_LEER",
           "T_ENTER",
           "T_ESCAPE",
           # Pfeiltasten
           "T_UNTEN",
           "T_RECHTS",
           "T_LINKS",
           "T_OBEN",
           "T_ENTFERNEN",
           "T_ASTERISK",
           "T_BACKSPACE",
           "T_DOPPELPUNKT",
           "T_KOMMA",
           "T_LSHIFT",
           "T_RSHIFT",
           "T_FRAGEZEICHEN",
           "T_PUNKT",
           "T_PLUS",
           "T_MINUS"
           ]

version = "0.2.5"

# Tn-Codes

T_0 = K_0
T_1 = K_1
T_2 = K_2
T_3 = K_3
T_4 = K_4
T_5 = K_5
T_6 = K_6
T_7 = K_7
T_8 = K_8
T_9 = K_9
T_a = K_a
T_b = K_b
T_c = K_c
T_d = K_d
T_e = K_e
T_f = K_f
T_g = K_g
T_h = K_h
T_i = K_i
T_j = K_j
T_k = K_k
T_l = K_l
T_m = K_m
T_n = K_n
T_o = K_o
T_p = K_p
T_q = K_q
T_r = K_r
T_s = K_s
T_t = K_t
T_u = K_u
T_v = K_v
T_w = K_w
T_x = K_x
T_y = K_y
T_z = K_z

T_LEER = K_SPACE
T_ENTER = K_RETURN
T_ESCAPE = K_ESCAPE

# Pfeiltasten
T_UNTEN = K_DOWN
T_RECHTS = K_RIGHT
T_LINKS = K_LEFT
T_OBEN = K_UP

T_ENTFERNEN = K_DELETE
T_ASTERISK = K_ASTERISK
T_BACKSPACE = K_BACKSPACE
T_DOPPELPUNKT = K_COLON
T_KOMMA = K_COMMA

T_LSHIFT = K_LSHIFT
T_RSHIFT = K_LSHIFT

T_FRAGEZEICHEN = K_QUESTION

T_PUNKT = K_PERIOD
T_PLUS = K_PLUS
T_MINUS = K_MINUS
