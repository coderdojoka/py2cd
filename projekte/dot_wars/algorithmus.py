import random
import threading
import time

from arena import *

__author__ = 'Mark Weinreuter'

# Fake-Enums
OBEN = 1
UNTEN = 2
LINKS = 3
RECHTS = 4



class Algorithmus(threading.Thread):
    SCHLAF_ZEIT = .00001

    def __init__(self, name):
        super().__init__()
        self.name = name

        # For some more randomness :)
        time.sleep(.2)
        self.x = random.randint(0, SPIELFELD_BREITE)

        time.sleep(.2)
        self.y = random.randint(0, SPIELFELD_HOEHE)

        self.arena = None
        self.gegner_index = -1
        self.index = -1
        self._letzter_zustand = FREI
        self.__fertig_sperre = threading.Lock()
        self.__punkte_sperre = threading.Lock()
        self.__zug_fertig = True
        self.__neu_eroberte_punkte = []
        """
        Liste mit allen neu eroberten Punkten.
        :type: [(int, int)]
        """

        # Logging Ausgabe anpassen
        logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s', )
        #logging.debug("Starte %s in %d, %d" % (self.name, self.x, self.y))

    def __str__(self):
        return "%s: %d, %d" % (self.name, self.x, self.y)

    def run(self):

        while self.arena.laueft_noch():
            # 'with' übernimmt das anfordern und freigeben der sperre für uns:
            # Flag setzen, dass wir am Arbeiten sind
            with self.__fertig_sperre:
                self.__zug_fertig = False

            # in Richtung bewegen, bzw. versuchen
            richtung = self.gib_richtung(self._letzter_zustand)
            self._letzter_zustand = self.__bewege(richtung)

            # Flag zurück setzen
            with self.__fertig_sperre:
                self.__zug_fertig = True

            # damit nicht alles sofort vorbei ist :D
            time.sleep(self.SCHLAF_ZEIT)

    def init(self, arena, index, gegner_index):
        self.arena = arena
        self.gegner_index = gegner_index
        self.index = index

        self.setName(self.name + "_" + str(index))

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

    def gib_eroberte_punkte(self):
        with self.__punkte_sperre:
            # Liste kopieren und leeren
            punkte = self.__neu_eroberte_punkte.copy()
            self.__neu_eroberte_punkte.clear()

        return punkte

    def gib_richtung(self, letzter_zustand):
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
        elif richtung == RECHTS:
            x += 1
        else:
            raise AttributeError("Richtung muss entweder OBEN(1), UNTEN(2), LINKS(3) oder RECHTS(4) sein!")

        info = self.arena.versuche_bewegung(x, y, self.index)
        if info == BESUCHT or info == FREI:

            # Position ändern
            self.x = x
            self.y = y
            if info == FREI:
                with self.__punkte_sperre:
                    self.__neu_eroberte_punkte.append((x, y))

        return info
