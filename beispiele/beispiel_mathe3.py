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

plot = Plot(lambda x: 0, -4, 4, SCHWARZ, 100, 100)
plot.zentriere()

yAchse = Linie((Spiel.breite / 2, Spiel.hoehe), (Spiel.breite / 2, -Spiel.hoehe), SCHWARZ)
yAchse.zentriere()

# Sigmoid
for T in [0.1, 0.5, 1, 2.5]:
    plot = Plot(lambda e: 1 / (math.exp(e / T) + 1), -10, 10, BLAU, 100, 100)
    plot.zentriere()

Spiel.starten()
