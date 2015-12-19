from py2cd import *
from py2cd import ROT, BBox

__author__ = 'Mark Weinreuter'

# Initialisiert das Fenster
Spiel.init(400, 400, "Jump and Run")


class Figur(Bild):
    def __init__(self, x, y, bild):
        super().__init__(x, y, bild)
        self.lauf_kraft = 3
        self.sprung_kraft = 10
        self.gravitation = .5
        self.kann_kollidieren = []
        self.spruenge = 0

        self.registriere_tasten(T_LINKS, T_RECHTS, T_OBEN)

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

    def registriere_tasten(self, taste_links, taste_rechts, taste_sprung):
        Spiel.registriere_solange_taste_unten(taste_links, lambda dt: self.bewege_links_rechts(self.lauf_kraft * -dt))
        Spiel.registriere_solange_taste_unten(taste_rechts, lambda dt: self.bewege_links_rechts(self.lauf_kraft * dt))
        Spiel.registriere_taste_gedrueckt(taste_sprung, lambda unten, pyg_ereignis: self.springen(unten))

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
BildSpeicher.lade_bild("scratch", "testimages/wobbel.png")
# Bild aus dem Speicher über seinen Schlüssel holen
figur = Figur(10, 10, "scratch")

boden = Rechteck(0, 0, Spiel.breite, 20, ROT)
boden.unten = 20

boden2 = Rechteck(300, 300, 40, 20, ROT)
boden3 = Rechteck(350, 100, 40, 20, ROT)
boden4 = Rechteck(270, 200, 40, 20, ROT)

bloecke = [boden, boden2, boden3, boden4]
figur.kann_kollidieren = bloecke


def aktualisiere(dt):
    figur.aktualisiere(dt)


# Das Spiel starten
Spiel.setze_aktualisierung(aktualisiere)
Spiel.starten()
