__author__ = 'Mark Weinreuter'

from unittest.case import TestCase

import pygame

from py2cd.anim import BildAnimation
from py2cd.farben import *
from py2cd.flaeche import neue_pygame_flaeche
from py2cd.linie import Linie
from py2cd.poly import Polygon, AALinien, Linien
from py2cd.rechteck import Rechteck
from py2cd.spiel import Spiel


class PositionTest(TestCase):
    fenster_breite = 640
    fenster_hoehe = 480
    laufzeit = 10
    laufend = 0

    @staticmethod
    def beenden_timer(dt):
        PositionTest.laufend += dt
        if PositionTest.laufzeit < PositionTest.laufend:
            Spiel._ist_aktiv = False

    def setUp(self):
        Spiel.init(PositionTest.fenster_breite, PositionTest.fenster_hoehe, "Test", PositionTest.beenden_timer)

    def test1(self):
        r = Rechteck(0, 10, 100.533343343434, 10.3340, BLAU)
        p = Polygon([(20.444, 210.22), (200, 200), (450, 150)], ROT, 1)
        l = Linie((50, 50.67667), (200, 200), (150, 250, 50), 4)
        ll = Linien([(233, 456), (5.55, 2.21)], True, SCHWARZ)
        al = AALinien([(400, 450), (530.3304, 500)], True, GRUEN)
        a = BildAnimation([(neue_pygame_flaeche(400, 400), 10)], True)

        self._dimension_check(r)
        self._dimension_check(p)
        self._dimension_check(l)
        self._dimension_check(ll)
        self._dimension_check(al)
        self._dimension_check(a)
        Spiel.starten()

    def _dimension_check(self, zeichenbar=None):
        """

        :param zeichenbar:
        :type zeichenbar:
        :return:
        :rtype:
        """
        if zeichenbar is None:
            return

        print("Test abstand_xy()")
        abstand = 12.534234234235
        stellen = 5

        zeichenbar.links = abstand
        self.assertAlmostEqual(abstand, zeichenbar.x, stellen)

        zeichenbar.rechts = abstand
        self.assertAlmostEqual(zeichenbar._eltern_flaeche.breite - abstand - zeichenbar.breite, zeichenbar.x, stellen)

        zeichenbar.oben = abstand
        self.assertAlmostEqual(abstand, zeichenbar.y, stellen)

        zeichenbar.unten = abstand
        self.assertAlmostEqual(zeichenbar._eltern_flaeche.hoehe - zeichenbar.hoehe - abstand, zeichenbar.y, stellen)

        print("Done")

        zeichenbar.zentriere()

        print("Teste zentriere()")
        self.assertAlmostEqual((PositionTest.fenster_breite - zeichenbar.breite) / 2, zeichenbar.x, stellen)
        self.assertAlmostEqual((PositionTest.fenster_hoehe - zeichenbar.hoehe) / 2, zeichenbar.y, stellen)
        print("Done.")

    def tearDown(self):
        pygame.quit()
