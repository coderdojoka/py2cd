from py2cd import *
from py2cd.farben import *

__author__ = 'Mark Weinreuter'

import math


def func(x):
    return x ** 3 - 5 * x ** 2 + 3 * x + 1


i = 0.0
while i <= 3:
    print(str(i) + ": " + str(func(i)))
    i += .5

Spiel.init(640, 480, "Hallo Mathe")

yAchse = Linie((Spiel.breite / 2, 0), (Spiel.breite / 2, Spiel.hoehe), SCHWARZ)
xAchse = Linie((0, Spiel.hoehe / 2), (Spiel.breite, Spiel.hoehe / 2))
# yAchse.zentriere()

# Sigmoid
plot = Plot(func, 0, 10, BLAU, 40, 40)

plot = Plot(lambda x: -.5 * math.cos(x) + 0 * math.sin(x), -40, 40, ROT, 100, 100)
plot.zentriere()

plot = Plot(lambda x: 0 * math.cos(x) + 1 * math.sin(x), -4, 4, GRUEN, 100, 100)
plot.zentriere()

Spiel.starten()
