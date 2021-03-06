import pygame

from py2cd.objekte import SkalierbaresElement
from py2cd.objekte import ZeichenbaresElement

__author__ = 'Mark Weinreuter'


class Bild(ZeichenbaresElement, SkalierbaresElement):
    def render(self, pyg_zeichen_flaeche, x_off=0, y_off=0):
        pyg_zeichen_flaeche.blit(self.__pygame_bild, (self.x + x_off, self.y + y_off))

    def __init__(self, x, y, bild, eltern_flaeche=None, position_geaendert=lambda: None):
        """
        Ein neues Bild, das gezeichnet wird.

        :param x: die x-Position
        :type x: float
        :param y: die y-Position
        :type y: float
        :param bild: Entweder der Schlüssel für den BilderSpeicher oder eine pygame Surface
        :type bild: str|pygame.Surface
        :param alpha: Wahr, falls das Bild einen Alpha-Kanal hat (Transparenz)
        :type alpha: bool
        """
        if isinstance(bild, str):
            self.__pygame_bild = BildSpeicher.gib_pygame_bild(bild)
        elif isinstance(bild, pygame.Surface):
            self.__pygame_bild = bild
        else:
            raise ValueError("Bitte Schlüssel des Bildes im Bildspeicher angeben.")

        self.__orginal_pygame_surface = self.__pygame_bild
        self.__quelle = bild

        SkalierbaresElement.__init__(self, self)
        ZeichenbaresElement.__init__(self, x, y, self.__pygame_bild.get_width(), self.__pygame_bild.get_height(), farbe=None,
                                     eltern_flaeche=eltern_flaeche,
                                     position_geaendert=position_geaendert)

    def _rotation_skalierung_anwenden(self):
        self.__pygame_bild = pygame.transform.rotozoom(self.__orginal_pygame_surface, self._winkel, self._skalierung)

        # das umgebende Rechteck hat sich geändert => Bild Zentrum anpassen
        rect = self.__pygame_bild.get_rect()
        return rect.width, rect.height

    def klone(self, x, y):
        b = Bild(x, y, self.__quelle, self._eltern_flaeche)
        return b


class BildWechsler(ZeichenbaresElement):
    def __init__(self, x, y, bilder_namen_liste, eltern_flaeche=None, position_geaendert=lambda: None):
        # Candy für Faule
        if isinstance(bilder_namen_liste, str):
            bilder_namen_liste = [bilder_namen_liste]

        self.__name_liste = bilder_namen_liste
        self.__pygame_bilder = []
        self.aktuelles_bild = 0
        self.zeige_erstes_bild = lambda: self.zeige_bild(0)
        self.zeige_letztes_bild = lambda: self.zeige_bild(-1)

        if len(bilder_namen_liste) == 0:
            raise ValueError("Bilder Liste darf nicht leer sein!")

        groesse = (0, 0)
        # alle Bilder laden und Größe ermittlen
        for name in bilder_namen_liste:
            pg_bild = BildSpeicher.gib_pygame_bild(name)
            groesse = max(groesse[0], pg_bild.get_width()), max(groesse[1], pg_bild.get_height())

            self.__pygame_bilder.append(pg_bild)

        self.anzahl_bilder = len(self.__pygame_bilder)

        super().__init__(x, y, *groesse, farbe=None, eltern_flaeche=eltern_flaeche,
                         position_geaendert=position_geaendert)

    def zeige_bild(self, index):
        if index < 0:
            index = 0
        elif index >= self.anzahl_bilder:
            index = self.anzahl_bilder - 1

        self.aktuelles_bild = index

    def naechstes_bild(self):
        if self.aktuelles_bild == self.anzahl_bilder - 1:
            self.aktuelles_bild = 0
        else:
            self.aktuelles_bild += 1

    def vorheriges_bild(self):
        if self.aktuelles_bild == 0:
            self.aktuelles_bild = self.anzahl_bilder - 1
        else:
            self.aktuelles_bild -= 1

    def render(self, pyg_zeichen_flaeche, x_offset=0, y_offset=0):
        bild = self.__pygame_bilder[self.aktuelles_bild]
        # Bild zentriert zeichnen
        pyg_zeichen_flaeche.blit(bild, (
            self.x + x_offset + (self.breite - bild.get_width()) / 2,
            self.y + y_offset + (self.hoehe - bild.get_height()) / 2))

    def klone(self, x, y):
        BildWechsler(x, y, self.__name_liste, self._eltern_flaeche)


class BildSpeicher:
    __alle_pyg_bilder = {}  # TODO: besser?: weakref.WeakValueDictionary()

    @classmethod
    def ist_bild_vorhanden(cls, schluessel):
        return schluessel in cls.__alle_pyg_bilder

    @classmethod
    def lade_bild_aus_paket(cls, schluessel, pfad, alpha=True):
        import os
        here = os.path.dirname(__file__)
        pfad = os.path.join(here, 'resourcen/bilder', pfad)
        print(pfad)
        return cls.lade_bild(schluessel, pfad, alpha)

    @classmethod
    def lade_bilder_aus_paket(cls, pfade_liste, alpha=True):
        """

        :param pfade_liste:
        :type pfade_liste: list[str]
        :param alpha:
        :type alpha:
        :return:
        :rtype:
        """
        import os
        here = os.path.dirname(__file__)
        for pfad in pfade_liste:
            schluessel = pfad.rsplit("/")[-1].split(".")[0]
            pfad = os.path.join(here, 'resourcen/bilder', pfad)
            print(schluessel, pfad)
            cls.lade_bild(schluessel, pfad, alpha)

    @classmethod
    def liste_bilder_aus_paket(cls):
        """
        Listet alle vorhanden Bilder auf, die aus dem Paket geladen werden können.
        """

        import os
        here = os.path.dirname(__file__)
        liste = []

        def liste_rekursiv(pfad):
            kompletter_pfad = os.path.join(here, 'resourcen/bilder', pfad)
            dateien = os.listdir(kompletter_pfad)

            for datei in dateien:

                if os.path.isdir(os.path.join(here, 'resourcen/bilder', datei)):
                    liste_rekursiv(os.path.join(pfad, datei))

                elif len(datei) > 3 and datei[-3:] == "png":
                    print(os.path.join(pfad, datei))

        liste_rekursiv("")

    @classmethod
    def paket_bilder_lizenzen(cls):
        """
        Lädt die Lizenzsinformationen zu den in py2cd mitgelieferten Bildern.

        :return: Liste mit Lizenzinfos
        :rtype: list[str]
        """
        import os
        here = os.path.dirname(__file__)

        def lese_datei(dateipfad):
            pfad = os.path.join(here, 'resourcen/bilder', dateipfad)
            inhalt = ""
            try:
                datei = open(pfad)
                inhalt = datei.read()
                datei.close()

            except IOError as e:
                print(e)

            return inhalt

        lizensen = [lese_datei("license.txt")]
        return lizensen

    @classmethod
    def lade_bilder(cls, pfade_liste, alpha=True):
        """

        :param pfade_liste:
        :type pfade_liste: list[str]
        :param alpha:
        :type alpha:
        :return:
        :rtype:
        """

        for pfad in pfade_liste:
            # bildname ohne endung als schluessel
            schluessel = pfad.rsplit("/")[-1].split(".")[0]

            cls.lade_bild(schluessel, pfad, alpha)

    @staticmethod
    def _lade_pygbild_aus_datei(pfad, alpha=True):
        """
        Lädt das Bild aus der beschrieben Datei.
        ACHTUNG: Kann das Bild nicht geladen werden, wird ein Fehler geworfen!

        :param pfad: Pfad des Bildes, das geladen werden soll
        :type pfad: str
        :param alpha: Falls das Bild Transparenz unterstüzten soll
        :type alpha: bool
        :return: die pygame Surface
        :rtype: pygame.Surface
        """
        try:
            pyg_bild = pygame.image.load(pfad)
        except pygame.error as e:
            print("Fehler beim Laden des Bildes: ", e)
            raise AttributeError("Das Bild: %s konnte nicht geladen werden!" % pfad)

        # laut Doku soll convert() aufgerufen werden?!
        if alpha:
            pyg_bild = pyg_bild.convert_alpha()
        else:
            pyg_bild = pyg_bild.convert()

        return pyg_bild

    @classmethod
    def lade_bild(cls, schluessel, pfad, alpha=True):
        bild = cls._lade_pygbild_aus_datei(pfad, alpha)
        cls.__alle_pyg_bilder[schluessel] = bild

        return bild

    @classmethod
    def gib_bild(cls, schluessel, x=0, y=0):
        """
        Lädt das Bild aus dem Bildspeicher und gibt ein neues Bild Objekt zurück.

        :param schluessel:
        :type schluessel: str
        :param x:
        :type x: int
        :param y:
        :type y: int
        :return:
        :rtype: py2cd.Bild
        """
        if schluessel not in cls.__alle_pyg_bilder:
            raise ValueError(("Bild %s nicht im BildSpeicher vorhanden. Füge es zuerst hinzu!" % schluessel))

        return Bild(x, y, cls.__alle_pyg_bilder[schluessel])

    @classmethod
    def gib_pygame_bild(cls, schluessel):
        if schluessel not in cls.__alle_pyg_bilder:
            raise ValueError("%s ist nicht im BildSpeicher vorhanden. Füge es zuerst hinzu!" % schluessel)

        return cls.__alle_pyg_bilder[schluessel]


if __name__ == "__main__":
    print(BildSpeicher.paket_bilder_lizenzen())
