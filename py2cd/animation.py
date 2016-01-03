import math

from py2cd import Linie
from py2cd import Spiel, Aktualisierbar

__author__ = 'Mark Weinreuter'

GESTOPPT = 0
GESTARTET = 1
PAUSIERT = 2


class Animation(Aktualisierbar):
    """
    Eine Animation, die für eine gegebene Zeit abgearbeitet wird.
    """

    def __init__(self, zeit_in_ms, aktualisiere=lambda dt: None, animation_gestartet=lambda wiederholung: None,
                 animation_geendet=lambda: None,
                 animation_gestoppt=lambda: None, animation_pausiert=lambda: None, wiederhole=False):
        """
        Ein neues Animationsobjekt.

        :param zeit_in_ms: Die Zeit in Millisekunden (1000 * Sekunde), bis sich die Animation wiederholt.
        :type zeit_in_ms: int
        :param aktualisiere: Die Funktion wird aufgerufen, wenn die Animation aktualisiert wird. Sie hat einen Parameter, der den Fortschritt anzeigt.
         Dieser Parameter ist im Bereich [0, 1]
        :type aktualisiere: (flaot) -> None
        :param animation_gestartet:
        :type animation_gestartet:
        :param animation_gestoppt:
        :type animation_gestoppt:
        :param animation_pausiert:
        :type animation_pausiert:
        :param wiederhole:
        :type wiederhole:
        """
        super().__init__()
        self._wiederhole_animation = wiederhole
        """
        Gibt an ob die Animation wiederholt wird oder nicht
        """
        self._aktualisiere_animation = aktualisiere
        self._animation_gestartet = animation_gestartet
        self._animation_geendet = animation_geendet
        self._animation_gestoppt = animation_gestoppt
        self._animation_pausiert = animation_pausiert

        self._gesamt_zeit_ms = zeit_in_ms
        self._zustand = GESTOPPT
        self._vergangene_zeit_ms = 0

    def setze_animation_gestoppt(self, animation_gestoppt):
        self._animation_gestoppt = animation_gestoppt

    def setze_animation_geendet(self, animation_geendet):
        self._animation_geendet = animation_geendet

    def setze_animation_gestartet(self, animation_gestartet):
        self._animation_gestartet = animation_gestartet

    def setze_wiederhole(self, wiederhole=True):
        self._wiederhole_animation = wiederhole

    def aktualisiere(self, dt, zeit_unterschied_ms):
        """
        Aktualisiert die Animation und überprüft, ob die Zeit abgelaufen ist.

        :return: Gibt True zurück, wenn die Animationszeit abgelaufen ist
        :rtype: bool
        """

        # Wir tun nur etwas, wenn wir aktiv sind
        if self._zustand != GESTARTET:
            return

        self._vergangene_zeit_ms += zeit_unterschied_ms
        # Ist die Zeit um?
        if self._vergangene_zeit_ms >= self._gesamt_zeit_ms:

            # Wir haben die Animation komplett durchlaufen
            self._aktualisiere_animation(1)
            self._animation_geendet()

            if self._wiederhole_animation:
                self._vergangene_zeit_ms = 0
                self._start(True)

            return True
        else:
            self._aktualisiere_animation(self._vergangene_zeit_ms / self._gesamt_zeit_ms)

        return False

    def start(self):
        if self._zustand == GESTOPPT:
            self._vergangene_zeit_ms = 0

        self._start()

    def stop(self):
        self._zustand = GESTOPPT
        self._animation_gestoppt()

    def pause(self):
        self._zustand = PAUSIERT
        self._animation_pausiert()

    def _start(self, wiederholung=False):
        self._zustand = GESTARTET

        # Extra Funktion, die beim Starten aufgerufen wird, um in aktualisiere nicht auf 0 testen zu müssen
        self._animation_gestartet(wiederholung)

        # Wir sind ganz am Anfang der Animation
        self._aktualisiere_animation(0)


class Warte(Animation):
    def __init__(self, warte_ms, wenn_zeit_um, wiederhole=False, sofort_starten=True):
        super().__init__(warte_ms, animation_geendet=wenn_zeit_um, wiederhole=wiederhole)

        if sofort_starten:
            self.start()


class AnimationenKette(Animation):
    def __init__(self, liste_animationen):
        """

        :param liste_animationen:
        :type liste_animationen: list[Animation]
        """

        if len(liste_animationen) == 0:
            raise AttributeError("Animationsliste darf nicht leer sein.")

        self._animationen = []
        """
        :type: list[Animation]
        """

        gesamt_zeit = 0
        self.anzahl_animationen = len(liste_animationen)

        for anim in liste_animationen:
            self._animationen.append(anim)

            # Gesamtzeit mitzählen
            gesamt_zeit += anim._gesamt_zeit_ms

        self._aktueller_index = 0
        self._aktuelle_animation = self._animationen[self._aktueller_index]
        """
        Die aktuelle Animation

        :type: Animation
        """

        # Ein bisschen Spielraum für ungenaues Timing
        gesamt_zeit += self.anzahl_animationen * 2000 / Spiel.fps
        super().__init__(gesamt_zeit, aktualisiere=self._aktualisiere, animation_gestartet=self._gestartet)

    def _gestartet(self, wdh=False):
        self._aktuelle_animation.start()

    def _eine_animation_gestoppt(self):
        # print("Animation %d gestoppt." % self._aktueller_index)
        self._aktueller_index += 1

        # Alle Animationen abgearbeitet
        if self._aktueller_index == self.anzahl_animationen:
            self.stop()
        else:
            self._aktuelle_animation = self._animationen[self._aktueller_index]
            self._aktuelle_animation.start()

    def _aktualisiere(self, delta):
        if self._aktuelle_animation.aktualisiere(delta, Spiel.zeit_unterschied_ms):
            self._eine_animation_gestoppt()


class AnimierteLinie(Animation):
    def __init__(self, start, ende, zeit_in_ms=None, geschwindigkeit=None, farbe=(0, 0, 0), dicke=1):

        if zeit_in_ms is None and geschwindigkeit is None:
            raise AttributeError("Entweder die Zeit oder die Geschwindigkeit müssen gesetzt sein.")

        self.linie = Linie(start, start, farbe=farbe, dicke=dicke)
        self.linie.verstecke()
        self.x_start = start[0]
        self.x_diff = ende[0] - start[0]
        self.y_start = start[1]
        self.y_diff = ende[1] - start[1]

        # Zeit berechnen
        if geschwindigkeit is not None:
            l = math.sqrt((ende[0] - start[0]) ** 2 + (ende[1] - start[1]) ** 2)

            zeit_in_ms = l / geschwindigkeit

        super().__init__(zeit_in_ms, aktualisiere=self._aktualisiere, animation_gestartet=self._gestartet)

    def _gestartet(self, wdh=False):
        self.linie.zeige()

    def _aktualisiere(self, dt):
        self.linie.setze_ende((self.x_start + self.x_diff * dt, self.y_start + self.y_diff * dt))
