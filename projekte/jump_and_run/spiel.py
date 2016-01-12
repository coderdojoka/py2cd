from figur import Figur
from level import Gegenstand
from py2cd import *
from test_level1 import TestLevel1

__author__ = 'Mark Weinreuter'

Spiel.init(400, 400, "Jump and Run")

level = TestLevel1()

# Bild laden in den Speicher laden und unter dem Schlüssel "scratch" ablegen
BildSpeicher.lade_bild("wobbel", "bilder/wobbel.png")
BildSpeicher.lade_bild("scratch", "bilder/scratch.png")

figur1 = Figur(10, 10, "wobbel")
level.neue_figur(figur1)


def wenn_scratch_beruehrt(gegenstand, figur):
    print("Scratch berührt")
    level.entferne_gegenstand(gegenstand)

    # Text anzeigen und nach 2 Sekunden wieder entfernen
    text = Text("Aua", schrift=Schrift(40), farbe=(255, 0, 255))
    text.zentriere()

    warte(2000, text.selbst_entfernen)  # Der Callback muss einen Funktion sein!


# Einen Gegenstand erzeugen
g1 = Gegenstand(BildSpeicher.gib_bild("scratch"), wenn_scratch_beruehrt)
g1.objekt.setze_position(300, 300)

level.neuer_gegenstand(g1)

# Das Spiel starten
Spiel.starten()
