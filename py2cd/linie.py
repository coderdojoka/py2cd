import math

import pygame

from py2cd.objekte import ZeichenbaresElement

__author__ = 'Mark Weinreuter'


class Linie(ZeichenbaresElement):
    """
    Eine Linie die angezeigt werden kann.
    """

    def render(self, pyg_zeichen_flaeche, x_offset=0, y_offset=0):
        pygame.draw.line(pyg_zeichen_flaeche, self.farbe,
                         (self.x, self.y), self.__verschobenes_ende, self.dicke)

    def setze_ende(self, ende):
        self.__ende = (ende[0] - self.__start[0], (ende[1] - self.__start[1]))
        self._aktualisiere_end_punkt()

    def _aktualisiere_end_punkt(self):
        self.__verschobenes_ende = (self.x + self.__ende[0], self.y + self.__ende[1])

    def laenge(self):
        return math.sqrt(self.__ende[0] ** 2 + self.__ende[1] ** 2)

    def __init__(self, start, ende, farbe=(0, 0, 0), dicke=1, eltern_flaeche=None):
        """
        Erstellt eine neue Linie zwischen den beiden gegebenen Punkten.

        :param start der Startpunkt
        :type start: tuple[float]
        :param ende der Endpunkt
        :type ende: tuple[float]
        :param farbe:
        :type farbe: tuple[int]
        :param dicke:
        :type dicke: int
        """

        # punkte umrechnen, so dass diese bei 0,0 beginnen, und start zu x,y-Position wird
        self.__start = start
        self.__ende = (ende[0] - start[0], (ende[1] - start[1]))
        self.dicke = dicke

        self.__verschobenes_ende = self.__ende
        """
        Internes Tupel für den Endpunkt, der aktualisiert werden muss, wenn die Position geändert wird
        :type: tuple[float]
        """

        super().__init__(start[0], start[1], self.__ende[0], self.__ende[1],
                         farbe, eltern_flaeche, position_geaendert=self._aktualisiere_end_punkt)

    def klone(self, x, y):
        start = (self.__start[0], self.__start[1])
        ende = (self.__start[0] + self.__ende[1], self.__start[1] + self.__ende[1])
        l = Linie(start, ende, self.farbe, self.dicke, self._eltern_flaeche)
        l.setze_position(x, y)

        return l
