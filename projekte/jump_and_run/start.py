import pygame

from py2cd import *
from py2cd.extensions.jnr.figur import Figur
from test_level1 import TestLevel1
from py2cd.extensions.jnr.zentrum_haupt_flaeche import *

__author__ = 'Mark Weinreuter'
haupt_flaeche = ZetrumHauptZeichenFlaeche(0, 0, pygame.display.set_mode((400, 400)))
Spiel.init(400, 400, "Jump and Run", haupt_flaeche=haupt_flaeche)

level = TestLevel1()
haupt_flaeche.setze_zentrum(level.haupt_figur)


# Das Spiel starten
Spiel.starten()
