__author__ = 'norbert'
from pygame.constants import *

from py2cd import *
from py2cd.farben import *


# from py2cd import *
# from py2cd.farben import *
# from pygame.constants import *



def tasten_druck(unten, e):
    if unten:
        neuer_buchstabe(e.unicode)


# Zähler falscher stellen
falsch = 0


def neuer_buchstabe(letter):
    global falsch, alle_buchstaben

    print(len(alle_buchstaben))

    letter = letter.capitalize()
    i = -1
    a = len(wort)
    # print("A: ", a)
    for element in wort:
        i = i + 1
        if element == letter:
            a = a + 10
            alle_buchstaben = alle_buchstaben[:i] + letter + alle_buchstaben[i + 1:]
        a = a - 1
        if a == 0:
            falsch = falsch + 1
            # Bei fehler neues stück anzeigen
            mydict[falsch].zeige()

    print(alle_buchstaben)
    if alle_buchstaben == wort:
        print("\ngewonnen")

    print(alle_buchstaben)


liste = []


def signwork(ele):
    liste.append(ele)
    ele.verstecke()


wort = "BUND"
alle_buchstaben = '_' * len(wort)

Spiel.init(640, 480, "hangman")

schrift = Schrift(30, "Arial")
text = Text("Hallo", 20, 50, schrift)
text.setze_text("Test")

# Hilfsgitter anzeigen
sideleft = Linie((350, 350), (350, 450), BRAUN, 6)
signwork(sideleft)
sideright = Linie((600, 350), (600, 450), BRAUN, 6)
signwork(sideright)
line = Linie((350, 350), (600, 350), BRAUN, 6)
signwork(line)
gallowhigh = Linie((550, 350), (550, 100), BRAUN, 6)
signwork(gallowhigh)
gallowhoriz = Linie((425, 100), (550, 100), BRAUN, 6)
signwork(gallowhoriz)
gallowdiag = Linie((550, 150), (500, 100), BRAUN, 6)
signwork(gallowdiag)
rope = Linie((425, 100), (425, 125), GELB, 4)
signwork(rope)
head = Kreis(408, 125, 20, HELL_GRAU)
signwork(head)
eyel = Kreis(414, 138, 5, WEISS)
signwork(eyel)
eyel1 = Kreis(418, 142, 3, SCHWARZ)
signwork(eyel1)
eyer = eyel.klone(432, 138)
signwork(eyer)
eyer1 = eyel1.klone(436, 142)
signwork(eyer1)
nose = Kreis(422, 150, 2)
signwork(nose)
nose1 = Kreis(430, 150, 2)
signwork(nose1)
tongue = Kreis(425, 155, 5, ROT)
signwork(tongue)
tongue1 = tongue.klone(428, 157)
signwork(tongue1)
body = Linie((425, 165), (425, 230), SCHWARZ, 6)
signwork(body)
armleft = Linie((425, 170), (400, 190), SCHWARZ, 6)
signwork(armleft)
armright = Linie((425, 170), (450, 190), SCHWARZ, 6)
signwork(armright)
legleft = Linie((425, 230), (400, 270), SCHWARZ, 6)
signwork(legleft)
legright = Linie((425, 230), (450, 270), SCHWARZ, 6)
signwork(legright)

mydict = {1: sideleft, 2: sideright}

for i in range(K_a, K_z):
    Spiel.registriere_taste_gedrueckt(i, tasten_druck)

Spiel.zeichne_gitter()
Spiel.starten()
