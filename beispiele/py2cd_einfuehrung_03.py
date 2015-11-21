__author__ = 'Mark Weinreuter'

from py2cd import *
from py2cd.farben import *

# Der erste Schritt, um ein Spiel zu starten ist immer init() aufzurufen
Spiel.init(640, 480, "Mein Spiel")
# Erstellt ein neues Fenster mit der gegebenen Größe von 640x480 und dem Titel "Mein Spiel"

skalierung = 1
vorzeichen = 1


# Diese Funktion wird aufgerufen, wenn das Spiel aktualisiert wird
def aktualisiere_spiel(delta):
    global skalierung, vorzeichen

    # skaliere langsam größer
    skalierung += delta * vorzeichen * .01

    bild.aendere_rotation(delta)
    bild.setze_skalierung(skalierung)

    # Skalierung umkehren
    if skalierung >= 3:
        vorzeichen = -1
    elif vorzeichen < 0 and skalierung <= .5:
        vorzeichen = 1


# Ein Quadrat an der Position 300x200
reckt = Rechteck(300, 200, 100, 100, GELB)
reckt.zentriere()

# Bild in Speicher laden
BildSpeicher.lade_bild("scratch", "testimages/scratch.png")
bild = BildSpeicher.gib_bild("scratch")

# Mittig zentrieren
bild.zentriere()

# Hilfsgitter einblenden
Spiel.zeichne_gitter()

# Funktion die aufgerufen wird, wenn das Spiel aktualisiert wird (fps mal)
Spiel.setze_aktualisierung(aktualisiere_spiel)

# Um das Spiel zu starten, muss Spiel.start() aufgerufen werden. Dies sollte immer die letzte Anweisung sein.
Spiel.starten()
