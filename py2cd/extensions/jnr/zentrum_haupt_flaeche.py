from py2cd import Vektor2, HauptZeichenFlaeche

__author__ = 'Mark Weinreuter'


class ZetrumHauptZeichenFlaeche(HauptZeichenFlaeche):
    def __init__(self, x, y, pygame_flaeche_breite):
        super().__init__(x, y, pygame_flaeche_breite)

        self.zentrum = None
        """
        :type: py2cd.objekte.Zeichenbar
        """

        self._x_faktor = .5
        self._y_faktor = .75
        self.__soll_position = Vektor2(self._x_faktor * self.breite, self._y_faktor * self.hoehe)

        """
        :type: py2cd.vektor.Vektor2
        """

    def setze_zentrum(self, figur):
        # Figur muss existieren und ein direktes Kind der Hauptfläche sein
        assert figur is not None
        assert figur in self.zeichenbareObjekte

        self.zentrum = figur

    def entferne_zentrale_figur(self):
        assert self.zentrum is not None
        self.zentrum = None

    def zeichne_alles(self):

        self.pyg_flaeche.fill(self.farbe)

        if self.zentrum is None:
            # zeichne alle
            for zb in self._zeichenbare_objekte:
                zb.zeichne()
        else:
            delta = self.__soll_position - self.zentrum.position()
            for zb in self._zeichenbare_objekte:
                zb.zeichne(delta[0], delta[1])
