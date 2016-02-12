import pygame

from py2cd.bild import BildSpeicher
from py2cd.ereignis import EreignisBearbeiter
from py2cd.objekte import ZeichenbaresElement, SkalierbaresElement
from py2cd.spiel import Spiel

__author__ = 'Mark Weinreuter'

# Inspired by Al Sweigarts pyganim: http://inventwithpython.com/pyganim/


GESTOPPT = 0
GESTARTET = 1
PAUSIERT = 2
ZEIGE_BILD = 3
STANDART_ZEIT = 100


def generiere_namen_liste(namen_muster, von, bis):
    """
    Erstellt eine Liste von Namen. Der Name muss ein %d enthalten, dass durch die Zahlen 'von' - 'bis'
     ersetzt wird.
    :param namen_muster: das Namen Muster, z.B. bild_%d.png -> wird zu bild_[von...bis].png
    :type namen_muster: str
    :param von: Startwert
    :type von: int
    :param bis: Endwert
    :type bis: int
    :return: eine Liste mit den generierten Namen
    :rtype: list[str]
    """
    liste = []
    for i in range(von, bis):
        liste.append(namen_muster % i)

    return liste


class BildAnimation(ZeichenbaresElement, SkalierbaresElement):
    """
    Zeigt einen Animation an, indem eine Liste von Bildern(ZeichenFlaechen) in angegeben Zeitabschnitten
    durch gewechselt werden.
    """

    def __init__(self, pygame_flaechen_und_zeiten, wiederhole=False, alpha=True, anzeige_dauer=STANDART_ZEIT):
        """
        Ein neues Animationsobjekt.

        :param pygame_flaechen_und_zeiten:
        :type pygame_flaechen_und_zeiten: list[]
        :param wiederhole:
        :type wiederhole: bool
        :param alpha:
        :type alpha: bool
        :param anzeige_dauer:
        :type anzeige_dauer: float
        :return:
        :rtype:
        """

        self._wiederhole_animation = wiederhole
        """
        Gibt an ob die Animation wiederholt wird oder nicht
        """
        self._flaechen_zeiten = []
        """
        :type: list[(ZeichenFlaeche, int)]
        """
        self._zeige_letztes_bild = False

        self._bild_gewechselt = EreignisBearbeiter()
        self._animation_gestartet = EreignisBearbeiter()
        self._animation_geendet = EreignisBearbeiter()

        self._gesamt_zeit = 0
        self._aktuelle_flaeche = 0
        self._zustand = GESTOPPT
        self._vergangen = 0
        self._gesamt_zeit = 0

        # zur Ermittlung der Dimension
        breite = 0
        hoehe = 0

        # Für klone()
        self.__quelle = pygame_flaechen_und_zeiten.copy()
        self.__alpha = alpha

        for zf in pygame_flaechen_und_zeiten:

            # Entweder Tupel/Liste mit (Bild,Zeit) oder nur Bild
            if isinstance(zf, list) or isinstance(zf, tuple):
                animations_bild = zf[0]
                dauer = zf[1]
            else:
                animations_bild = zf
                dauer = anzeige_dauer

            # Die Fläche kann entweder aus einer Datei/ dem Bildspeicher geladen werden
            if isinstance(animations_bild, str):
                # Falls im Speicher, nehmen wir dieses Bild
                if BildSpeicher.ist_bild_vorhanden(animations_bild):
                    animations_bild = BildSpeicher.gib_pygame_bild(animations_bild)
                else:
                    # Ansonsten laden wir es
                    animations_bild = BildSpeicher._lade_pygbild_aus_datei(animations_bild, alpha)

            # oder schon eine pygame surface sein
            elif not isinstance(animations_bild, pygame.Surface):
                raise AttributeError("Entweder Surface oder Strings übergeben.")

            # die größten werte ermitteln
            if animations_bild.get_width() > breite:
                breite = animations_bild.get_width()
            if animations_bild.get_height() > hoehe:
                hoehe = animations_bild.get_height()



            # Zur List hinzufügen und Zeit addieren
            self._flaechen_zeiten.append((animations_bild, dauer))
            self._gesamt_zeit += dauer

        self.__rotations_flaechen = None
        self._anzahl_flaechen = len(self._flaechen_zeiten)

        SkalierbaresElement.__init__(self, self)
        ZeichenbaresElement.__init__(self, 0, 0, breite, hoehe, None)

    def start(self):
        if self._zustand == GESTOPPT or self._zustand == ZEIGE_BILD:
            self._vergangen = 0
            self._aktuelle_flaeche = 0

        self._zustand = GESTARTET
        self._animation_gestartet()

    def render(self, pyg_zeichen_flaeche, x_offset=0, y_offset=0):
        """
        Zeichnet das aktuelle Bild dieser Animation.

        :param pyg_zeichen_flaeche: die Fläche, auf der gezeichnet wird
        :type pyg_zeichen_flaeche: pygame.Surface
        """
        if self._zustand == GESTARTET:
            self._vergangen += Spiel.zeit_unterschied_ms

            naechste_flaeche = self._aktuelle_flaeche

            # solange die Zeit für das aktuelle Bild abgelaufen ist, gehe zum nächsten bild
            while self._vergangen > self._flaechen_zeiten[self._aktuelle_flaeche][1]:
                self._vergangen -= self._flaechen_zeiten[self._aktuelle_flaeche][1]

                naechste_flaeche += 1  # nächste fläche

                # alle Flächen gezeichnet?
                if naechste_flaeche == self._anzahl_flaechen:

                    if not self._wiederhole_animation:

                        if self._zeige_letztes_bild:
                            # animation anhalten
                            self.zeige_letztes_bild()

                            # damit genau dieses Bild gezeichnet wird
                            break
                        else:

                            self._animation_geendet()
                            self._zustand = GESTOPPT

            # falls die animation läuft, müssen wir die bilder wechseln
            if self._zustand == GESTARTET and self._aktuelle_flaeche != naechste_flaeche:
                # sicher gehen, das wir einen korrekten index verwenden
                self._aktuelle_flaeche = naechste_flaeche % self._anzahl_flaechen
                self._bild_gewechselt(self._aktuelle_flaeche)

        # in allen zuständen, außer gestoppt zeichnen wir
        if self._zustand != GESTOPPT:
            # das aktuelle bild wird immer noch gezeichnet
            return pyg_zeichen_flaeche.blit(self._flaechen_zeiten[self._aktuelle_flaeche][0],
                                            (self.x + x_offset, self.y + y_offset))

    def zeige_letztes_bild_wenn_geendet(self, wert=True):
        """
        Wenn die Animation geendet hat, wird das letzte Bilder der Animation als Standbild angezeigt.
        Achtung: Dies ist nur möglich, wenn die Animation nicht wiederholt wird.

        :param wert:
        :type wert: bool
        """
        if self._wiederhole_animation:
            print("Bei wiederholenden Animationen ist dies nicht nicht möglich!")

        self._zeige_letztes_bild = wert

    def zeige_bild(self, index):
        if index < 0 or index > len(self._flaechen_zeiten):
            raise ValueError("Index muss größer 0 und kleiner als die Anzahl an Bildern sein")

        self._zustand = ZEIGE_BILD
        self._aktuelle_flaeche = index

    def registriere_wenn_bild_gewechselt(self, wenn_gewechselt):
        self._bild_gewechselt.registriere(wenn_gewechselt)

    def registriere_wenn_gestartet(self, wenn_gestartet):
        self._animation_gestartet.registriere(wenn_gestartet)

    def registriere_wenn_geendet(self, wenn_geendet):
        self._animation_geendet.registriere(wenn_geendet)

    def setze_wiederhole(self, wiederhole=True):
        self._wiederhole_animation = wiederhole

    def stop(self):
        self._zustand = GESTOPPT

    def pause(self):
        self._zustand = PAUSIERT

    def _rotation_skalierung_anwenden(self):
        if self.__rotations_flaechen is None:
            # lazy init um Speicher zu sparen, falls nicht benötigt
            self.__rotations_flaechen = self._flaechen_zeiten.copy()

        index = 0
        for flaeche, zeit in self.__rotations_flaechen:
            self._flaechen_zeiten[index] = (pygame.transform.rotozoom(flaeche,
                                                                      self._winkel, self._skalierung), zeit)
            index += 1

        rect = self._flaechen_zeiten[0][0].get_rect()

        return rect.width, rect.height

    def klone(self, x, y):
        ba = BildAnimation(self.__quelle, self._wiederhole_animation, self.__alpha)
        ba.setze_position(x, y)
        return ba

    def zeige_letztes_bild(self):
        self.zeige_bild(self._anzahl_flaechen - 1)


class BildAnimationSpeicher:
    __alle_animationen = {}

    @classmethod
    def ist_animation_vorhanden(cls, schluessel):
        return schluessel in cls.__alle_animationen

    @classmethod
    def registriere_animation(cls, schluessel, bilder_und_zeiten, wiederhole=False, alpha=True):
        cls.__alle_animationen[schluessel] = (bilder_und_zeiten, wiederhole, alpha)

        return BildAnimation(*cls.__alle_animationen[schluessel])

    @classmethod
    def gib_animation(cls, schluessel):
        if schluessel not in cls.__alle_animationen:
            raise ValueError("Animation nicht im Speicher vorhanden.")

        return BildAnimation(*cls.__alle_animationen[schluessel])
