from spieler import *
from spielfeld import *

__author__ = 'Mark Weinreuter'

GRENZE = 50


class Zufall1(Spieler):
    def gib_richtung(self):

        # Überprüfen, ob wir nicht mehr weiter können
        if (self.counter == self.offset) or self._letzter_zustand == RAND or self._letzter_zustand == BELEGT:

            self.counter = 0
            self.offset = random.randint(10, GRENZE)

            r = random.randint(0, 1)
            # Neue Richtung ermitteln, die NICHT die alte ist

            if self.richtung == RECHTS or self.richtung == LINKS:
                self.richtung = OBEN + r
            else:
                self.richtung = LINKS + r

        self.counter += 1
        return self.richtung

    def __init__(self):
        super().__init__("Zufall 1")
        self.counter = 0
        self.offset = random.randint(10, GRENZE)
        self.richtung = random.randint(1, 4)