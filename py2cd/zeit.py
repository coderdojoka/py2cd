from py2cd.objekte import Aktualisierbar

__author__ = 'Mark Weinreuter'


class Warte(Aktualisierbar):
    def aktualisiere(self, relative_dt, zeit_unterschied_ms):
        if self._runterzaehl_ms <= 0:
            self.wenn_zeit_um()
            if self.wiederhole:
                self._runterzaehl_ms = self.warte_ms
            else:
                self.entferne_aktualisierung()

        self._runterzaehl_ms -= zeit_unterschied_ms

    def __init__(self, warte_ms, wenn_zeit_um, wiederhole=False):
        super().__init__()

        self.warte_ms = warte_ms
        self._runterzaehl_ms = warte_ms
        self.wenn_zeit_um = wenn_zeit_um
        self.wiederhole = wiederhole
