__author__ = 'Mark Weinreuter'

from pygame.constants import *

from py2cd import *
from py2cd.farben import *

links_down = False
rechts_down = False
oben_down = False
unten_down = False
speed = 1


def aktualisiere(dt):
    l.aendere_position(1, -1)
    p_box.aendere_position(1, -1)

    if links_down:
        r.aendere_position(-speed, 0)

    if rechts_down:
        r.aendere_position(speed, 0)

    if oben_down:
        r.aendere_position(0, -speed)

    if unten_down:
        r.aendere_position(0, speed)

    beruehrt = r.beruehrt_objekt(kollision)
    if beruehrt:
        kollision.farbe = ROT
    else:
        kollision.farbe = GRUEN


def links(gedrueckt, e):
    global links_down
    links_down = gedrueckt


def rechts(gedrueckt, e):
    global rechts_down
    rechts_down = gedrueckt


def oben(gedrueckt, e):
    global oben_down
    oben_down = gedrueckt


def unten(gedrueckt, e):
    global unten_down
    unten_down = gedrueckt


Spiel.init(300, 300, "Hallo Welt", aktualisiere)

p = Polygon([(20, 200), (10, 240), (40, 250), (50, 220)], ROT)
l = Linien([(300, 20), (400, 40), (50, 200)], geschlossen=True)
r = Rechteck(40, 40, 40, 40, BLAU)
kollision = Rechteck(48, 40, 40, 40, ROT)

schrift = Schrift(20)
t = Text("Hallo Welt", 200, 0, schrift, BLAU, ROT)
t.verstecke()

p_box = Rechteck(p.x, p.y, p.breite, p.hoehe, ROT)
p_box = Rechteck(l.x, l.y, l.breite, l.hoehe, (255, 0, 0, 120))

k = Kreis(260, 260, 50, GRUEN)

o = Oval(30, 40, 150, 50, BLAU)
b = Bogen(40, 100, 20, 40, 0, 270,dicke=5)

t.zentriere()

Spiel.registriere_taste_gedrueckt(K_a, links)
Spiel.registriere_taste_gedrueckt(K_w, oben)
Spiel.registriere_taste_gedrueckt(K_s, unten)
Spiel.registriere_taste_gedrueckt(K_d, rechts)

Spiel.starten()
