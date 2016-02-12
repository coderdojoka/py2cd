from py2cd import *
from py2cd.erweiterungen.jnr.level import Level, BewegtesLevelElement
from py2cd.farben import *

__author__ = 'Mark Weinreuter'


class Level1(Level):
    def __init__(self, figur):
        super().__init__(figur)

        # Bild einmal laden
        BildSpeicher.lade_bild_aus_paket("block", "tiles/sand.png")

        # Hässlicher roter Boden
        boden = Rechteck(0, 400, 500, 20, ROT)

        # Drei Blöcke erstellen
        block = BildSpeicher.gib_bild("block", 100, 200)
        block2 = BildSpeicher.gib_bild("block", 350, 100)
        block3 = BildSpeicher.gib_bild("block", 270, 200)

        # Blöcke zu Bewegten Blöcken machen
        self.bewegt = BewegtesLevelElement(block)
        self.bewegt.setze_geschwindigkeit(1, 0)
        self.bewegt1 = BewegtesLevelElement(block2)
        self.bewegt1.setze_geschwindigkeit(0, 1)

        # Bewegete Blöcke zum Level hinzufügen
        self.neues_bewegtes_level_element(self.bewegt)
        self.neues_bewegtes_level_element(self.bewegt1)

        # Feste Blöcke hinzufügen
        self.neues_level_element(boden)
        self.neues_level_element(block3)

        # Wartet 300 MilliSekunden und führt dann die Funktion aus.
        # Das ganze wird alle 300 ms wiederholt
        warte(300, self.haupt_figur.naechstes_bild, True)

        # Zähler für bewegungänderung
        self.counter = 0

        # Hauptfigur position
        self.haupt_figur.x = 200

    def aktualisiere(self, relativer_zeitunterschied, zeit_unterschied_ms):
        super().aktualisiere(relativer_zeitunterschied, zeit_unterschied_ms)

        self.counter += 1
        if self.counter % 100 == 0:
            self.counter = 0
            self.bewegt.x_geschwindigkeit *= -1
            self.bewegt1.y_geschwindigkeit *= -1
            # Code kommt hier her
