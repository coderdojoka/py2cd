from py2cd import *
from pygame.constants import *
from py2cd.farben import *

__author__ = 'Mark Weinreuter'
# Images from and based on: http://inventwithpython.com/pyganim/

def aktualiserungs_funktion(t):
    pass


Spiel.init(400, 400, "Hallo Animation", aktualiserungs_funktion)
hintergrund_farbe = (100, 50, 50)
Spiel.setze_hintergrund_farbe(hintergrund_farbe)

zeit = 1000 / 11
Spiel.fps = 30

boltAnim = BildAnimation([('testimages/bolt_strike_0001.png', zeit),
                      ('testimages/bolt_strike_0002.png', zeit),
                      ('testimages/bolt_strike_0003.png', zeit),
                      ('testimages/bolt_strike_0004.png', zeit),
                      ('testimages/bolt_strike_0005.png', zeit),
                      ('testimages/bolt_strike_0006.png', zeit),
                      ('testimages/bolt_strike_0007.png', zeit),
                      ('testimages/bolt_strike_0008.png', zeit),
                      ('testimages/bolt_strike_0009.png', zeit),
                      ('testimages/bolt_strike_0010.png', zeit)])

boltAnim.start()
boltAnim.setze_wiederhole(True)
boltAnim.setze_position(200, 250)
boltAnim.oben = 20
boltAnim.rechts = Spiel.breite - boltAnim.breite - 10
boltAnim.zentriere_horizontal()

zeit = 1000 / 6
fireAnim = BildAnimation([("testimages/flame_a_0001.png", zeit),
                      ("testimages/flame_a_0002.png", zeit),
                      ("testimages/flame_a_0003.png", zeit),
                      ("testimages/flame_a_0004.png", zeit),
                      ("testimages/flame_a_0005.png", zeit),
                      ("testimages/flame_a_0006.png", zeit)], False)
fireAnim.start()
fireAnim.setze_wiederhole(True)
fireAnim.setze_position(200, 200)
fireAnim.unten = 0
fireAnim.links = 12
fireAnim.zentriere_vertikal()



Spiel.registriere_taste_gedrueckt(K_p, lambda a, b: boltAnim.pause())
Spiel.registriere_taste_gedrueckt(K_s, lambda a, b: boltAnim.start())

Spiel.starten()
