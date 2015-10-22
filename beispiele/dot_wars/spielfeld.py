from py2cd import Spiel

__author__ = 'Mark Weinreuter'

from py2cd.farben import *
from py2cd.flaeche import ZeichenFlaeche

SPIELFELD_BREITE = 100
SPIELFELD_HOEHE = 100
BOX_GROESSE = 4

FREI = 1
RAND = 2
BELEGT = 3
BESUCHT = 4

FARBEN = [TUERKIS, ORANGE]
SPIELER_1 = -1
SPIELER_2 = -2


class SpielFeld(ZeichenFlaeche):
    zuege = 0
    punkte = [0, 0]
    flaeche = None
    felder = bytearray(SPIELFELD_BREITE * SPIELFELD_HOEHE)

    @classmethod
    def init(cls):
        cls.flaeche = ZeichenFlaeche(40, 40, (SPIELFELD_BREITE * BOX_GROESSE, SPIELFELD_HOEHE * BOX_GROESSE),
                                     eltern_flaeche=Spiel.gib_zeichen_flaeche(), farbe=None)
        cls.flaeche.zentriere()
        cls.flaeche.zeichne_rechteck_direkt(0, 0, cls.flaeche.breite, cls.flaeche.hoehe, farbe=FAST_WEISS)

        cls.flaeche.verstecke()

    @classmethod
    def feld_info(cls, x, y, farb_index):

        cls.zuege += 1
        if x < 0 or x >= SPIELFELD_BREITE or y < 0 or y >= SPIELFELD_HOEHE:
            return RAND

        farbe = cls.felder[x + y * SPIELFELD_HOEHE]

        if farbe == 0:
            cls.feld_besucht(x, y, farb_index)
            return FREI

        if farbe == farb_index:
            return BESUCHT
        else:
            return BELEGT


    @classmethod
    def feld_besucht(cls, x, y, farb_index):
        cls.flaeche.zeichne_rechteck_direkt(x * BOX_GROESSE, y * BOX_GROESSE, BOX_GROESSE, BOX_GROESSE, FARBEN[farb_index - 1])
        cls.felder[y * SPIELFELD_HOEHE + x] = farb_index
        cls.punkte[farb_index-1] += 1
