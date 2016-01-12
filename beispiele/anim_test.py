from pygame.constants import *

from py2cd import *

__author__ = 'Mark Weinreuter'


# Images from and based on: http://inventwithpython.com/pyganim/

def aktualiserungs_funktion(dt):
    fireAnim.aendere_rotation(dt)


Spiel.init(400, 400, "Hallo Animation", aktualiserungs_funktion)
hintergrund_farbe = (100, 50, 50)
Spiel.setze_hintergrund_farbe(hintergrund_farbe)

zeit = 1000 / 11
Spiel.fps = 30

bilder_namen = generiere_namen_liste('testimages/bolt_strike_000%d.png', 1, 10)
boltAnim = BildAnimation(bilder_namen, anzeige_dauer=zeit)

boltAnim.start()
boltAnim.setze_wiederhole(True)

boltAnim.setze_position(200, 250)
boltAnim.oben = 20
boltAnim.rechts = Spiel.breite - boltAnim.breite - 10
boltAnim.zentriere_horizontal()
boltAnim.setze_rotation(90)

zeit = 1000 / 6
bilder_namen = generiere_namen_liste("testimages/flame_a_000%d.png", 1, 6)
fireAnim = BildAnimation(bilder_namen, False, anzeige_dauer=zeit)

fireAnim.start()
fireAnim.setze_wiederhole(True)
fireAnim.setze_position(200, 200)
fireAnim.unten = 0
fireAnim.links = 12
fireAnim.zentriere_vertikal()

fire2 = fireAnim.klone(200, 100)
fire2.start()

fire2.setze_skalierung(1.2)

Spiel.registriere_taste_gedrueckt(K_p, lambda a, b: boltAnim.pause())
Spiel.registriere_taste_gedrueckt(K_s, lambda a, b: boltAnim.start())

Spiel.starten()
