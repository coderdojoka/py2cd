import py2cd
from py2cd.objekte import Aktualisierbar

__author__ = 'Mark Weinreuter'


class LevelElement(object):
    def __init__(self, zeichenbar):
        self.figuren_drauf = []

        self.objekt = zeichenbar
        """

        :type: py2cd.objekte.Zeichenbar
        """

    def figur_steht_drauf(self, figur):
        if figur not in self.figuren_drauf:
            self.figuren_drauf.append(figur)

    def figur_steht_nicht_drauf(self, figur):
        self.figuren_drauf.remove(figur)


class BewegtesLevelElement(LevelElement):
    def __init__(self, zeichenbar):
        super().__init__(zeichenbar)
        self.x_geschwindigkeit = 0
        self.y_geschwindigkeit = 0

    def setze_geschwindigkeit(self, x=0, y=0):
        self.x_geschwindigkeit = x
        self.y_geschwindigkeit = y

    def aktualisiere(self, rdt):
        self.objekt.aendere_position(self.x_geschwindigkeit * rdt, self.y_geschwindigkeit * rdt)


class Gegenstand(object):
    def __init__(self, zeichenbar, wenn_beruehrt=lambda: None):
        self.objekt = zeichenbar
        """

        :type: py2cd.objekte.Zeichenbar
        """
        self.wenn_beruehrt = wenn_beruehrt


class Level(Aktualisierbar):
    def __init__(self, haupt_figur):
        """

        :param haupt_figur:
        :type haupt_figur: py2cd.erweiterungen.jnr.figur.Figur
        :return:
        :rtype:
        """
        super().__init__()
        self.bewegte_level_elemente = []
        """

        :type: list[py2cd.erweiterungen.jnr.level.BewegtesLevelElement]
        """

        self.gegenstaende = []
        """
        Liste aller Gegenstände.

        :type: list[level.Gegenstand]
        """
        self.alle_level_elemente = []
        """
        Liste aller statischen! Levelelement (Mauer, etc...)

        :type: list[py2cd.erweiterungen.jnr.level.LevelElement]
        """
        self.figuren = []
        """
        Liste aller Figuren.

        :type: list[py2cd.erweiterungen.jnr.figur.Figur]
        """

        self.anzahl_level_elemente = 0
        self.anzahl_bewegte_level_elemente = 0

        self.haupt_figur = haupt_figur
        """
        :type: py2cd.erweiterungen.jnr.figur.Figur
        """

        self.neue_figur(self.haupt_figur)

    def aktualisiere(self, relativer_zeitunterschied, zeit_unterschied_ms):

        for bele in self.bewegte_level_elemente:
            bele.aktualisiere(relativer_zeitunterschied)
            for figur in self.figuren:
                if figur.beruehrt_objekt(bele.objekt):

                    if bele.x_geschwindigkeit > 0:
                        figur.x = bele.objekt.x + bele.objekt.breite
                    elif bele.x_geschwindigkeit < 0:
                        figur.x = bele.objekt.x - figur.breite

                    if bele.y_geschwindigkeit > 0:
                        figur.y = bele.objekt.y + bele.objekt.hoehe
                    elif bele.y_geschwindigkeit < 0:
                        figur.y = bele.objekt.y - figur.hoehe

        for figur in self.figuren:
            figur.figur_aktualisiere(self.alle_level_elemente, relativer_zeitunterschied)

            for gegenstand in self.gegenstaende:
                if figur.beruehrt_objekt(gegenstand.objekt):
                    gegenstand.wenn_beruehrt(gegenstand, figur)

    def neue_figur(self, figur):
        self.figuren.append(figur)
        figur.kann_kollidieren = self.alle_level_elemente

    def neues_level_element(self, element):
        if isinstance(element, py2cd.bbox.BBox):
            element = LevelElement(element)

        assert isinstance(element, LevelElement)
        self.alle_level_elemente.insert(self.anzahl_level_elemente, element)
        self.anzahl_level_elemente += 1

    def neues_bewegtes_level_element(self, element):
        self.alle_level_elemente.append(element)
        self.bewegte_level_elemente.append(element)
        self.anzahl_bewegte_level_elemente += 1

    def neuer_gegenstand(self, gegenstand):
        self.gegenstaende.append(gegenstand)

    def entferne_gegenstand(self, gegenstand):
        if gegenstand in self.gegenstaende:
            self.gegenstaende.remove(gegenstand)
            gegenstand.objekt.selbst_entfernen()
        else:
            print("Gegenstand nicht vorhanden.")
