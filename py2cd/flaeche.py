import pygame

from py2cd.objekte import Zeichenbar

__author__ = 'Mark Weinreuter'


def neue_pygame_flaeche(breite, hoehe, alpha=False):
    """
    Erstellt einen neues pygame.Surface Objekt, das intern zum Zeichnen verwendet wird.
    :param breite:
    :type breite: int
    :param hoehe:
    :type hoehe: int
    :param alpha:
    :type alpha: bool
    :return:
    :rtype:pygame.Surface
    """
    if alpha:
        flaeche = pygame.Surface([breite, hoehe], pygame.SRCALPHA, 32)
        """:type:pygame.Surface"""
        flaeche.convert_alpha()
    else:
        flaeche = pygame.Surface([breite, hoehe])
        flaeche.convert()

    return flaeche


class ZeichenFlaeche(Zeichenbar):
    """
    Eine Fläche auf der gezeichnet werden kann. Es können z.B. Rechtecke oder Bilder gezeichnet werden.
    """

    def __init__(self, x, y, pygame_flaeche_breite, farbe=(0, 0, 0, 0), eltern_flaeche=None):
        """
        Eine neue Zeichenfläche.

        :param x:
        :type x: float
        :param y:
        :type y: float
        :param pygame_flaeche_breite:
        :type pygame_flaeche_breite: pygame.Surface|tuple(int,int,bool)
        :param eltern_flaeche:
        :type eltern_flaeche:
        :param farbe:
        :type farbe: tuple[int]
        :return:
        :rtype:
        """

        self._zeichenbare_objekte = []
        """
        Liste aller ZeichenbarenObjekte, die auf dieser Fläche gezeichnet werden
        :type: list[ZeichenbaresObjekt]
        """

        if isinstance(pygame_flaeche_breite, tuple):
            self.pyg_flaeche = neue_pygame_flaeche(*pygame_flaeche_breite)
        elif isinstance(pygame_flaeche_breite, pygame.Surface):
            self.pyg_flaeche = pygame_flaeche_breite
        else:
            raise ValueError("Bubberfisch")

        """
        Die eigentliche pygame Zeichenfläche auf der gezeichnet wird.
        :type:pygame.Surface
        """

        self.__zeichne_nur_bei_aenderung = False
        """
        Bestimmt, ob die Zeichenfläche jedes Mal neu bemalt wird, oder ob nur bei Änderungen erneut alle Kinder gezeichnet werden

        :type: bool
        """
        self.__hat_aenderungen = True
        """
        Flag, dass zusammen mit ____zeichne_nur_bei_aenderung bestimmt, ob neugezeichnet wird.

        :type: bool
        """

        super().__init__(x, y, self.pyg_flaeche.get_width(), self.pyg_flaeche.get_height(),
                         farbe, eltern_flaeche=eltern_flaeche)

    def zeichne_nur_bei_aenderung(self, wert=True):
        self.__zeichne_nur_bei_aenderung = wert
        self.__hat_aenderungen = True

    def fuege_hinzu(self, objekt):
        """
        Fügt ein zeichenbares Objekt zur Liste hinzu, d.h. es wird in jedem Update gezeichnet.
        :param objekt: das zeichenbare Objekt
        :type objekt:Zeichenbar
        :return:
        :rtype:
        """
        if not issubclass(objekt.__class__, Zeichenbar):
            raise AttributeError("Objekt muss von ZeichenbaresObjekt erben!")

        # falls das Objekt bereits registriert ist, entferne es
        if objekt._eltern_flaeche is not None:
            objekt._eltern_flaeche.entferne(objekt)

        # setzt die neue Elternfläche
        objekt._eltern_flaeche = self
        # Zur Liste von Objekten hinzufügen
        self._zeichenbare_objekte.append(objekt)

        # Die Zeichenfläche wurde geändert
        self.__hat_aenderungen = True

    def entferne(self, objekt):
        """
        Löscht das übergebene Objekt von dieser Zeichenfläche, falls es vorhanden ist
        :param objekt:
        :type objekt:
        :return:
        :rtype:
        """
        if objekt in self._zeichenbare_objekte:
            # Die Zeichenfläche wurde geändert
            self.__hat_aenderungen = True

            self._zeichenbare_objekte.remove(objekt)
            objekt._eltern_flaeche = None

    def zeichne_rechteck_direkt(self, x=0, y=0, breite=1, hoehe=1, farbe=(0, 0, 0), dicke=0):
        pygame.draw.rect(self.pyg_flaeche, farbe, (x, y, breite, hoehe), dicke)

    def zeichne_alles(self):

        if self.__zeichne_nur_bei_aenderung:
            if not self.__hat_aenderungen:
                return
            # Zurücksetzen, da jetzt neu gezeichnet wird
            self.__hat_aenderungen = False

        if self.farbe is not None:
            self.pyg_flaeche.fill(self.farbe)

        # zeichne alle
        for zb in self._zeichenbare_objekte:
            zb.zeichne()

    def render(self, pyg_zeichen_flaeche, x_offset=0, y_offset=0):
        self.zeichne_alles()
        return pyg_zeichen_flaeche.blit(self.pyg_flaeche, (self.x + x_offset, self.y + y_offset))

    def setze_farbmaske(self, farbe):
        self.pyg_flaeche.set_colorkey(farbe)

    def lese_farbmaske(self):
        return self.pyg_flaeche.get_colorkey()

    @property
    def zeichenbare_objekte(self):
        return self._zeichenbare_objekte


class HauptZeichenFlaeche(ZeichenFlaeche):
    def __init__(self, x, y, pygame_flaeche_breite, farbe=(255, 255, 255)):
        super().__init__(x, y, pygame_flaeche_breite, farbe=farbe)

    def zeichne_alles(self):
        self.pyg_flaeche.fill(self.farbe)

        # zeichne alle
        for zb in self._zeichenbare_objekte:
            zb.zeichne()
