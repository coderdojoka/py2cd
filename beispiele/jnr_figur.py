from py2cd import Bild, BildSpeicher

__author__ = 'Mark Weinreuter'


class JnRFigur(Bild):
    FALL_GESCHWINDIGKEIT = 5
    GESCHWINDIGKEIT = 5
    LINKS = -1
    RECHTS = 1

    def __init__(self, bild_name, x, y, bild_namen):
        super().__init__(x, y, BildSpeicher.gib_bild(bild_namen))
        self.sprung_geschwindigkeit = JnRFigur.GESCHWINDIGKEIT
        self.richtung = JnRFigur.LINKS
        self.geschwindigkeit = JnRFigur.GESCHWINDIGKEIT
        self.__bewegung_x = 0
        self.__bewegung_y = 0
        self.fall_geschwindigkeit = JnRFigur.FALL_GESCHWINDIGKEIT
        self.sprung_dauer_ms = 1000
        self.sprung_ms = 0
        self.faellt = False
        self.springt = False

    def laufen(self, richtung=None):
        if richtung is not None:
            self.richtung = richtung
        self.__bewegung_x = self.geschwindigkeit * self.richtung

    def springen(self):
        if not self.hat_boden():
            print("Müssen stehen zum springen")

        if self.springt:
            print("Springen bereits")
            return

        self.sprung_ms = 0
        self.springt = True

    def aktualisiere(self, delta, vergangene_ms):

        # überprüfen ob wir auf festem boden stehen oder fallen
        if self.hat_boden():
            print("Fällt nicht")
            if self.faellt:
                self.faellt = False
        else:
            print("Fällt")
            self.__bewegung_y += self.fall_geschwindigkeit

        if self.springt:
            self.__bewegung_y -= self.sprung_geschwindigkeit

            self.sprung_ms += vergangene_ms
            if self.sprung_ms > self.sprung_dauer_ms:
                print("Sprung ende")
                self.springt = False

        # Position aktualisieren
        self.aendere_position(self.__bewegung_x * delta, self.__bewegung_y * delta)
        self.__bewegung_x = 0
        self.__bewegung_y = 0

    def hat_boden(self):
        raise NotImplementedError("Methode muss überschrieben werden!")