from py2cd import *

__author__ = 'Mark Weinreuter'


class Figur(Bild):
    def __init__(self, x, y, bild, taste_links=T_LINKS, taste_rechts=T_RECHTS, taste_sprung=T_OBEN):
        Bild.__init__(self, x, y, bild)
        self.max_y_geschwindigkeit = 12.5
        self.lauf_kraft = 3
        self.sprung_kraft = 10
        self.gravitation = .5
        self.kann_kollidieren = []
        self.spruenge = 0

        if taste_links is not None:
            Spiel.registriere_solange_taste_unten(taste_links, lambda dt: self.bewege_links_rechts(self.lauf_kraft * -dt))

        if taste_rechts is not None:
            Spiel.registriere_solange_taste_unten(taste_rechts, lambda dt: self.bewege_links_rechts(self.lauf_kraft * dt))

        if taste_sprung is not None:
            Spiel.registriere_taste_gedrueckt(taste_sprung, lambda unten, pyg_ereignis: self.springen(unten))

    def figur_aktualisiere(self, rdt):
        self.y_geschwindigkeit += self.gravitation

        bewegung_y = self.y_geschwindigkeit * rdt

        for block in self.kann_kollidieren:
            max_y = self.kollision_oben_unten(block, bewegung_y)
            if max_y is not None:
                self.y_geschwindigkeit = 0
                # Wir haben eine Kollision gefunden => maximale Bewegung
                bewegung_y = max_y[0]
                if max_y[1] == BBox.UNTEN:
                    self.spruenge = 0

                break

        self.aendere_position(0, bewegung_y)

    def springen(self, unten):
        if unten and self.spruenge < 2:
            self.spruenge += 1
            self.y_geschwindigkeit -= self.sprung_kraft
            self.y_geschwindigkeit = min(self.max_y_geschwindigkeit, max(self.y_geschwindigkeit, -self.max_y_geschwindigkeit))

    def bewege_links_rechts(self, bewegung_x):
        for block in self.kann_kollidieren:
            max_x = self.kollision_links_rechts(block, bewegung_x)
            if max_x is not None:
                # Wir haben eine Kollision gefunden => maximale Bewegung
                bewegung_x = max_x[0]
                break

        self.aendere_position(bewegung_x, 0)
