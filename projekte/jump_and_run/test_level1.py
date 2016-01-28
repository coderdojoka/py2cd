from level import Level, Gegenstand
from py2cd import *
from py2cd.farben import *

__author__ = 'Mark Weinreuter'


class TestLevel1(Level):
    def __init__(self):
        super().__init__()

        boden = Rechteck(0, 0, 5000, 20, ROT)
        boden.unten = 20

        boden2 = Rechteck(100, 300, 40, 20, ROT)
        boden3 = Rechteck(350, 100, 40, 20, ROT)
        boden4 = Rechteck(270, 200, 40, 20, ROT)

        self.neues_level_element(boden)
        self.neues_level_element(boden2)
        self.neues_level_element(boden3)
        self.neues_level_element(boden4)

        # Wartet die angegebne Zahl an Millisekunden, bis die Funktion ausgeführt wird
        warte(3500, self.wenn_zeit_um, True)

        #self.auto_scrollen = True

    def wenn_zeit_um(self):
        print("zeit um")
        bild = BildSpeicher.gib_bild("ufo")
        bild.setze_skalierung(.5)
        g1 = Gegenstand(bild)
        g1.objekt.setze_position(350,200)

        def entferne_ufo(gegenstand, figur):
            self.entferne_gegenstand(gegenstand)
            # Text anzeigen und nach 2 Sekunden wieder entfernen
            text = Text("Boom", schrift=Schrift(40), farbe=(255, 0, 255))
            text.zentriere()

            warte(1000, text.selbst_entfernen)  # Der Callback muss einen Funktion sein!

        g1.wenn_beruehrt = entferne_ufo
        self.neuer_gegenstand(g1)

