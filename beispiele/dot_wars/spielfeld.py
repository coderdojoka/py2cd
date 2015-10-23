import logging
from threading import Lock

from py2cd import Spiel
from py2cd.farben import *
from py2cd.flaeche import ZeichenFlaeche

__author__ = 'Mark Weinreuter'

LIMIT_ZUEGE = 10000
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


class SpielFeld:
    zuege = 0
    punkte = [0, 0]
    flaeche = None
    spieler1 = None
    """
    :type: spieler.Spieler
    """
    spieler2 = None
    """
    :type: spieler.Spieler
    """
    felder = bytearray(SPIELFELD_BREITE * SPIELFELD_HOEHE)
    felder_sperre = Lock()
    zuege_sperre = Lock()

    @classmethod
    def init(cls, algo1_modul, algo1_name, algo2_modul, algo2_name):
        cls.flaeche = ZeichenFlaeche(40, 40, (SPIELFELD_BREITE * BOX_GROESSE, SPIELFELD_HOEHE * BOX_GROESSE),
                                     eltern_flaeche=Spiel.gib_zeichen_flaeche(), farbe=None)
        cls.flaeche.zentriere()
        cls.flaeche.zeichne_rechteck_direkt(0, 0, cls.flaeche.breite, cls.flaeche.hoehe, farbe=FAST_WEISS)

        cls.flaeche.verstecke()

        _modul1 = __import__(algo1_modul, globals(), locals())
        _modul2 = __import__(algo2_modul, globals(), locals())

        cls.spieler1 = getattr(_modul1, algo1_name)()
        cls.spieler2 = getattr(_modul2, algo2_name)()

        cls.spieler1.init(1, 2)
        cls.spieler2.init(2, 1)

        # Logging Ausgabe anpassen
        logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s', )

    @classmethod
    def start(cls):
        cls.spieler1.start()
        cls.spieler2.start()

    @classmethod
    def aktualisiere(cls):

        # Die neuen Punkte der beiden Spieler abfragen (thread-sicher)
        punkte1 = cls.spieler1.gib_punkte()
        punkte2 = cls.spieler2.gib_punkte()

        anz_punkte1 = len(punkte1)
        anz_punkte2 = len(punkte2)

        logging.debug("Punkte1: %d, Punkte2: %d" % (anz_punkte1, anz_punkte2))

        for x, y in punkte1:
            # Rechteck zeichnen
            cls.flaeche.zeichne_rechteck_direkt(x * BOX_GROESSE, y * BOX_GROESSE, BOX_GROESSE, BOX_GROESSE, FARBEN[0])

        for x, y in punkte2:
            # Rechteck zeichnen
            cls.flaeche.zeichne_rechteck_direkt(x * BOX_GROESSE, y * BOX_GROESSE, BOX_GROESSE, BOX_GROESSE, FARBEN[1])

        cls.punkte[0] += anz_punkte1
        cls.punkte[1] += anz_punkte2

        cls.zuege += anz_punkte1 + anz_punkte2

    @classmethod
    def beenden(cls):
        with cls.zuege_sperre:
            cls.zuege = LIMIT_ZUEGE + 1

        if cls.spieler2.is_alive():
            cls.spieler2.join()
        if cls.spieler1.is_alive():
            cls.spieler1.join()

    @classmethod
    def feld_info(cls, x, y, farb_index):

        cls.zuege += 1
        if x < 0 or x >= SPIELFELD_BREITE or y < 0 or y >= SPIELFELD_HOEHE:
            return RAND

        # Nur ein Thread einlassen, für andere Threads sperren:
        # felder Info aktualisieren
        cls.felder_sperre.acquire()
        try:
            farbe = cls.felder[x + y * SPIELFELD_HOEHE]

            if farbe == 0:
                # Daten aktualisieren
                cls.felder[y * SPIELFELD_HOEHE + x] = farb_index

                return FREI

            if farbe == farb_index:
                return BESUCHT
            else:
                return BELEGT

        finally:
            # Sperre wieder aufheben
            cls.felder_sperre.release()

    @classmethod
    def laueft_noch(cls):
        with cls.zuege_sperre:
            return cls.zuege < LIMIT_ZUEGE
