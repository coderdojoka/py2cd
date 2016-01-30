from py2cd import *
from py2cd.erweiterungen.jnr.level import Level, Gegenstand
from py2cd.farben import *

__author__ = 'Mark Weinreuter'


class Level1(Level):
    def __init__(self, figur):
        super().__init__(figur)

        boden = Rechteck(0, 400, 500, 20, ROT)

        BildSpeicher.lade_bild_aus_paket("block", "tiles/sand.png")
        block = BildSpeicher.gib_bild("block", 100, 200)
        boden3 = BildSpeicher.gib_bild("block", 350, 100)
        boden4 = BildSpeicher.gib_bild("block", 270, 200)
        block.setze_skalierung(.75)

        self.neues_level_element(boden)
        self.neues_level_element(block)
        self.neues_level_element(boden3)
        self.neues_level_element(boden4)


        self.haupt_figur.x = 200

    def aktualisiere(self, relativer_zeitunterschied, zeit_unterschied_ms):
        super().aktualisiere(relativer_zeitunterschied, zeit_unterschied_ms)

        # Code kommt hier her
