__author__ = "Mark Weinreuter"

from py2cd import *
from py2cd.farben import *


# Der erste Schritt um ein Spiel zu starten ist immer, der Initialisierungsfunktion init()
Spiel.init(640, 480, "Mein Spiel")
"""Erstellt ein neues Fenster mit der gegebenen Größe von 640x480 und dem Titel "Mein Spiel"
"""

# ein neues Rechteckt mit Position 270x200 und Größe 100x100 mit Farbe Gelb
haus = Rechteck(270, 200, 100, 100, GELB)

# ein Polygon mit den Ecken aus der Liste und der Farbe Rot
dach = Polygon([(270, 200), (320, 160), (370, 200)], ROT)
dach.zentriere()
dach.oben = 160

# ein neues Rechteck mit Position 320x200 und Größe: 30x50 in grün
tuer = Rechteck(320, 250, 30, 50, GRUEN)

# Eine Linie zwischen den gegeben Punkten in Rot und 2 Pixel dick
boden = Linie((100, 300), (540, 300), ROT, 2)

# Text an der Stelle 0x0 mit einer Schrift in der Größe: 20
text = Text("Hallo Welt", 0, 0, Schrift(20))

# setzt die Position an die gegebene Stelle: oben mittig mit Abstand 10 Pixel vom Rand
text.setze_position((Spiel.breite - text.breite) / 2, Spiel.hoehe - text.hoehe - 10)

# Viel einfacher kann man dies auch so machen:
text.zentriere_horizontal()
text.unten = 10

zf = ZeichenFlaeche(20,20,(200, 200),SCHWARZ,eltern_flaeche=Spiel.gib_zeichen_flaeche())
k = Kreis(100, 100, 30, BLAU, eltern_flaeche=zf)

warte(100,lambda : zf.aendere_position(10, 0), True)

# Hilfsgitter anzeigen
Spiel.zeichne_gitter()

Spiel.gib_zeichen_flaeche().speichere_flaeche("test.png")

Spiel.starten()
"""
Um das Spiel zu starten, muss Spiel.start() aufgerufen werden. Dies sollte immer die letzte Anweisung sein!
"""
