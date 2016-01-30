import py2cd.bbox
import py2cd.vektor

__author__ = 'Mark Weinreuter'


class Kamera():
    x = 0
    y = 0
    breite = 0
    hoehe = 0
    zentrum = None
    """

    :type: py2cd.bbox.BBox
    """
    __soll_position = py2cd.vektor.Vektor2()
    verschiebung = py2cd.vektor.Vektor2(0, 0)

    """
    :type: py2cd.bbox.BBox
    """

    @classmethod
    def init(cls, x, y, breite, hoehe):
        cls.x = x
        cls.y = y
        cls.breite = breite
        cls.hoehe = hoehe

        cls.zentrum = None
        """
        :type: py2cd.objekte.Zeichenbar
        """

        cls.__soll_position = py2cd.vektor.Vektor2(.5 * cls.breite, .55 * cls.hoehe)

        """
        :type: py2cd.vektor.Vektor2
        """

    @classmethod
    def setze_zentrum(cls, zentrum, x_faktor=.5, y_faktor=.55):
        """

        :param y_faktor:
        :type y_faktor:
        :param x_faktor:
        :type x_faktor:
        :param zentrum:
        :type zentrum: py2cd.bbox.BBox
        :return:
        :rtype:
        """
        # Figur muss existieren
        assert zentrum is not None
        assert isinstance(zentrum, py2cd.bbox.BBox)
        cls.zentrum = zentrum
        cls.__soll_position = py2cd.vektor.Vektor2(x_faktor * cls.breite, y_faktor * cls.hoehe)

        cls.zentrum.position_geaendert.registriere(cls.berechne_verschiebung)

    @classmethod
    def entferne_zentrale_figur(cls):
        assert cls.zentrum is not None
        cls.zentrum = None

    @classmethod
    def berechne_verschiebung(cls):
        cls.verschiebung = cls.__soll_position - cls.zentrum.mitte
