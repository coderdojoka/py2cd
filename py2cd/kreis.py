import math

import pygame

from py2cd.objekte import ZeichenbaresElement

__author__ = 'Mark Weinreuter'


class Kreis(ZeichenbaresElement):
    """
    Ein Kreis, der angezeigt werden kann.
    """

    def render(self, pyg_zeichen_flaeche, x_offset=0, y_offset=0):
        # Mitte verschieben, damit x,y immer der linke Rand ist
        pygame.draw.circle(pyg_zeichen_flaeche, self.farbe,
                           (int(self.x + x_offset + self.radius), int(self.y + y_offset + self.radius)), self.radius, self.dicke)

    def __init__(self, x, y, radius, farbe=(0, 0, 0), dicke=0, eltern_flaeche=None):
        """
        Erstellt ein neues Rechteck mit den gegebenen Maßen.

        :param x:
        :type x: float
        :param y:
        :type y: float
        :param radius: der Kreisradius
        :type radius: float
        :param eltern_flaeche:
        :type eltern_flaeche: py2cd.flaeche.ZeichenFlaeche
        :param farbe:
        :type farbe: tuple[inŧ]
        :param dicke:
        :type dicke: int
        :return:
        :rtype:
        """
        super().__init__(x, y, radius * 2, radius * 2, farbe, eltern_flaeche)
        self.radius = radius
        self.dicke = dicke

    def klone(self, x, y):
        k = Kreis(x, y, self.radius, self.farbe, self.dicke, self._eltern_flaeche)
        return k


class Oval(ZeichenbaresElement):
    def klone(self, x, y):
        o = Oval(x, y, self.radius_breite, self.radius_hoehe, self.farbe, self.dicke)
        return o

    def __init__(self, x, y, radius_breite, radius_hoehe, farbe=(0, 0, 0), dicke=0, eltern_flaeche=None):
        self.radius_breite = radius_breite
        self.radius_hoehe = radius_hoehe
        self.dicke = dicke
        self._pyg_rect = (x, y, radius_breite * 2, radius_hoehe * 2)

        super().__init__(x, y, radius_breite * 2, radius_hoehe * 2, farbe, position_geaendert=self.geandert, eltern_flaeche=eltern_flaeche)

    def geandert(self):
        self._pyg_rect = (self.x, self.y, self.radius_breite * 2, self.radius_hoehe * 2)

    def render(self, pyg_zeichen_flaeche, x_offset=0, y_offset=0):
        # ellipse(Surface, color, Rect, width=0) -> Rect
        pygame.draw.ellipse(pyg_zeichen_flaeche, self.farbe, self._pyg_rect, self.dicke)


class Bogen(Oval):
    def __init__(self, x, y, radius_breite, radius_hoehe, start_winkel=0, end_winkel=90, farbe=(0, 0, 0), dicke=1, eltern_flaeche=None):
        super().__init__(x, y, radius_breite, radius_hoehe, farbe, dicke, eltern_flaeche=eltern_flaeche)
        self.__end_winkel_rad = 0
        self.__start_winkel_rad = 0
        self.setze_winkel(start_winkel, end_winkel)

    def setze_winkel(self, start_winkel=None, end_winkel=None):
        if start_winkel is not None:
            self.__start_winkel_rad = math.pi / 180 * start_winkel
        if end_winkel is not None:
            self.__end_winkel_rad = math.pi / 180 * end_winkel

    def render(self, pyg_zeichen_flaeche, x_offset=0, y_offset=0):
        # arc(Surface, color, Rect, start_angle, stop_angle, width=1) -> Rect
        pygame.draw.arc(pyg_zeichen_flaeche, self.farbe, self._pyg_rect, self.__start_winkel_rad, self.__end_winkel_rad, self.dicke)

    def klone(self, x, y):
        b = Bogen(x, y, self.radius_breite, self.radius_hoehe,
                  self.__start_winkel_rad / math.pi * 180, self.__end_winkel_rad / math.pi * 180, self.farbe, self.dicke)
        return b
