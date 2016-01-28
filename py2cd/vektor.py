from math import sqrt
from numbers import Number

__author__ = 'Mark Weinreuter'


class Vektor2:
    def __init__(self, x=0, y=0):
        """
        Erstellt einen neuen 2D-Vektor.

        :param x:
        :type x: Number|list[Number]
        :param y:
        :type y: Number
        """
        if (isinstance(x, list) or isinstance(x, tuple)) and len(x) > 2:
            y = x[1]
            x = x[0]

        self.__x = x
        self.__y = y

    def __len__(self):
        return self.laenge()

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise ValueError("Nur 0/1 können zugewiesen werden.")

    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        else:
            raise ValueError("Nur 0/1 können abgefragt werden: " + item)

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        self.__x = x

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y):
        self.__y = y

    def laenge(self):
        return sqrt(self.__x ** 2 + self.__y ** 2)

    def subtrahiere_selbst(self, other):
        self.__x -= other.__x
        self.__y -= other.__y
        return self

    def addiere_selbst(self, other):
        self.__x += other.__x
        self.__y += other.__y
        return self

    def multipliziere_selbst(self, faktor):
        self.__x *= faktor
        self.__y *= faktor
        return self

    def __add__(self, other):
        if not isinstance(other, Vektor2):
            raise AttributeError("%s muss ein Vektor2 sein" % str(other))

        return Vektor2(self.__x + other.__x, self.__y + other.__y)

    def __sub__(self, other):
        if not isinstance(other, Vektor2):
            raise AttributeError("%s muss ein Vektor2 sein" % str(other))

        return Vektor2(self.__x - other.__x, self.__y - other.__y)

    def __mul__(self, other):
        if not isinstance(other, Number):
            raise AttributeError("%s muss eine Zahl sein" % str(other))

        return Vektor2(self.__x * other, self.__y * other)

    def setze(self, x, y):
        """
        Setzt die x- und y-Komonente auf den gegebenen Wert.

        :param x: x-Wert
        :type x: float
        :param y: y-Wert
        :type y: float
        """
        self.__x = x
        self.__y = y

    def aendere(self, dx, dy):
        """
        Ändert die x- und y-Komonente um den gegebenen Wert.

        :param dx: x-Wert
        :type dx: float
        :param dy: y-Wert
        :type dy: float
        """

        self.__x += dx
        self.__y += dy

    def klone(self):
        return Vektor2(self.__x, self.__y)

    def __str__(self):
        return "(%.2f,%.2f)" % (self.__x, self.__y)
