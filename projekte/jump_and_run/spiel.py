from figur import Figur
from level import Gegenstand
from py2cd import *
from test_level1 import TestLevel1

__author__ = 'Mark Weinreuter'

Spiel.init(400, 400, "Jump and Run")

level = TestLevel1()

# Bild laden in den Speicher laden und unter dem Schlüssel "scratch" ablegen
BildSpeicher.lade_bild("wobbel", "bilder/schaf.png")
BildSpeicher.lade_bild("ufo", "bilder/ufo.png")

figur1 = Figur(10, 10, "wobbel")
level.neue_figur(figur1)

# Das Spiel starten
Spiel.starten()
