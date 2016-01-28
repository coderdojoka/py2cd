from py2cd import *

__author__ = 'Mark Weinreuter'


class Figur(Bild):
    def __init__(self, x, y, bild, taste_links=T_LINKS, taste_rechts=T_RECHTS, taste_sprung=T_OBEN):
        Bild.__init__(self, x, y, bild)
        self.max_y_geschwindigkeit = 15
        self.lauf_kraft = 3
        self.sprung_kraft = 12
        self.gravitation = .75
        self.kann_kollidieren = []
        self.spruenge = 0
        self.auf_boden = False

        if taste_links is not None:
            Spiel.registriere_solange_taste_unten(taste_links, self.solange_links)

        if taste_rechts is not None:
            Spiel.registriere_solange_taste_unten(taste_rechts, self.solange_rechts)

        if taste_sprung is not None:
            Spiel.registriere_taste_gedrueckt(taste_sprung, lambda unten, pyg_ereignis: self.springen(unten))

    def solange_links(self, dt):
        self.x_geschwindigkeit = -self.lauf_kraft

    def solange_rechts(self, dt):
        self.x_geschwindigkeit = self.lauf_kraft

    def figur_aktualisiere(self, rdt):

        self.y_geschwindigkeit += self.gravitation
        # in dubio contra reo
        self.auf_boden = False

        pos_x = self.x + self.x_geschwindigkeit * rdt
        pos_y = self.y + self.y_geschwindigkeit * rdt

        for block in self.kann_kollidieren:
            hat_kollision_x = block.beruehrt_rechteck(pos_x, self.y, self.breite, self.hoehe)

            if hat_kollision_x:
                if self.x_geschwindigkeit > 0:
                    pos_x = block.x - self.breite
                elif self.x_geschwindigkeit < 0:
                    pos_x = block.x + block.breite

            hat_kollision_y = block.beruehrt_rechteck(self.x, pos_y, self.breite, self.hoehe)
            if hat_kollision_y:
                if self.y_geschwindigkeit > 0:
                    pos_y = block.y - self.hoehe

                    # Können wiederspringen und sind auf dem Boden
                    self.spruenge = 0
                    self.auf_boden = True

                elif self.y_geschwindigkeit < 0:
                    pos_y = block.y + block.hoehe

                # Sprung/Fall abbrechen
                self.y_geschwindigkeit = 0

        # Zurücksetzen
        self.x_geschwindigkeit = 0

        self.setze_position(pos_x, pos_y)

    def springen(self, unten):
        if unten and self.spruenge < 2:
            self.spruenge += 1
            self.y_geschwindigkeit -= self.sprung_kraft
            self.y_geschwindigkeit = min(self.max_y_geschwindigkeit, max(self.y_geschwindigkeit, -self.max_y_geschwindigkeit))
