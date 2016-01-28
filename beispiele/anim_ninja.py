from pygame.constants import *

from py2cd import *

__author__ = 'Mark Weinreuter'


def aktualiserungs_funktion(dt):
    if logo.ist_sichtbar():
        logo.aendere_rotation(5 * dt)
        logo.aendere_position(-3 * dt, -1 * dt)


Spiel.init(600, 400, "Hallo Animation", aktualiserungs_funktion)
hintergrund_farbe = (100, 50, 50)
Spiel.setze_hintergrund_farbe(hintergrund_farbe)

zeit = 100

def bild_gewechselt(bild_nummer):
    if bild_nummer == 4:
        logo.zeige()


def animation_zuende():
    print("zu ende")


ninjaAnim = BildAnimation([('testimages/n1.png', zeit),
                           ('testimages/n2.png', zeit),
                           ('testimages/n3.png', zeit),
                           ('testimages/n4.png', zeit),
                           ('testimages/n5.png', zeit),
                           ('testimages/n6.png', zeit),
                           ('testimages/n7.png', zeit)])

ninjaAnim.setze_skalierung(.75)
ninjaAnim.registriere_wenn_bild_gewechselt(bild_gewechselt)
ninjaAnim.registriere_wenn_geendet(animation_zuende)
ninjaAnim.rechts = 20
ninjaAnim.unten = 20
ninjaAnim._zeige_letztes_bild = True
ninjaAnim.setze_wiederhole(False)

BildSpeicher.lade_bild("logo", "testimages/python_logo.png")
logo = BildSpeicher.gib_bild("logo")
logo.setze_skalierung(.75)


def neu_starten():
    logo.verstecke()
    logo.links = ninjaAnim.links
    logo.oben = ninjaAnim.oben + 80
    ninjaAnim.stop()
    ninjaAnim.start()


neu_starten()

Spiel.registriere_taste_gedrueckt(K_s, lambda a, b: neu_starten())

Spiel.starten()
