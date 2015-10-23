import threading
import random
import time
import logging

from spielfeld import *

__author__ = 'Mark Weinreuter'

# Fake-Enums
OBEN = 1
UNTEN = 2
LINKS = 3
RECHTS = 4

SCHLAF_ZEIT = .001


class Spieler(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

        # For some more randomness :)
        time.sleep(.2)
        self.x = random.randint(0, SPIELFELD_BREITE)

        time.sleep(.2)
        self.y = random.randint(0, SPIELFELD_HOEHE)

        self.gegner_farbe_index = -1
        self.farb_index = -1
        self._letzter_zustand = FREI
        self.__fertig_sperre = threading.Lock()
        self.__punkte_sperre = threading.Lock()
        self.__zug_fertig = True
        self.__neue_punkte = []


        # Logging Ausgabe anpassen
        logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s', )
        logging.debug("Starte in %d, %d" % (self.x, self.y))

    def __str__(self):
        return "%s: %d, %d" % (self.name, self.x, self.y)

    def run(self):
        logging.debug("Start")

        while SpielFeld.laueft_noch():
            # 'with' übernimmt das anfordern und freigeben der sperre für uns:
            # Flag setzen, dass wir am Arbeiten sind
            with self.__fertig_sperre:
                self.__zug_fertig = False

            # in Richtung bewegen, bzw. versuchen
            richtung = self.gib_richtung()
            self._letzter_zustand = self.__bewege(richtung)

            # Flag zurück setzen
            with self.__fertig_sperre:
                self.__zug_fertig = True

            # damit nicht alles sofort vorbei ist :D
            time.sleep(SCHLAF_ZEIT)

    def init(self, farbe, gegner_farbe):
        self.gegner_farbe_index = gegner_farbe
        self.farb_index = farbe

        self.setName(self.name + "_" + str(farbe))

    def abstand_links(self):
        return self.x

    def abstand_rechts(self):
        return SPIELFELD_BREITE - self.x

    def abstand_oben(self):
        return self.y

    def abstand_unten(self):
        return SPIELFELD_HOEHE - self.y

    def ist_bereit(self):

        with self.__fertig_sperre:
            bereit = self.__zug_fertig

        return bereit

    def gib_punkte(self):
        with self.__punkte_sperre:
            # Liste kopieren und leeren
            punkte = self.__neue_punkte.copy()
            self.__neue_punkte.clear()

        return punkte

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
            if info == FREI:
                with self.__punkte_sperre:
                    self.__neue_punkte.append((x, y))

        return info
