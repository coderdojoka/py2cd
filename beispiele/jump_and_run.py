from py2cd import ROT

__author__ = 'Mark Weinreuter'

from py2cd import *

# Initialisiert das Fenster
Spiel.init(400, 400, "Jump and Run")

gravitation = .4


def aktualisiere(dt):
    bild.aendere_geschwindigkeit(0, gravitation)

    bewg_y = bild.y_geschwindigkeit * dt

    for block in bloecke:
        max_y = bild.kollision_oben_unten(block, bewg_y)
        if max_y is not None:
            bild.setze_geschwindigkeit(0, 0)
            bewg_y = max_y
            break

    bild.aendere_position(0, bewg_y)


def springen(unten, pyg_ereignis):
    if unten:
        print("Sprung")
        bild.aendere_geschwindigkeit(0, -10)


bewege = 3


def solange_links(dt):
    bewg_x = -bewege * dt
    for block in bloecke:
        max = bild.kollision_links_rechts(block, bewg_x)
        if max is not None:
            bewg_x = max
            break
    bild.aendere_position(bewg_x, 0)


def solange_rechts(dt):
    bewg_x = bewege * dt
    for block in bloecke:
        max = bild.kollision_links_rechts(block, bewg_x)
        if max is not None:
            bewg_x = max
            break
    bild.aendere_position(bewg_x, 0)


def rechts_unten(unten, pyg_ereignis):
    print("rechts unten:", unten)
    if unten:
        bild.aendere_geschwindigkeit(bewege, 0)
    else:
        bild.aendere_geschwindigkeit(-bewege, 0)  # bewegung aufheben


# Bild laden in den Speicher laden und unter dem Schlüssel "scratch" ablegen
BildSpeicher.lade_bild("scratch", "testimages/scratch.png")
# Bild aus dem Speicher über seinen Schlüssel holen
bild = BildSpeicher.gib_bild("scratch", 10, 10)

boden = Rechteck(0, 0, Spiel.breite, 20, ROT)
boden.unten = 20

boden2 = Rechteck(300, 300, 40, 20, ROT)
boden3 = Rechteck(350, 100, 40, 20, ROT)

bloecke = [boden, boden2, boden3]

# Tastendruck-Funktionen registrieren.
Spiel.registriere_taste_gedrueckt(T_LEER, springen)

Spiel.registriere_solange_taste_unten(T_LINKS, solange_links)
Spiel.registriere_solange_taste_unten(T_RECHTS, solange_rechts)

# Das Spiel starten
Spiel.setze_aktualisierung(aktualisiere)
Spiel.starten()
