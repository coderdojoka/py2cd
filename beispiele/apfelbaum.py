__author__ = 'Mark Weinreuter'

from py2cd import *
from py2cd.farben import *

Spiel.init(640, 480, "Apfelbaum")

Spiel.zeichne_gitter()

stamm = Rechteck(190, 200, 20, 120, BRAUN)
krone = Kreis(140, 140, 60, MATT_GRUEN)
krone.setze_mitte(200, 200)

apfel_1 = Kreis(200, 200, 10, ROT)
apfel_2 = Kreis(190, 220, 10, ROT)
apfel_3 = Kreis(230, 180, 10, ROT)
apfel_4 = Kreis(180, 170, 10, ROT)
apfel_5 = Kreis(160, 160, 10, ROT)
apfel_6 = Kreis(150, 210, 10, ROT)



Spiel.starten()
