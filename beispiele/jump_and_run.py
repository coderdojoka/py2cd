from py2cd import ROT

__author__ = 'Mark Weinreuter'

from py2cd import *

# Initialisiert das Fenster
Spiel.init(400, 400, "Jump and Run")

gravitation = .4
bloecke = []


def aktualisiere(dt):
    bild.aendere_geschwindigkeit(0, gravitation)

    bewg_x = bild.x_geschwindigkeit * dt
    bewg_y = bild.y_geschwindigkeit * dt

    for block in bloecke:

        max = block.box_bewegung(bild, bewg_x, bewg_y)
        if max is None:
            bild.bewege(dt)
        else:
            if max[2] >= 3:
                bild.aendere_position(bewg_x, max[1])
                bild.y_geschwindigkeit = 0
            else:
                bild.aendere_position(max[0], bewg_y)


def springen(unten, pyg_ereignis):
    if unten:
        print("Sprung")
        bild.aendere_geschwindigkeit(0, -10)


bewege = 3


def links_unten(unten, pyg_ereignis):
    print("links unten:", unten)
    if unten:
        bild.aendere_geschwindigkeit(-bewege, 0)
    else:
        bild.aendere_geschwindigkeit(bewege, 0)  # bewegung aufheben


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
bloecke = [boden, boden2]

# Tastendruck-Funktionen registrieren.
Spiel.registriere_taste_gedrueckt(T_LEER, springen)
Spiel.registriere_taste_gedrueckt(T_LINKS, links_unten)
Spiel.registriere_taste_gedrueckt(T_RECHTS, rechts_unten)

# Das Spiel starten
Spiel.setze_aktualisierung(aktualisiere)
Spiel.starten()
