from py2cd.objekte import Aktualisierbar

__author__ = 'Mark Weinreuter'


class Warte(Aktualisierbar):
    def aktualisiere(self, relativer_zeitunterschied, zeit_unterschied_ms):
        if self._runterzaehl_ms <= 0:
            self.wenn_zeit_um()
            if self.wiederhole:
                self._runterzaehl_ms = self.warte_ms
            else:
                self.entferne_aktualisierung()

        self._runterzaehl_ms -= zeit_unterschied_ms

    def __init__(self, warte_ms, wenn_zeit_um, wiederhole=False):
        """
        Erstellt ein neues Warte-Objekt.

        :param warte_ms:  wie lange gewartet wird
        :type warte_ms: int
        :param wenn_zeit_um: Die Funktion die ausgeführt wird, wenn die Zeit um ist
        :type wenn_zeit_um: None -> None
        :param wiederhole: Falls die Funktion wiederholt ausgeführt werden soll
        :type wiederhole: bool
        """
        super().__init__()

        self.warte_ms = warte_ms
        self._runterzaehl_ms = warte_ms
        self.wenn_zeit_um = wenn_zeit_um
        self.wiederhole = wiederhole


def warte(warte_ms, wenn_zeit_um, wiederhole=False):
    """
    Erstellt ein neues Warte-Objekt.

    :param warte_ms:  wie lange gewartet wird
    :type warte_ms: int
    :param wenn_zeit_um: Die Funktion die ausgeführt wird, wenn die Zeit um ist
    :type wenn_zeit_um: None -> None
    :param wiederhole: Falls die Funktion wiederholt ausgeführt werden soll
    :type wiederhole: bool
    :return: das Warte Objekt
    :rtype: py2cd.zeit.Warte
    """
    return Warte(warte_ms, wenn_zeit_um, wiederhole)
