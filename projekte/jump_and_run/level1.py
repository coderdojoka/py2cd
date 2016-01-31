from py2cd import *
from py2cd.erweiterungen.jnr.level import Level, BewegtesLevelElement
from py2cd.farben import *

__author__ = 'Mark Weinreuter'


class Level1(Level):
    def __init__(self, figur):
        super().__init__(figur)

        boden = Rechteck(0, 400, 500, 20, ROT)

        BildSpeicher.lade_bild_aus_paket("block", "tiles/sand.png", False)
        block = BildSpeicher.gib_bild("block", 100, 200)
        block2 = BildSpeicher.gib_bild("block", 350, 100)
        boden4 = BildSpeicher.gib_bild("block", 270, 200)

        self.b = BewegtesLevelElement(block)
        self.b.setze_geschwindigkeit(1, 0)
        self.b2 = BewegtesLevelElement(block2)
        self.b2.setze_geschwindigkeit(0, 1)

        self.counter = 0

        self.neues_bewegtes_level_element(self.b)
        self.neues_bewegtes_level_element(self.b2)

        self.neues_level_element(boden)
        self.neues_level_element(boden4)

        self.haupt_figur.x = 200

    def aktualisiere(self, relativer_zeitunterschied, zeit_unterschied_ms):
        super().aktualisiere(relativer_zeitunterschied, zeit_unterschied_ms)

        self.counter += 1
        if self.counter % 100 == 0:
            self.counter = 0
            self.b.x_geschwindigkeit *= -1
            self.b2.y_geschwindigkeit *= -1
            # Code kommt hier her
