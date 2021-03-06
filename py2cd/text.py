import pygame
import pygame.font

from py2cd.objekte import ZeichenbaresElement

__author__ = 'Mark Weinreuter'


class Schrift:
    """
    Eine Schrift, die zum Darstellen von Text verwendet werden kann.
    """

    def __init__(self, schrift_groesse, schrift_art="freesansbold"):
        """

        :param schrift_groesse: Gröpße der Schrift
        :type schrift_groesse: int
        :param schrift_art: Der Name der Schrift, z.B. Arial
        :type schrift_art: str
        """
        self.schrift_art = schrift_art
        self.schrift_groesse = schrift_groesse
        self._pyg_schrift = pygame.font.SysFont(schrift_art, schrift_groesse)

    def berechne_groesse(self, text):
        """
        Gibt die Größe des Textes zurück
        :param text:
        :type text:
        :return:
        :rtype:
        """
        return self._pyg_schrift.size(text)

    def render(self, text, aa, farbe, hintergrund):
        return self._pyg_schrift.render(text, aa, farbe, hintergrund)

    @classmethod
    def gib_vorhandene_schriftarten(cls):
        fonts = pygame.font.get_fonts()
        return fonts

    @classmethod
    def gib_standart_schrift(cls):
        return pygame.font.get_default_font()


class Text(ZeichenbaresElement):
    """
    Ein Text, der angezeigt werden kann.
    """

    def setze_text(self, text):
        self.__text = text
        dim = self.schrift.berechne_groesse(self.__text)
        self._aendere_groesse(*dim)

    def render(self, pyg_zeichen_flaeche, x_offset=0, y_offset=0):
        return pyg_zeichen_flaeche.blit(self.schrift.render(self.__text, True, self.farbe, self.hintergrund),
                                        (self.x + x_offset, self.y + y_offset))

    def __init__(self, text, x=0, y=0, schrift=Schrift(20), farbe=(0, 0, 0), hintergrund=None, eltern_flaeche=None):
        """
        Ein neuer Text an der angebenen Position
        :param text:
        :type text:str
        :param x:
        :type x: int
        :param y:
        :type y: int
        :param schrift:
        :type schrift:py2cd.text.Schrift
        :param farbe:
        :type farbe:tuple[int]
        :param hintergrund:
        :type hintergrund: tuple[int]
        """
        self.hintergrund = hintergrund
        """
        Die Hintergrundfarbe
        :type: tuple[int]
        """
        self.__text = text
        """
        Der anzuzeigende Text
        :type:str
        """
        self.schrift = schrift
        """
        Die verwendete Schrift
        :type:Schrift
        """

        # berechne Größe
        dim = self.schrift.berechne_groesse(self.__text)

        # Eltern Konstruktor
        super().__init__(x, y, dim[0], dim[1], farbe, eltern_flaeche)

    def klone(self, x, y):
        t = Text(self.__text, x, y, self.schrift, self.farbe, self.hintergrund, self._eltern_flaeche)
        return t
