from py2cd import HauptZeichenFlaeche, Vektor2

__author__ = 'Mark Weinreuter'

class JNRHauptZeichenFlaeche(HauptZeichenFlaeche):
    def __init__(self, x, y, pygame_flaeche_breite):
        super().__init__(x, y, pygame_flaeche_breite)

        self.zentrale_figur = None
        """
        :type: py2cd.objekte.Zeichenbar
        """

        self._x_faktor = .5
        self._y_faktor = .75
        self.__soll_position = Vektor2(self._x_faktor * self.breite, self._y_faktor * self.hoehe)


        self.letzte_zentrale_pos = None
        """
        :type: py2cd.vektor.Vektor2
        """

    def setze_zentrale_figur(self, figur):
        # Figur muss existieren und ein direktes Kind der Hauptfläche sein
        assert figur is not None
        assert figur in self.zeichenbareObjekte

        self.zentrale_figur = figur
        self.letzte_zentrale_pos = figur.position()
        self.zentrale_figur.position_geaendert.registriere(self.aktualisiere_positionen)

    def entferne_zentrale_figur(self):
        assert self.zentrale_figur is not None
        self.zentrale_figur.position_geandert.entferne(self.aktualisiere_positionen)
        self.zentrale_figur = None

    def aktualisiere_positionen(self):
        self.delta = self.__soll_position - self.zentrale_figur.position()
        print(self.delta)

    def zeichne_alles(self):

        self.pyg_flaeche.fill(self.farbe)

        if self.zentrale_figur is None:
            # zeichne alle
            for zb in self._zeichenbare_objekte:
                zb.zeichne()
        else:
            for zb in self._zeichenbare_objekte:
                zb.aendere_position(self.delta)
                zb.zeichne()
                zb.aendere_position(self.delta.klone().multipliziere_selbst(-1))

