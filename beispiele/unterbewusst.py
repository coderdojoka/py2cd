import random
from py2cd import *
from py2cd.farben import *

Spiel.init(640, 480, "Mein Spiel")

zaehler = 0


def aktualisiere(dt):
    global zaehler

    block.pralle_vom_rand_ab(True)
    block.bewege(dt)

    text.verstecke()
    if zaehler == 100:
        text.zeige()
        zaehler = 0

    zaehler = zaehler + 1

namen = ["Cola", "Pepsi", "7 Up", "Dr. Pepper"]
text = Text(namen[random.randint(0, len(namen)-1)], schrift=Schrift(50),farbe=HELL_GRAU)
text.zentriere()

block = Rechteck(10, 10, 100, 100, ROT)
block.setze_geschwindigkeit(5,5)

Spiel.fps = 500
Spiel.setze_aktualisierung(aktualisiere)
Spiel.starten()
