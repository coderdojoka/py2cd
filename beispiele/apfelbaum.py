__author__ = "Norbert"

from py2cd import *
from py2cd.farben import *

Spiel.init(640, 480, "Mein Spiel")
haus = Rechteck(270, 200, 100, 100, GELB)
# ein Polygon mit den Ecken aus der Liste und der Farbe Rot
dach = Polygon([(270, 200), (320, 160), (370, 200)], ROT)
# ein neues Rechteck mit Position 320x200 und Größe: 30x50 in grün
tuer = Rechteck(320, 250, 30, 50, GRUEN)
# Eine Linie zwischen den gegeben Punkten in Rot und 2 Pixel dick
boden = Linie((100, 300), (550, 300), ROT, 2)

# und noch viel mehr Objekte malen :D
baum = Rechteck(450, 250, 10, 50, BRAUN)
laub = Kreis(390, 110, 70, MATT_GRUEN)
apfel1 = Kreis(450, 150, 10, ROT)
apfel2 = Kreis(480, 140, 10, HELL_GELB)
apfel3 = Kreis(410, 180, 11, ROT)
apfel4 = Kreis(440, 140, 10, ROT)
apfel5 = Kreis(500, 170, 10, ROT)
apfel6 = Kreis(450, 210, 11, HELL_GELB)
apfel7 = Kreis(400, 200, 10, ROT)
apfel8 = Kreis(490, 200, 10, ROT)
Hund = Kreis(150, 250, 20, BRAUN)
hundkopf = Kreis(180, 240, 15, BRAUN)
schwanz = Rechteck(125, 260, 40, 4, BRAUN)
fuss1 = Rechteck(155, 280, 5, 20, BRAUN)
fuss2 = Rechteck(165, 280, 5, 20, BRAUN)
fuss3 = Rechteck(175, 280, 5, 20, BRAUN)
fuss4 = Rechteck(182, 280, 5, 20, BRAUN)
auge = Kreis(200, 248, 4, WEISS)
ohren = Polygon([(190, 242), (195, 238), (200, 242)], BLAU)

# Hilfsgitter anzeigen
Spiel.zeichne_gitter()
Spiel.starten()
