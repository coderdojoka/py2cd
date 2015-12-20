from py2cd import *
from py2cd import ROT, BBox

__author__ = 'Mark Weinreuter'

Spiel.init(400, 400, "Jump and Run")


class Figur(Bild):
    def __init__(self, x, y, bild, taste_links=T_LINKS, taste_rechts=T_RECHTS, taste_sprung=T_OBEN):
        super().__init__(x, y, bild)
        self.lauf_kraft = 3
        self.sprung_kraft = 10
        self.gravitation = .5
        self.kann_kollidieren = []
        self.spruenge = 0

        Spiel.registriere_solange_taste_unten(taste_links, lambda dt: self.bewege_links_rechts(self.lauf_kraft * -dt))
        Spiel.registriere_solange_taste_unten(taste_rechts, lambda dt: self.bewege_links_rechts(self.lauf_kraft * dt))
        Spiel.registriere_taste_gedrueckt(taste_sprung, lambda unten, pyg_ereignis: self.springen(unten))

    def aktualisiere(self, dt):
        self.y_geschwindigkeit += self.gravitation

        bewegung_y = self.y_geschwindigkeit * dt

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

    def bewege_links_rechts(self, bewegung_x):
        for block in self.kann_kollidieren:
            max_x = self.kollision_links_rechts(block, bewegung_x)
            if max_x is not None:
                # Wir haben eine Kollision gefunden => maximale Bewegung
                bewegung_x = max_x[0]
                break

        self.aendere_position(bewegung_x, 0)


# Bild laden in den Speicher laden und unter dem Schlüssel "scratch" ablegen
BildSpeicher.lade_bild("wobbel", "testimages/wobbel.png")

boden = Rechteck(0, 0, Spiel.breite, 20, ROT)
boden.unten = 20

boden2 = Rechteck(300, 300, 40, 20, ROT)
boden3 = Rechteck(350, 100, 40, 20, ROT)
boden4 = Rechteck(270, 200, 40, 20, ROT)

bloecke = [boden, boden2, boden3, boden4]

figur1 = Figur(10, 10, "wobbel")
figur1.kann_kollidieren = bloecke
figur2 = Figur(310, 10, "wobbel", taste_links=T_a, taste_rechts=T_d, taste_sprung=T_w)
figur2.kann_kollidieren = bloecke


def aktualisiere(dt):
    figur1.aktualisiere(dt)
    figur2.aktualisiere(dt)


# Das Spiel starten
Spiel.setze_aktualisierung(aktualisiere)
Spiel.starten()
