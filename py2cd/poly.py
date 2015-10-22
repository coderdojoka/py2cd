__author__ = 'Mark Weinreuter'

import pygame

from py2cd.objekte import *


class Polygon(ZeichenbaresElement):
    def __init__(self, punkte, farbe=(0, 0, 0), dicke=0, eltern_flaeche=None):
        """
        Erstellt ein neues Polygon mit den gegebenen Eckpunkte.

        :param punkte: Die Punkte, die das Polygone ausmachen. Jeder Punkt besteht aus einem Tupel von x, y Koordinaten
        :type: punkte: list [int, int]
        :param eltern_flaeche: die Elternfläche
        :type eltern_flaeche: py2cd.flaeche.ZeichenFlaeche
        :param farbe:
        :type farbe: tuple [int]
        :param dicke: die Dicke des Rahmens, für dicke = 0 ist das Polygon gefüllt
        :type: dicke: int
        """

        self._punkte = []
        """
        Die Punkteliste. Die Punkte werden so umgerechnet, dass sie relativ zum Startpunkt sind.

        :type: list[int, int]
        """
        self._verschobene_punkte = []
        """
        Interne Liste mit x,y Verschiebung

        :type: list[int, int]
        """

        self.dicke = dicke
        """
        Die Dicke mit der das Polygon gezeichnet wird, 0=> gefüllt.

        :type: int
        """

        x, y, breite, hoehe = self.setze_punkte(punkte)

        # Eltern init()
        super().__init__(x, y, breite, hoehe, farbe, eltern_flaeche, self._aktualisiere_punkte)

    def render(self, pyg_zeichen_flaeche):
        return pygame.draw.polygon(pyg_zeichen_flaeche, self.farbe, self._verschobene_punkte, self.dicke)

    def _aktualisiere_punkte(self):
        self._verschobene_punkte = [(p[0] + self.x, p[1] + self.y) for p in self._punkte]

    def setze_punkte(self, punkte):
        # Konvertiere die Punkte so, das der erste Punkt bei (0,0) liegt und der erste Punkt wird als x,y-Koordinaten angesehen
        x_min = punkte[0][0]
        x_max = punkte[0][0]
        y_min = punkte[0][1]
        y_max = punkte[0][1]
        for punkt in punkte:
            if punkt[0] < x_min:
                x_min = punkt[0]

            elif punkt[0] > x_max:
                x_max = punkt[0]

            if punkt[1] < y_min:
                y_min = punkt[1]

            elif punkt[1] > y_max:
                y_max = punkt[1]

        self._punkte = [(p[0] - x_min, (p[1] - y_min)) for p in punkte]
        self._verschobene_punkte = punkte.copy()

        # x-, y-Position, Breite, Höhe
        return x_min, y_min, x_max - x_min, y_max - y_min


class Linien(Polygon):
    """
    Mehrere Linie zwischen den angegebenen Punkten. Alle Punkte werden der Reihe nach verbunden. 1 -> 2 -> 3...
    """

    def render(self, pyg_zeichen_flaeche):
        return pygame.draw.lines(pyg_zeichen_flaeche, self.farbe, self._geschlossen, self._verschobene_punkte,
                                 self.dicke)

    def __init__(self, punkte, geschlossen=False, farbe=(0, 0, 0), dicke=1, eltern_flaeche=None):
        """
        Erstellt ein neues Liniensystem aus den gegebenen Punkten.

        :param punkte:
        :type punkte: list[tuple[float]]
        :param eltern_flaeche:
        :type eltern_flaeche: py2cd.flaeche.ZeichenFlaeche
        :param geschlossen:
        :type geschlossen: bool
        :param farbe:
        :type farbe: tuple[int]
        :param dicke:
        :type dicke: int
        """
        self._geschlossen = geschlossen

        super().__init__(punkte, farbe, dicke, eltern_flaeche)


class AALinien(Polygon):
    """
    Mehrere Linie zwischen den angegebenen Punkten. Alle Punkte werden der Reihe nach verbunden. 1 -> 2 -> 3...
    """

    def render(self, pyg_zeichen_flaeche):
        return pygame.draw.aalines(pyg_zeichen_flaeche, self.farbe, self._geschlossen, self._verschobene_punkte,
                                   True)

    def __init__(self, punkte, geschlossen=False, farbe=(0, 0, 0), eltern_flaeche=None):
        """
        Erstellt ein neues Liniensystem aus den gegebenen Punkten.

        :param punkte:
        :type punkte: list[tuple[float]]
        :param eltern_flaeche:
        :type eltern_flaeche: py2cd.flaeche.ZeichenFlaeche
        :param geschlossen:
        :type geschlossen: bool
        :param farbe:
        :type farbe: tuple[int]
        """
        self._geschlossen = geschlossen

        super().__init__(punkte, farbe, eltern_flaeche=eltern_flaeche)
