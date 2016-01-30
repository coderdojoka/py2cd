from py2cd.erweiterungen.jnr.figur import Figur
from py2cd.objekte import Aktualisierbar

__author__ = 'Mark Weinreuter'


class LevelElement(object):
    def __init__(self, zeichenbar, wenn_beruehrt):
        self.objekt = zeichenbar
        """

        :type: py2cd.objekte.Zeichenbar
        """


class Gegenstand(object):
    def __init__(self, zeichenbar, wenn_beruehrt=lambda: None):
        self.objekt = zeichenbar
        """

        :type: py2cd.objekte.Zeichenbar
        """
        self.wenn_beruehrt = wenn_beruehrt


class Level(Aktualisierbar):
    def __init__(self, haupt_figur):
        super().__init__()
        self.gegenstaende = []
        """
        Liste aller Gegenstände.
        :type: list[level.Gegenstand]
        """
        self.level_elemente = []
        """
        Liste aller statischen Levelelement (Mauer, etc...)
        :type: list[py2cd.objekte.Zeichenbar]
        """
        self.figuren = []

        self.haupt_figur = haupt_figur
        self.neue_figur(self.haupt_figur)
        self.auto_scrollen = False
        self.scroll_geschwindigkeit = 1.2

    def aktualisiere(self, relativer_zeitunterschied, zeit_unterschied_ms):

        if self.auto_scrollen:
            self.haupt_figur.x_geschwindigkeit += self.scroll_geschwindigkeit * relativer_zeitunterschied

        for figur in self.figuren:
            figur.figur_aktualisiere(relativer_zeitunterschied)

            for gegenstand in self.gegenstaende:
                if figur.beruehrt_objekt(gegenstand.objekt):
                    gegenstand.wenn_beruehrt(gegenstand, figur)

    def neue_figur(self, figur):
        self.figuren.append(figur)
        figur.kann_kollidieren = self.level_elemente

    def neues_level_element(self, element):
        self.level_elemente.append(element)

    def neuer_gegenstand(self, gegenstand):
        self.gegenstaende.append(gegenstand)

    def entferne_gegenstand(self, gegenstand):
        if gegenstand in self.gegenstaende:
            self.gegenstaende.remove(gegenstand)
            gegenstand.objekt.selbst_entfernen()
        else:
            print("Gegenstand nicht vorhanden.")
