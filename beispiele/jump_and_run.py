from py2cd import *
from py2cd import ROT, BBox

__author__ = 'Mark Weinreuter'

Spiel.init(400, 400, "Jump and Run")


class Figur(Bild, Aktualisierbar):
    def __init__(self, x, y, bild, taste_links=T_LINKS, taste_rechts=T_RECHTS, taste_sprung=T_OBEN):
        Bild.__init__(self, x, y, bild)
        Aktualisierbar.__init__(self)
        self.lauf_kraft = 3
        self.sprung_kraft = 10
        self.gravitation = .5
        self.kann_kollidieren = []
        self.spruenge = 0

        Spiel.registriere_solange_taste_unten(taste_links, lambda dt: self.bewege_links_rechts(self.lauf_kraft * -dt))
        Spiel.registriere_solange_taste_unten(taste_rechts, lambda dt: self.bewege_links_rechts(self.lauf_kraft * dt))
        Spiel.registriere_taste_gedrueckt(taste_sprung, lambda unten, pyg_ereignis: self.springen(unten))

    def aktualisiere(self, rdt, zeit_unterschied_ms):
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

                print(max_y[1])
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

verschiebung = 0


def aktualisiere(dt):
    # damit die einzelnen Objekte nicht unterschiedlich schnell verschoben werden
    global verschiebung
    verschiebung -= 1 * dt
    tmp = int(verschiebung) # nur ganze pixel könen verschboen werden
    verschiebung -= tmp
    for block in bloecke:
        block.aendere_position(tmp, 0)


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


def wenn():
    print("zeit um")
    b = Rechteck(350, 100, 40, 20, ROT)
    bloecke.append(b)


w = Warte(2400, wenn, True)

for i in range(0, 0):
    b = Rechteck(350 + i * 75, 100, 40, 20, ROT)
    bloecke.append(b)

Spiel.fps = 30

# Das Spiel starten
Spiel.setze_aktualisierung(aktualisiere)
Spiel.starten()
