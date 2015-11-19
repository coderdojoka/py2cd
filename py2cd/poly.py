__author__ = 'Mark Weinreuter'

import math

import pygame

from py2cd.objekte import *


class Polygon(ZeichenbaresElement, SkalierbaresElement):
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

        self._mittel_punkt = Punkt(0, 0)
        self._punkte = []
        """
        Die Punkteliste. Die Punkte werden so umgerechnet, dass sie relativ zum Startpunkt sind.

        :type: list[Punkt]
        """
        self._verschobene_punkte = []
        """
        Interne Liste mit x,y Verschiebung

        :type: list[(int, int)]
        """

        self._transformierte_punkte = []
        """
        Interne Liste mit x,y Verschiebung transformiert!

        :type: list[Punkt]
        """

        self.dicke = dicke
        """
        Die Dicke mit der das Polygon gezeichnet wird, 0=> gefüllt.

        :type: int
        """

        x, y, breite, hoehe = self.setze_punkte(punkte)

        # Eltern init(). Reihenfolge!
        SkalierbaresElement.__init__(self, self)
        ZeichenbaresElement.__init__(self, x, y, breite, hoehe, farbe, eltern_flaeche, self._aktualisiere_punkte)

    def render(self, pyg_zeichen_flaeche):
        return pygame.draw.polygon(pyg_zeichen_flaeche, self.farbe, self._verschobene_punkte, self.dicke)

    def _aktualisiere_punkte(self):
        self._verschobene_punkte = self._mache_relativ_zu(self.x, self.y, self._transformierte_punkte)

    def setze_punkte(self, punkte):

        # die maße der Eingabedaten
        x_min, y_min, breite, hoehe = self._umgebendes_rechteck(punkte)
        self._mittel_punkt.setze(breite / 2, hoehe / 2)

        # Punkte relativ zur linken oberen ecke (x_min, y_min)
        self._punkte = [Punkt(p[0] - x_min, p[1] - y_min) for p in punkte]
        self._transformierte_punkte = self._punkte.copy()
        self._verschobene_punkte = self._punkte.copy()

        return x_min, y_min, breite, hoehe

    @staticmethod
    def _umgebendes_rechteck(punkte):
        # umgebendes Rechteck berechnen
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

        # wir berechnen die Punkte, so dass die Mitte bei (0,0) liegt
        breite = x_max - x_min
        hoehe = y_max - y_min
        return x_min, y_min, breite, hoehe

    @property
    def mitte_punkte(self):
        # gewichtete mitte aller punkte
        mitte = Punkt(0, 0)
        for punkt in self._transformierte_punkte:
            mitte.addiere(punkt)

        return mitte.skaliere(1 / len(self._transformierte_punkte))

    @mitte_punkte.setter
    def mitte_punkte(self, x, y=None):
        # um Tupel zu akzeptieren
        if y is None:
            y = x[1]
            x = x[0]
        mitte = self.mitte_punkte
        self._mache_relativ_zu(-mitte.x + x, -mitte.y + y, self._transformierte_punkte)

    def _rotation_skalierung_anwenden(self):

        _radians = self._winkel / 180 * math.pi

        cs = math.cos(_radians)
        sn = math.sin(_radians)

        matrix = Matrix2(cs, -sn, sn, cs)
        # (cos, -sin) * (x, y)
        # (cos, sin)  *
        # und die skalierung
        m = self._mittel_punkt  # //Punkt(self.breite / 2, self.hoehe / 2)
        # Punkt relativ zur Mitte machen, dann rotieren und skalieren, dann rücktransformieren
        # relativ zu linken oberen ecke

        self._transformierte_punkte = []
        for punkt in self._punkte:
            p = (punkt - m)
            p = (matrix * p)
            p.skaliere(self._skalierung)
            p += m
            self._transformierte_punkte.append(p)

        x, y, breite, hoehe = self._umgebendes_rechteck(self._transformierte_punkte)

        self._transformierte_punkte = self._mache_relativ_zu(-x, -y, self._transformierte_punkte)

        return breite, hoehe

    def _mitte_nach_rotation_zurueck_setzen(self, alte_mitte):
        self.mitte = alte_mitte

    @staticmethod
    def _mache_relativ_zu(x, y, punkte):
        return [p.addiere(x, y) for p in punkte]

    def klone(self, x, y):
        p = Polygon(self._punkte.copy(), self.farbe, self.dicke, self._eltern_flaeche)
        p.setze_position(x, y)
        return p


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

    def klone(self, x, y):
        l = Linien(self._punkte.copy(), self._geschlossen, self.farbe, self.dicke, self._eltern_flaeche)
        l.setze_position(x, y)
        return l


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

    def klone(self, x, y):
        aal = AALinien(self._punkte.copy(), self._geschlossen, self.farbe, self._eltern_flaeche)
        aal.setze_position(x, y)
        return all


class Punkt:
    def __init__(self, x=0, y=0):
        """

        :param x:
        :type x: Number
        :param y:
        :type y: Number
        :return:
        :rtype:
        """
        self.x = x
        self.y = y

    def __sub__(self, anderes_objekt):
        return Punkt(self.x - anderes_objekt.x, self.y - anderes_objekt.y)

    def __add__(self, anderes_objekt):
        return Punkt(self.x + anderes_objekt.x, self.y + anderes_objekt.y)

    def __mul__(self, anderes_objekt):
        if isinstance(anderes_objekt, Punkt):
            return self.x * anderes_objekt.x + self.y * anderes_objekt.y
        else:
            raise AttributeError("Nur Punkte oder Zahlen können multipliziert werden")

    def setze(self, x, y):
        self.x = x
        self.y = y

    def __delitem__(self, key):
        raise AttributeError("Kann nicht löschen.")

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise IndexError("Index muss 0=>x oder 1=>y sein!")

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise IndexError("Index muss 0=>x oder 1=>y sein!")

    def __len__(self):
        return 2

    def __abs__(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __str__(self):
        return "x: %.2f, y: %.2f, len: %.2f" % (self.x, self.y, abs(self))

    def skaliere(self, _skalierung):
        self.x *= _skalierung
        self.y *= _skalierung
        return self

    def subtrahiere(self, x_oder_punkt, y=None):
        if y is not None:
            self.x -= x_oder_punkt
            self.y -= y
        else:
            self.x -= x_oder_punkt[0]
            self.y -= x_oder_punkt[1]
        return self

    def addiere(self, x_oder_punkt, y=None):
        if y is not None:
            self.x += x_oder_punkt
            self.y += y
        else:
            self.x += x_oder_punkt[0]
            self.y += x_oder_punkt[1]

        return self


class Matrix2:
    def __init__(self, m11, m12, m21, m22):
        """
        Links oben, rechts oben, links unten, rechts unten

        :param m11:
        :type m11:
        :param m12:
        :type m12:
        :param m21:
        :type m21:
        :param m22:
        :type m22:
        :return:
        :rtype:
        """
        self._reihe1 = Punkt(m11, m12)
        self._reihe2 = Punkt(m21, m22)

    def __mul__(self, other):
        if isinstance(other, Punkt):
            return Punkt(other * self._reihe1, other * self._reihe2)
        else:
            raise AttributeError("Nur Punkte können multipliziert werden")
            # elif isinstance(other, Matrix2):
            #    pass
