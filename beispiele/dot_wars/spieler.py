__author__ = 'Mark Weinreuter'
import random

from spielfeld import *

# Fake-Enums
OBEN = 1
UNTEN = 2
LINKS = 3
RECHTS = 4


class Spieler:
    def __init__(self, name):
        self.name = name
        self.x = random.randint(0, SPIELFELD_BREITE)
        self.y = random.randint(0, SPIELFELD_HOEHE)
        self.gegner_farbe_index = -1
        self.farb_index = -1
        self.letzter_zustand = FREI

    def __str__(self):
        return "%s: %d, %d" % (self.name, self.x, self.y)

    def start(self, farbe, gegner_farbe):
        self.gegner_farbe_index = gegner_farbe
        self.farb_index = farbe

    def abstand_links(self):
        return self.x

    def abstand_rechts(self):
        return SPIELFELD_BREITE - self.x

    def abstand_oben(self):
        return self.y

    def abstand_unten(self):
        return SPIELFELD_HOEHE - self.y

    def aktualisiere(self):
        richtung = self.gib_richtung()
        self.letzter_zustand = self.__bewege(richtung)

    def gib_richtung(self):
        raise NotImplementedError("Diese Methode muss überschrieben werden und OBEN, UNTEN, RECHTS oder LINKS zurückgeben.")

    def __bewege(self, richtung):

        x = self.x
        y = self.y

        if richtung == UNTEN:
            y += 1
        elif richtung == OBEN:
            y -= 1
        elif richtung == LINKS:
            x -= 1
        else:
            x += 1

        info = SpielFeld.feld_info(x, y, self.farb_index)
        if info == BESUCHT or info == FREI:
            self.x = x
            self.y = y

        return info
