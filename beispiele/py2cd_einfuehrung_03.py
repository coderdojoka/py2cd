__author__ = "Mark Weinreuter"

from py2cd import *
from py2cd.farben import *

# Der erste Schritt um ein Spiel zu starten ist immer, der Initialisierungsfunktion init()
Spiel.init(640, 480, "Mein Spiel")


# Erstellt ein neues Fenster mit der gegebenen Größe von 640x480 und dem Titel "Mein Spiel"


# Diese Funktion wird aufgerufen, wenn das Spiel aktualisiert wird
def aktualisiere_spiel(delta):
    pass

# Ein Quadrat an der Position 300x200
reckt = Rechteck(300, 200, 100, 100, GELB)

# Ein Dreieck zeichenn, in dem alle Eckpunte angegeben werden
dreieck = Polygon([(300, 200), (350, 160), (400, 200)], ROT)

# Ein weiteres Quadrat
box = Rechteck(100, 100, 50, 50, GRUEN)

# Hilfsgitter einblenden
Spiel.zeichne_gitter()

# Funktion die aufgerufen wird, wenn das Spiel aktualisiert wird (fps mal)
Spiel.setze_aktualisierung(aktualisiere_spiel)

Spiel.starten()
"""
Um das Spiel zu starten, muss Spiel.start() aufgerufen werden. Dies sollte immer die letzte Anweisung sein.
"""
