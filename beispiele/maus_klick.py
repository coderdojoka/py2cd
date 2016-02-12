from py2cd import *
from py2cd.farben import *
import random

# Der erste Schritt, um ein Spiel zu starten ist immer init() aufzurufen
Spiel.init(640, 480, "Mein Spiel")
# Erstellt ein neues Fenster mit der gegebenen Größe von 640x480 und dem Titel "Mein Spiel"


# Ein Quadrat an der Position 300x200
haus = Rechteck(300, 200, 100, 100, GELB)

# Ein Dreieck zeichenn, in dem alle Eckpunte angegeben werden
dreieck = Polygon([(300, 200), (350, 160), (400, 200)], ROT)

# Ein weiteres Quadrat
box = Rechteck(100, 100, 50, 50, GRUEN)

# Wird aufgerufen, immer wenn die Maus bewegt wird
def maus_bewegt(pyg_event):
    maus_position = pyg_event.pos
    print(maus_position)

# Wird aufgerufen, immer wenn die Maus gedrueckt (geklickt) wird
def maus_gedrueckt(pyg_event):
    maus_position = pyg_event.pos

    if box.punkt_in_rechteck(maus_position):
        box.farbe = (random.randint(0,255),random.randint(0,255),random.randint(0,255))

    if dreieck.punkt_in_rechteck(maus_position):
        dreieck.setze_position (random.randint(10, 500), random.randint(10, 455))

    if haus.punkt_in_rechteck(maus_position):
        haus.setze_position(random.randint(10, 500), random.randint(10, 455))


# Bindet die Funktion 'maus_gedrueckt' an das maus_gedrueckt-Ereignis
Spiel.registriere_maus_gedrueckt(maus_gedrueckt)
# Bindet die Funktion 'maus_bewegt' an das maus_bewegt-Ereignis
Spiel.registriere_maus_bewegt(maus_bewegt)

# Hilfsgitter einblenden
Spiel.zeichne_gitter()

# Um das Spiel zu starten, muss Spiel.start() aufgerufen werden. Dies sollte immer die letzte Anweisung sein.
Spiel.starten()
