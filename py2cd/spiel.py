import logging
import sys

import pygame
import pygame.freetype
from pygame.constants import *

import py2cd
import py2cd.pygameui as ui
from py2cd.ereignis import *
from py2cd.farben import *
from py2cd.kamera import Kamera
from py2cd.objekte import Aktualisierbar
from py2cd.tasten import Taste

__author__ = 'Mark Weinreuter'

logger = logging.getLogger(__name__)


class Spiel:
    """
    Die Hauptklasse des Spiels.
    Es muss Spiel.init() und Spiel.starten() aufgerufen werden.
    """

    _unten_tasten = []
    """
    Liste der Tasten, die einen Unten-Aktualisierungshandler haben.

    :type: list[py2cd.Taste]
    """

    _alle_tasten_bearbeiter = EreignisBearbeiter()
    """
    Wird aufgerufen, falls eine Tasten gedrückt wird.

    :type: py2cd.EreignisBearbeiter
    """

    _zeige_gui = False
    """
    Wenn dieses Flag gesetzt ist, wird die pygameui GUI gezeichnet.

    :type: bool

    """

    _ist_aktiv = True
    """
    Solange dieses Flag auf True gesetzt ist, läuft die Spiel.

    :type: bool
    """

    breite = 640
    """
    Die Breite des Spiels (Fensters).

    :type: int"""
    hoehe = 480
    """
    Die Höhe des Spiels (Fensters).

    :type: int
    """
    fps = 30
    """
    Die Anzahl der Aktualisierungen pro Sekunde ("Frames per second).

    :type: float """

    __haupt_flaeche = None
    """
    Die ZeichenFlaeche des Spiels (Fensters)
    :type: py2cd.flaeche.ZeichenFlaeche """

    standard_flaeche = None
    """
    Die Fläche zu der Objekte standartmäßig hinzugefügt werden, falls die Elternfläche nicht explizit angegben ist.
    :type: py2cd.zeichen_flaeche.ZeichenFlaeche
    """

    _tasten = {}
    """
    Tastendruck-Funktionen werden hier gespeichert.

    :type: dict[int, py2cd.Taste]
    """

    _clock = pygame.time.Clock()
    """
    Taktgeber für das Spiel um die Fps einzustellen.

    :type: pygame.time.Clock
    """

    __aktualisiere = EreignisBearbeiter()
    """
    Die Funktion, die aufgerufen wird, wenn das Spiel aktualisiert wird (fps mal).

    :type: py2cd.EreignisBearbeiter
    """

    zeit_unterschied_ms = 0
    """
    Der Zeitunterschied zwischen den aktuellen Frames.

    :type: float
    """

    _mausBewegt = EreignisBearbeiter()
    """
    Die Funtion, die aufgerufen wird wenn die Maus beweget wird.

    :type: py2cd.EreignisBearbeiter
    """

    _maus_taste_gedrueckt = EreignisBearbeiter()
    """
    Funktion die aufgerufen wird, wenn eine Taste gedrückt wurde.

    :type: py2cd.EreignisBearbeiter
    """

    _spiel_wird_beendet = EreignisBearbeiter()
    """
    Funktion die aufgerufen wird, wenn das Spiel beendet wird.

    :type: py2cd.EreignisBearbeiter
    """

    _maus_taste_losgelassen = EreignisBearbeiter()
    """
    Die Funktion die aufgerufen wird, wenn die Maus losgelassen wird.

    :type: py2cd.EreignisBearbeiter()
    """


    @classmethod
    def init(cls, breite=640, hoehe=480, titel="Py2cd Zeichenbibliothek", aktualisierungs_funktion=lambda zeit: None,
             haupt_flaeche="py2cd.flaeche.HauptZeichenFlaeche"):
        """
        Initialisiert das Spiel.

        HINWEIS: Diese Funktion muss aufgerufen werden, bevor py2cd Funktionen verwendet werden können.

        :param breite: die Fensterbreite
        :type breite: int
        :param hoehe: die Fensterhöhe
        :type hoehe: int
        :param titel: Der Fenstertitel
        :type titel: str
        :param aktualisierungs_funktion: die Aktualisierungsfunktion, die bei jedem Neuzeichnen aufgerufen wird (fps mal pro sekunde)
        :type aktualisierungs_funktion: (float) -> None
        """

        # Initialisiert pygame
        pygame.init()

        # Versions Info
        logger.debug("Python: ", sys.version)
        logger.debug("Pygame: ", pygame.version.ver)

        # die spiel schleife
        Spiel.__aktualisiere.registriere(aktualisierungs_funktion)

        # Dimension des Fensters
        Spiel.breite = breite
        Spiel.hoehe = hoehe
        Kamera.init(0,0, breite, hoehe)

        # Die Hauptzeichenfläche erstellen
        import importlib
        module_name, class_name = haupt_flaeche.rsplit(".", 1)
        class_ = getattr(importlib.import_module(module_name), class_name)
        instance = class_(0, 0, pygame.display.set_mode((breite, hoehe)), WEISS)

        if not isinstance(instance, py2cd.flaeche.HauptZeichenFlaeche):
            raise AttributeError("Hauptfläche muss vom Typ HauptFlaeche sein.")

        # die Hauptzeichenfläche des Spiels!
        Spiel.__haupt_flaeche = instance
        """
        :type: py2cd.flaeche.ZeichenFlaeche
        """

        Spiel.standard_flaeche = Spiel.__haupt_flaeche
        """
        Kann geändert werden, falls viele neue Objekte auf eine eigene Zeichenfläche erstellt werden sollen.

        :type: py2cd.flaeche.ZeichenFlaeche
        """

        # Fenstertitel
        Spiel.setze_fenster_titel(titel)

        # setze ESC handler um das Fenster zu schließen
        Spiel.registriere_taste_gedrueckt(K_ESCAPE, lambda down, y: Spiel.beenden())

    @classmethod
    def beenden(cls):
        """
        Beendet das Spiel und schließt das Fenster.
        """
        cls._spiel_wird_beendet()
        pygame.quit()
        sys.exit()

    @staticmethod
    def starten():
        """
        Startet das Spiel. Hinweis, diese Funktion blockiert und kehrt nie zurück!
        """
        # erster tick für zeit_unterschied_ms
        Spiel._clock.tick(Spiel.fps)
        while Spiel._ist_aktiv:  # spiel schleife

            # wir gehen alle events durch
            for ereignis in pygame.event.get():

                # Fenster schließen
                if ereignis.type == QUIT:
                    Spiel.beenden()

                if not Spiel._zeige_gui or not ui.reagiere(ereignis):
                    # Maus bewegt
                    if ereignis.type == MOUSEMOTION:
                        if Spiel._mausBewegt:
                            Spiel._mausBewegt(ereignis)

                    # Maustaste gedrückt
                    elif ereignis.type == MOUSEBUTTONDOWN:
                        if Spiel._maus_taste_gedrueckt:
                            Spiel._maus_taste_gedrueckt(ereignis)

                    # Maustaste losgelassen
                    elif ereignis.type == MOUSEBUTTONUP:
                        if Spiel._maus_taste_losgelassen:
                            Spiel._maus_taste_losgelassen(ereignis)

                    # Taste losgelassen
                    elif ereignis.type == KEYUP:
                        # allgemeiner Bearbeiter
                        Spiel._alle_tasten_bearbeiter(False, ereignis)

                        # spezialisierter Handler
                        if ereignis.key in Spiel._tasten:
                            taste = Spiel._tasten[ereignis.key]

                            taste.oben(ereignis)

                            # liste der tasten, die dauerhaft unten events feuern
                            Spiel._unten_tasten.remove(taste)

                    # Taste gedrückt
                    elif ereignis.type == KEYDOWN:
                        # allgemeiner Bearbeiter
                        Spiel._alle_tasten_bearbeiter(True, ereignis)

                        # spezialisierter Handler
                        if ereignis.key in Spiel._tasten:
                            taste = Spiel._tasten[ereignis.key]
                            taste.unten(ereignis)

                            # für die faule unten variante
                            if taste not in Spiel._unten_tasten:
                                Spiel._unten_tasten.append(taste)

            # lässt das Spiel mit ca. dieser fps laufen und fragt vergangene Zeit ab
            Spiel.zeit_unterschied_ms = Spiel._clock.tick(Spiel.fps)

            # relativer Zeitunterschied
            delta = Spiel.zeit_unterschied_ms / Spiel.fps

            for taste in Spiel._unten_tasten:
                taste.wenn_unten_bearbeiter(delta)

            Spiel.__aktualisiere(delta)
            Aktualisierbar.aktualisiere_alle(delta, Spiel.zeit_unterschied_ms)

            # zeichne alles!!!
            Spiel.__haupt_flaeche.zeichne_alles()

            # falls wir eine GUI haben
            if Spiel._zeige_gui:
                ui.aktualisiere(Spiel.zeit_unterschied_ms)
                ui.zeichne(Spiel.__haupt_flaeche.pyg_flaeche)

                # muss aufgerufen werden um Änderungen anzuzeigen
            pygame.display.flip()  # update besser?

    @classmethod
    def zeige_gui(cls):
        cls._zeige_gui = True

    @classmethod
    def verstecke_gui(cls):
        cls._zeige_gui = False

    @staticmethod
    def setze_fenster_titel(titel):
        """
        Setzt den Titel für das Fenster.

        :param titel: Der Fenstertitel
        :type titel: str
        """
        pygame.display.set_caption(titel)

    @classmethod
    def setze_hintergrund_farbe(cls, farbe):
        """
        Setzt die Hintergrundfarbe des Fensters.

        :param farbe: Die Farbe
        :type farbe: tuple(int)
        """
        cls.__haupt_flaeche.farbe = farbe

    @classmethod
    def zeichne_gitter(cls, groesse=50):
        """
        Zeichnet ein Hilfsgitter mit der gegebenen Gittergröße.

        :param groesse: die Größe, Standart: 50
        :type groesse: int
        """

        # Wir importieren diese erst hier, um Kreis-Abhängigkeiten zu verhindern
        from py2cd import Linie, Text, ZeichenFlaeche
        from py2cd.farben import HELL_GRAU
        from py2cd.text import Schrift

        zf = ZeichenFlaeche(0, 0, (cls.breite, cls.hoehe, True), eltern_flaeche=cls.__haupt_flaeche)
        zf.zeichne_nur_bei_aenderung(True)
        zf.ignoriere_kamera = True
        # Anzahl an horizontalen Gitterlinien
        anzahl = round(cls.breite / groesse)
        schrift = Schrift(24)
        for i in range(1, anzahl):
            Linie((i * groesse, 0), (i * groesse, cls.hoehe), HELL_GRAU, eltern_flaeche=zf)
            t = Text("%d" % (i * groesse), i * groesse, 2, schrift=schrift, eltern_flaeche=zf)

        # Anzahl an vertikalen Gitterlinien
        anzahl = round(cls.hoehe / groesse)
        for i in range(1, anzahl):
            Linie((0, i * groesse), (cls.breite, i * groesse), HELL_GRAU, eltern_flaeche=zf)
            t = Text("%d" % (i * groesse), 2, i * groesse, schrift=schrift, eltern_flaeche=zf)

    @classmethod
    def registriere_alle_tasten(cls, funktion):
        """
        Die Funktion wird aufgerufen, wenn eine beliebige Taste gedrückt wird

        :param funktion:
        :type funktion: (bool, Any) -> None
        """
        cls._alle_tasten_bearbeiter.registriere(funktion)

    @staticmethod
    def registriere_taste_gedrueckt(taste, funktion):
        """
        Registriert eine Funktion, die ausgeführt wird, wenn die angegebene Taste gedrückt wird.

        :param taste: die Taste z.B. die a-Taste ist 97. Die wichtigsten Tasten sind vordefiniert, so entspricht T_a der 'a'-Taste
        :type taste: int
        :param funktion: Die Funktion die aufgerufen wird. Sie muss 2 Parameter akzeptieren, der
        Erste gibt an, ob die Taste gedrückt oder losgelassen ist und der Zweite ist das Event Objekt
        :type funktion: (bool, py2cd.Taste) -> None
        """
        if taste not in Spiel._tasten:
            Spiel._tasten[taste] = Taste(taste)

        Spiel._tasten[taste].gedrueckt_bearbeiter.registriere(funktion)

    @staticmethod
    def entferne_taste_gedrueckt(taste, funktion):
        """
        Entfernt eine Funktion, die ausgeführt wird, wenn die angegebene Taste gedrückt wird.

        :param taste: die Taste
        :type taste: int
        :param funktion: Die Funktion die aufgerufen wird.
        :type funktion: (bool, py2cd.Taste) -> None
        """
        if taste in Spiel._tasten:
            Spiel._tasten[taste].gedrueckt_bearbeiter.entferne(funktion)

    @classmethod
    def registriere_solange_taste_unten(cls, taste_code, funktion):
        """
        Registriert eine Funktion, die periodisch ausgeführt wird, solange die Taste gedrückt ist.

        :param taste_code: die Taste z.B. die a-Taste ist 97. Die wichtigsten Tasten sind vordefiniert, so entspricht T_a der 'a'-Taste
        :type taste_code: int
        :param funktion: Die Funktion die aufgerufen wird.
        :type funktion: () -> None
        """
        if taste_code not in Spiel._tasten:
            Spiel._tasten[taste_code] = Taste(taste_code)

        Spiel._tasten[taste_code].wenn_unten_bearbeiter.registriere(funktion)

    @staticmethod
    def registriere_maus_bewegt(funktion):
        """
        Registriert eine Funktion, die ausgeführt wird, wenn eine Maus-Taste gedrückt wird.
        Wenn die Funktion aufgerufen wird, wird ihr ein Objekt übergeben, das so aufgebaut ist:

            button: 1-3 # welche Taste: 1 = Links, ...
            pos: (x,y) # Tupel mit der Position

        :param funktion: Die Funktion die aufgerufen werden soll, wenn eine Taste gedrückt wurde
        :type funktion: (object) -> None
        """
        Spiel._mausBewegt.registriere(funktion)

    @staticmethod
    def registriere_maus_losgelassen(funktion):
        """
        Registriert eine Funktion, die aufgerufen wird, wenn eine Maustaste losgelassen wird.

        :param funktion: Die Funktion
        :type funktion: (object)->None
        """
        Spiel._maus_taste_losgelassen.registriere(funktion)

    @staticmethod
    def registriere_spiel_wird_beendet(funktion):
        """
        Registriert eine Funktion, die aufgerufen wird, wenn das Spiel beendet wird.

        :param funktion: Die Funktion
        :type funktion: (object)->None
        """
        Spiel._spiel_wird_beendet.registriere(funktion)

    @staticmethod
    def registriere_maus_gedrueckt(funktion):
        """
        Registriert eine Funktion, die aufgerufen wird, wenn eine Maustaste gedrückt wird.

        :param funktion:
        :type funktion: (object)->None
        """
        Spiel._maus_taste_gedrueckt.registriere(funktion)

    @staticmethod
    def gib_zeichen_flaeche():
        """
        Gibt die Hauptzeichenfläche des Spiels zurück. Darauf kann (muss) gezeichnet werden.

        :return: Die Zeichenfläche
        :rtype: py2cd.flaeche.ZeichenFlaeche
        """
        return Spiel.__haupt_flaeche

    @staticmethod
    def setze_aktualisierung(funktion):
        """
        Setzt die Funktion, die einmal pro Spiel Update-Durchlauf aufgerufen wird, in der Spiel-Objekte
        aktualisiert werden können.

        :param funktion: die Aktualisierungsfunktion
        :type funktion: (float) -> None
        """
        Spiel.__aktualisiere.registriere(funktion)

    @staticmethod
    def entferne_aktualisierung():
        """
        Entfernt die Aktualisierugsfuntion.
        """
        Spiel.__aktualisiere.entferne_alle()
