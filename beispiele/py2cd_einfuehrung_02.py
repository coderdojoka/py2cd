__author__ = "Mark Weinreuter"

from py2cd import *
from py2cd.farben import *

# Der erste Schritt um ein Spiel zu starten ist immer, der Initialisierungsfunktion init()
Spiel.init(640, 480, "Mein Spiel")
# Erstellt ein neues Fenster mit der gegebenen Größe von 640x480 und dem Titel "Mein Spiel"

Spiel.fps = 30  # Setzt die Neuzeichnungsrate auf 30mal pro Sekunde. (Diese Anweisung ist optional, da 30 der Standartwert ist)

"""
Ein Spiel (Programme im Allgemeinen) zeichnen wiederholt "Bilder" auf den Bildschirm. Je nach Anwendung wird der
Bildschirm unterschiedlich oft aktualisiert.
Die Aktualisierungsrate wird als oftmals als "Frames per second", kurz "fps" bezeichnet.
Übersetzt bedeutet dies einfach "Neuzeichnung pro Sekunde".
Folglich hat die Anweisung: 'Spiel.fps = 60', die Bedeutung, dass das Spiel 60mal pro Sekunde neugezeichnet wird.
Bei Spielen ist als grobe Grenze gesetzt, dass es gut mit 60 Fps läuft.
Für das menschliche Auge reicht es allerdings auch aus sicherzustellen, das ein Spiel zumindest noch mit 30 Fps läuft,
da ab diesen Wert die einzelnen Bilder nicht mehr unterscheiden werden können.
"""


# Diese Funktion wird aufgerufen wenn die Maus bewegt wurde
def maus_bewegt(evt):
    if reckt.punkt_in_rechteck(evt.pos):
        reckt.farbe = GRUEN
    else:
        reckt.farbe = GELB

# Geschwindigkeit in x (rechts/links) und y (oben/unten) Richtung
bewegung_x = -5
bewegung_y = -4

# Diese Funktion wird aufgerufen, wenn das Spiel aktualisiert wird
def aktualisiere_spiel(delta):
    global bewegung_x,bewegung_y

    # 1. Variante: Die Box bewegen, prallt automatisch von der Wand ab
    box_gruen.mache_schritte()

    # 2. Variante, wir müssen selbst auf Kollision mit der Wand testen

    # am rechten und linken Rand die x-Richtung ändern
    if box_rot.beruehrt_linken_oder_rechten_rand():
        bewegung_x *= -1

    # am obereren und unteren Rand die y-Richtung ändern
    if box_rot.beruehrt_oberen_oder_unteren_rand():
        bewegung_y *= -1

    # bewege die Box
    box_rot.aendere_position(bewegung_x, bewegung_y)

    # Wenn die beiden Boxen sich berühren, Farbe ändern
    if box_gruen.beruehrt_objekt(box_rot):
        box_gruen.farbe = BLAU
    else:
        box_gruen.farbe = GRUEN

reckt = Rechteck(270, 200, 100, 100, GELB)

dreieck = Polygon([(270, 200), (320, 160), (370, 200)], ROT)

box_gruen = Rechteck(13, 10, 50, 50, GRUEN)
box_rot = Rechteck(107, 120, 80, 80, ROT)


# Geschwindigkeit in x (rechts/links) und y (oben/unten) Richtung
box_gruen.setze_geschwindigkeit(5,5)
# Vom Rand abprallen aktivieren
box_gruen.pralle_vom_rand_ab(True)

# Funktion die aufgerufen wird, wenn die Maus bewegt wurde
Spiel.registriere_maus_bewegt(maus_bewegt)

# Funktion die aufgerufen wird, wenn das Spiel aktualisiert wird (fps mal)
Spiel.setze_aktualisierung(aktualisiere_spiel)

Spiel.starten()
"""
Um das Spiel zu starten, muss Spiel.start() aufgerufen werden. Dies sollte immer die letzte Anweisung sein.
"""
