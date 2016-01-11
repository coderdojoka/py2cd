from level import Level
from py2cd import *
from py2cd.farben import *

__author__ = 'Mark Weinreuter'


class TestLevel1(Level):
    def __init__(self):
        super().__init__()

        boden = Rechteck(0, 0, 5000, 20, ROT)
        boden.unten = 20

        boden2 = Rechteck(300, 300, 40, 20, ROT)
        boden3 = Rechteck(350, 100, 40, 20, ROT)
        boden4 = Rechteck(270, 200, 40, 20, ROT)

        self.neues_level_element(boden)
        self.neues_level_element(boden2)
        self.neues_level_element(boden3)
        self.neues_level_element(boden4)

        # Wartet die angegebne Zahl an Millisekunden, bis die Funktion ausgeführt wird
        warte(3500, self.wenn_zeit_um, True)

        for i in range(0, 0):
            b = Rechteck(350 + i * 75, 100, 40, 20, ROT)
            self.neues_level_element(b)

        self.auto_scrollen = True

    def wenn_zeit_um(self):
        print("zeit um")
        b = Rechteck(350, 220, 40, 20, BLAU)
        self.neues_level_element(b)
