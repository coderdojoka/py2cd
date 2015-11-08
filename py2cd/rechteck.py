__author__ = 'Mark Weinreuter'

import pygame
from py2cd.objekte import ZeichenbaresElement


class Rechteck(ZeichenbaresElement):
    """
    Ein Rechteck, das angezeigt werden kann.
    """

    def render(self, pyg_zeichen_flaeche):
        pygame.draw.rect(pyg_zeichen_flaeche, self.farbe,
                         (self.x, self.y, self.breite, self.hoehe),
                         self.dicke)

    def __init__(self, x, y, breite, hoehe, farbe=(0, 0, 0), dicke=0, eltern_flaeche=None):
        """
        Erstellt ein neues Rechteck mit den gegebenen Maßen.

        :param x: die x-Koordinate
        :type x: float
        :param y:
        :type y: float
        :param breite:
        :type breite: float
        :param hoehe:
        :type hoehe: float
        :param eltern_flaeche:
        :type eltern_flaeche: py2cd.flaeche.ZeichenFlaeche
        :param farbe:
        :type farbe: tuple[inŧ]
        :param dicke: die Rahmendicke
        :type dicke: int
        """
        super().__init__(x, y, breite, hoehe, farbe, eltern_flaeche)
        self.dicke = dicke

    def klone(self, x, y):
        r = Rechteck(x, y, self.breite, self.hoehe, self.farbe, self.dicke, self._eltern_flaeche)
        return r
