import pygame

from figur import Figur
from jnr_haupt_flaeche import JNRHauptZeichenFlaeche
from py2cd import *
from test_level1 import TestLevel1

__author__ = 'Mark Weinreuter'
haupt_flaeche = JNRHauptZeichenFlaeche(0, 0, pygame.display.set_mode((400, 400)))
Spiel.init(400, 400, "Jump and Run", haupt_flaeche=haupt_flaeche)

level = TestLevel1()

# Bild laden in den Speicher laden und unter dem Schlüssel "scratch" ablegen
BildSpeicher.lade_bild("wobbel", "bilder/wobbel.png")
BildSpeicher.lade_bild("ufo", "bilder/ufo.png")

figur1 = Figur(10, 10, "wobbel")

haupt_flaeche.setze_zentrale_figur(figur1)

level.neue_figur(figur1)

# Das Spiel starten
Spiel.starten()
