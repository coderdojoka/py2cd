from py2cd import *
from py2cd.erweiterungen.jnr.level import BewegtesLevelElement

__author__ = 'Mark Weinreuter'


class Figur(BildWechsler):
    def __init__(self, x, y, bilder_namen_liste, taste_links=T_LINKS, taste_rechts=T_RECHTS, taste_sprung=T_OBEN):
        super().__init__(x, y, bilder_namen_liste)

        self.max_y_geschwindigkeit = 15
        self.lauf_kraft = 3
        self.sprung_kraft = 12
        self.gravitation = .75
        self.spruenge = 0
        self.auf_boden = False
        self.steht_auf = None
        """
        :type: py2cd.bbox.BBox
        """

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

    def figur_aktualisiere(self, kann_kollidieren, rdt):

        self.y_geschwindigkeit += self.gravitation

        if isinstance(self.steht_auf, BewegtesLevelElement):
            self.x_geschwindigkeit += self.steht_auf.x_geschwindigkeit
            self.y_geschwindigkeit += self.steht_auf.y_geschwindigkeit

        pos_x = self.x + self.x_geschwindigkeit * rdt
        pos_y = self.y + self.y_geschwindigkeit * rdt

        # in dubio contra reo
        tmp_steht_auf = self.steht_auf
        self.auf_boden = False
        self.steht_auf = None

        for ele in kann_kollidieren:
            block = ele.objekt
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
                    ele.figur_steht_drauf(self)
                    self.steht_auf = ele

                elif self.y_geschwindigkeit < 0:
                    pos_y = block.y + block.hoehe

                # Sprung/Fall abbrechen
                self.y_geschwindigkeit = 0

        # Zurücksetzen
        if tmp_steht_auf != self.steht_auf:
            if tmp_steht_auf is not None:
                tmp_steht_auf.figur_steht_nicht_drauf(self)

        self.x_geschwindigkeit = 0
        self.setze_position(pos_x, pos_y)

    def springen(self, unten):
        if unten and self.spruenge < 2:
            self.spruenge += 1
            self.y_geschwindigkeit -= self.sprung_kraft
            self.y_geschwindigkeit = min(self.max_y_geschwindigkeit, max(self.y_geschwindigkeit, -self.max_y_geschwindigkeit))
