__author__ = 'Mark Weinreuter'

from py2cd import *
from py2cd.farben import *

links_down = False
rechts_down = False
oben_down = False
unten_down = False
speed = 3.1
ball_x = speed - 1
ball_y = speed


def aktualisiere(dt):
    global ball_x, ball_y

    # Überprüfen ob der Ball die Kanten berührt
    if ball.beruehrt_linken_oder_rechten_rand():
        ball_x *= -1

    if ball.beruehrt_oberen_oder_unteren_rand():
        ball_y *= -1

    # Ball bewegen
    ball.aendere_position(ball_x * dt, ball_y * dt)

    # Kollision der zwei Rechtecke überprüfen
    beruehrt = rechteck.beruehrt_objekt(kollision)
    if beruehrt:
        kollision.farbe = ROT
    else:
        kollision.farbe = GELB


# Diese Funktionen werden aufgerufen, wenn die entsprechende Taste gedrückt wird
def links(dt):
    rechteck.aendere_position(-speed * dt, 0)


def rechts(dt):
    rechteck.aendere_position(speed * dt, 0)


def oben(dt):
    rechteck.aendere_position(0, -speed * dt)


def unten(dt):
    rechteck.aendere_position(0, speed * dt)


# Initialisiert das Fenster
Spiel.init(400, 400, "Steuere das Rechteck!", aktualisiere)

# Zwei Rechtecke erstellen
rechteck = Rechteck(40, 160, 40, 40, BLAU)
kollision = Rechteck(50, 40, 60, 40, ROT)

# Einen Text anzeigen
schrift = Schrift(20)
t = Text("Pfeiltasten zum bewegen", 0, 10, schrift, GRAU)

# 5 Pixel vom rechten Rand plazieren
t.rechts = 5

# Bild laden in den Speicher laden und unter dem Schlüssel "scratch" ablegen
BildSpeicher.lade_bild("scratch", "testimages/scratch.png")
# Bild aus dem Speicher über seinen Schlüssel holen
ball = BildSpeicher.gib_bild("scratch", 10, 10)

# Tastendrücke-Funktionen registrien. Wird die Taste K_a = 'a' gedrückt, so wird die
# Funktion mit dem Namen links aufgerufen
Spiel.registriere_solange_taste_unten(T_LINKS, links)
Spiel.registriere_solange_taste_unten(T_RECHTS, rechts)
Spiel.registriere_solange_taste_unten(T_UNTEN, unten)
Spiel.registriere_solange_taste_unten(T_OBEN, oben)

# Das Spiel starten
Spiel.starten()
