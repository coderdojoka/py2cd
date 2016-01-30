import pygame

from py2cd import *
from py2cd.erweiterungen.jnr import Figur
from level1 import Level1


__author__ = 'Mark Weinreuter'
Spiel.init(800, 800, "Jump and Run")
haupt_zeichenflaech = Spiel.gib_zeichen_flaeche()
bilder_namen = ["spieler/p1_stand.png", "spieler/p1_vorne.png", "spieler/p1_ducken.png", "spieler/p1_aua.png", "spieler/p1_sprung.png"]
BildSpeicher.lade_bilder_aus_paket(bilder_namen)

bilder_namen = ["p1_stand", "p1_vorne", "p1_aua"]
figur = Figur(200, 300, bilder_namen)
level = Level1(figur)
Kamera.setze_zentrum(figur)


Spiel.zeichne_gitter()
# Das Spiel starten
Spiel.starten()
