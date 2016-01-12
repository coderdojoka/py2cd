from datetime import datetime
from random import randint

from py2cd import *
from py2cd.farben import *



# CODE UM TUERCHEN ZU ERSTELLEN UND AUF MAUS EREIGNISE ZU REAGIEREN

# Eine Klasse ist eine Art Container für Variablen. Wenn man viel gleiche Dinge benötigt
# erstellt man sich eine Klasse. Eine Klasse ist eine Art Vorlage mit definierten Variablen und Funktionen.
# So hat ein Tuerchen immer einen Text, einen Rahmen und eine Variable für den Tag, den
# das Türchen darstellt.
class Tuerchen(ZeichenFlaeche):
    def __init__(self, tag, x, y, aktion, schriftart, breite=40, hoehe=40, aktiv_farbe=MATT_GRUEN, inaktiv_farbe=GRAU_GRUEN):
        super().__init__(x, y, (breite, hoehe), aktiv_farbe)

        self.tag = tag
        self.aktion = aktion
        self.ist_aktiv = True
        self.aktiv_farbe = aktiv_farbe
        self.inaktiv_farbe = inaktiv_farbe

        # Wir müssen eine neue Zeichenfläche von Hand zum Spiel hinzufügen
        Spiel.gib_zeichen_flaeche().fuege_hinzu(self)

        # Der Text soll auf unseren neuen Fläche gezeichnet werden => eltern_flaeche setzen
        self.text = Text(str(tag), 0, 0, schriftart, SCHWARZ, eltern_flaeche=self)
        self.text.zentriere()  # in unseren neuen fläche zentrieren. NICHT im ganzen Fenster, da Elternfläche angegeben wurde

        # Ein Rahmen um unsere Fläche zeichnen
        self.rahmen = Rechteck(0, 0, breite - 1, hoehe - 1, SCHWARZ, dicke=2, eltern_flaeche=self)

    def maus_geklickt(self):
        # Nur aktive Türchen können geklickt werden
        if self.ist_aktiv:
            self.aktion(self.tag)

    def maus_betritt(self):
        if self.ist_aktiv:
            self.rahmen.farbe = ORANGE
            self.text.farbe = HELL_GRAU

    def maus_verlassen(self):
        if self.ist_aktiv:
            self.rahmen.farbe = GRAU
            self.text.farbe = SCHWARZ

    def deaktiviere(self):
        # Farbe des Türchen und Rahmen ändern, Tür deaktiveren
        self.ist_aktiv = False
        self.farbe = self.inaktiv_farbe
        self.rahmen.farbe = HELL_GRAU


# Findet die Tür, auf die geklickt wird
# Geht die Liste und überprüft, ob die Mausposition mit einer Tür übereinstimmt
def finde_tuerchen(ereignis):
    for tuer in tuerchen:
        if tuer.punkt_in_rechteck(ereignis.pos):
            return tuer


# Falls eine Tür angeklickt wird
def maus_geklickt(ereignis):
    tuer = finde_tuerchen(ereignis)

    if tuer is not None:
        tuer.maus_geklickt()


# Hier wird die lezte Tür gespeichert, über die sich die Maus bewegt hat
# Dies ist nötig, da wir den Rahmen der Tür einfarben, wenn die Maus darüber fährt
letze_tuer = None


# Falls die Maus sich über eine Tür bewegt
def maus_bewegt(ereignis):
    global letze_tuer

    tuer = finde_tuerchen(ereignis)
    if letze_tuer is not None:
        letze_tuer.maus_verlassen()

    letze_tuer = tuer
    if tuer is not None:
        tuer.maus_betritt()


# ENDE TÜRCHEN CODE



# AKTUALISIERUNGS-FUNKTION

faktor = 0.01
skalierung = 1

# Diese Funktion wird aufgerufen, wenn das Spiel aktualisiert wird
def aktualisiere(delta):
    global faktor, skalierung

    if skalierung >= 1.15:  # maximal 1.15 mal so groß
        faktor *= -1  # wieder kleiner werden
    elif skalierung <= .85:  # minimal 0.85 mal so klein
        faktor *= -1  # wieder größer werden

    # Stern skalieren
    skalierung += faktor * delta
    stern.setze_skalierung(skalierung) # Neues Feature, dass ich eingebaut habe



# SPIEL CODE


# Der erste Schritt, um ein Spiel zu starten ist immer init() aufzurufen
# Erstellt ein neues Fenster mit der gegebenen Größe von 640x480 und dem Titel "Mein Spiel"
Spiel.init(800, 900, "Advent Advent...")

# Funktion die aufgerufen wird, wenn das Spiel aktualisiert wird (ca 30 mal pro Sekunde)
Spiel.setze_aktualisierung(aktualisiere)

Spiel.registriere_maus_gedrueckt(maus_geklickt)
Spiel.registriere_maus_bewegt(maus_bewegt)

# AB HIER WIRD GEZEICHNET


# Hintergrund: oben blau, unten gruen
HINTERGRUND_BLAU = (50, 50, 255)
blauHintergrund = Rechteck(0, 0, 800, 500, HINTERGRUND_BLAU)
gruenHintergrund = Rechteck(0, 500, 800, 900, HELL_GRUEN)

# NR6(KERZE)
Rechteck(200, 300, 20, 100, WEISS)
Linie((210, 300), (210, 285))
Oval(201, 265, 9, 13, GELB)

# NR13(KERZE)
Rechteck(100, 600, 20, 100, WEISS)
Linie((110, 600), (110, 585))
Oval(101, 565, 9, 11, GELB)

# NR8(KUGEL)
Linie((605, 475), (605, 520))
Kreis(580, 510, 25, ROT)

# NR2(KUGEL)
Linie((205, 475), (205, 520))
Kreis(180, 510, 25, ROT)

# 20
Rechteck(640, 560, 20, 80, WEISS)
Linie((651, 545), (651, 560))
Oval(640, 523, 10, 11, GELB)

# WEINATSBAUM <- gutes Deutsch :D
# Alter Baum
# Polygon([(0, 800), (325, 475), (100, 475), (350, 225), (200, 225), (380, 50),
#           (550, 225), (410, 225), (650, 475), (425, 475), (750, 800), (400, 800)], GRUEN)
# Rechteck(325, 800, 125, 100, BRAUN)

# Ich hab den Baum aus 3 Dreiecken gezeichnet
# x=0, wir zentrieren später
baum_oben = Dreieck(0, 80, 300, 150, MATT_GRUEN)
baum_mitte = Dreieck(0, 80 + 90, 550, 320, MATT_GRUEN)
baum_unten = Dreieck(0, 80 + 90 + 200, 700, 360, MATT_GRUEN)
stamm = Rechteck(0, baum_unten.oben + baum_unten.hoehe, 120, 100, BRAUN)
baum_oben.zentriere_horizontal()
baum_mitte.zentriere_horizontal()
baum_unten.zentriere_horizontal()
stamm.zentriere_horizontal()

# NR23(STERN)
# Alter Stern
# Polygon([(380, 0), (430, 150), (300, 60), (460, 60), (330, 150)], (210, 183, 34))

# spitze bei 0,0. wir setzen die Position später
# wenn der stern gefüllt sein soll, müssen alle eckpunkte angegeben werden
stern = Polygon([(0, 0), (20, 60), (80, 60), (30, 90), (50, 150), (0, 110),
                 # ab hier alle Punkte gespiegelt
                 (-50, 150), (-30, 90), (-80, 60), (-20, 60)], MATT_GOLD)
stern.zentriere_horizontal()

# 10
Linie((525, 225), (525, 270))
Kreis(500, 270, 25, ROT)

# NR5
Rechteck(600, 700, 100, 150, ROT)
Oval(470, 800, 115, 50, ROT)
Bogen(600, 780, 50, 20, 180, 360, SCHWARZ)
Oval(600, 680, 50, 20, (165, 42, 42))

# Geschenk NR24
Rechteck(100, 800, 100, 100, ROT)
Polygon([(200, 700), (300, 700), (200, 800), (100, 800)], (19, 172, 19))
Polygon([(300, 700), (300, 800), (200, 900), (200, 800)], GELB)
Linie((100, 800), (200, 800))
Rechteck(100, 838, 100, 24, BLAU)
Rechteck(138, 800, 24, 100, BLAU)
Polygon([(238, 700), (262, 700), (162, 800), (138, 800)], BLAU)
Polygon([(300, 738), (300, 762), (200, 862), (200, 838)], BLAU)

#
Rechteck(0, 200, 180, 10, BRAUN)
Rechteck(0, 140, 10, 60, BRAUN)
Rechteck(0, 140, 90, 10, BRAUN)

# Das ist ein Hack, da man Bogensegment nicht schön zeichnen kann
# eine Zeichenfläche der Größe 90x60
# Zum bewegen, einfach die Zeichenfläche zf verschieben! Nicht die Ovale
zf = ZeichenFlaeche(90, 140, (90, 60,True))
# Ovale, die auf der Fläche gezeichnet werden!
bogen = Oval(0, 0, 90, 60, BRAUN, eltern_flaeche=zf)
bogen.mitte = (0, 60) # so sieht man nur den rechten oberen Teil des Ovals
# Mit einem 2ten kleineren Oval, den Innenteil des Bogens transparent übermalen
ausschnitt = Oval(0, 0, 80, 50, (0, 0, 0, 0), eltern_flaeche=zf)
ausschnitt.mitte = (0, 60)
Spiel.gib_zeichen_flaeche().fuege_hinzu(zf)



# FERTIG MIT ZEICHNEN



liste = [GELB, HELL_GRUEN, ORANGE]  # konvertiert mit Geany Farbwähler
zufall = randint(0, len(liste) - 1)

schrift = Schrift(40)  # Schriftart kann als 2ter parameter übergeben werden, z.B.: 'Arial'
text = Text('Wilkommen zu Ihrem Adventskalender', 100, 200, schrift=schrift, hintergrund=liste[zufall])
text.zentriere_horizontal()


def zeit_um():
    text.verstecke()


# Um den Text zu verstecken nach 3000 Millisekunden = 3s
textAnim = Animation(3000, animation_gestoppt=lambda: text.selbst_entfernen())
textAnim.start()


# HIER WERDEN ALLE TÜRCHEN WERDEN DEFINIERT

# Diese Funktion wird aufgerufen, wenn eine Tür geklickt wird
# Der Tag wird übergeben
def tuer_geklickt(tag):
    print("Tag: ", tag)


schrift = Schrift(30)  # Schriftart kann als 2ter parameter übergeben werden, z.B.: 'Arial'
# Tuerchen Parameter: tag, links, oben, aktion, schriftart, breite, hoehe, aktive_farbe, inaktiv_farbe
t1 = Tuerchen(1, 450, 600, tuer_geklickt, schrift, 50, 50)
t4 = Tuerchen(4, 300, 400, tuer_geklickt, schrift, 50, 50)

t2 = Tuerchen(2, 192, 520, tuer_geklickt, schrift, 30, 30, ROT, MATT_ROT)
t8 = Tuerchen(8, 590, 520, tuer_geklickt, schrift, 30, 30, ROT, MATT_ROT)

t5 = Tuerchen(5, 620, 735, tuer_geklickt, schrift, 60, 60, ROT, MATT_ROT)
t10 = Tuerchen(10, 510, 280, tuer_geklickt, schrift, 30, 30, ROT, MATT_ROT)

t3 = Tuerchen(3, 380, 755, tuer_geklickt, schrift, 40, 40, BRAUN, MATT_BRAUN)

t7 = Tuerchen(7, 100, 60, tuer_geklickt, schrift, 40, 40, BLAU, GRAU_BLAU)
t11 = Tuerchen(11, 650, 85, tuer_geklickt, schrift, 40, 40, BLAU, GRAU_BLAU)
t12 = Tuerchen(12, 30, 150, tuer_geklickt, schrift, 60, 50, BRAUN, MATT_BRAUN)


t9 = Tuerchen(9, 265, 835, tuer_geklickt, schrift, 40, 40, HELL_GRUEN, GRUEN)
t23 = Tuerchen(23, 380, 65, tuer_geklickt, schrift, 40, 40, MATT_GOLD, GRAU_GOLD)

schriftKerze = Schrift(18)
t6 = Tuerchen(6, 200, 300, tuer_geklickt, schriftKerze, 20, 70, WEISS, MATT_WEISS)
t13 = Tuerchen(13, 100, 600, tuer_geklickt, schriftKerze, 20, 60, WEISS, MATT_WEISS)
t20 = Tuerchen(20, 640, 560, tuer_geklickt, schriftKerze, 20, 60, WEISS, MATT_WEISS)

# TODO: die Türchen müssen noch gesetzt werden
t14 = Tuerchen(20, 640, 560, tuer_geklickt, schriftKerze, 20, 60, WEISS, MATT_WEISS)
t15 = Tuerchen(20, 640, 560, tuer_geklickt, schriftKerze, 20, 60, WEISS, MATT_WEISS)
t16 = Tuerchen(20, 640, 560, tuer_geklickt, schriftKerze, 20, 60, WEISS, MATT_WEISS)
t17 = Tuerchen(20, 640, 560, tuer_geklickt, schriftKerze, 20, 60, WEISS, MATT_WEISS)
t18 = Tuerchen(20, 640, 560, tuer_geklickt, schriftKerze, 20, 60, WEISS, MATT_WEISS)
t19 = Tuerchen(20, 640, 560, tuer_geklickt, schriftKerze, 20, 60, WEISS, MATT_WEISS)
t21 = Tuerchen(20, 640, 560, tuer_geklickt, schriftKerze, 20, 60, WEISS, MATT_WEISS)
t22 = Tuerchen(20, 640, 560, tuer_geklickt, schriftKerze, 20, 60, WEISS, MATT_WEISS)
t24 = Tuerchen(20, 640, 560, tuer_geklickt, schriftKerze, 20, 60, WEISS, MATT_WEISS)

# List mit allen Türchen
tuerchen = [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15,
            t16, t17, t18, t19, t20, t21, t22, t23, t24]

# Datum kann man sich besser so holen
d = datetime.now()  # heutiges datum
v = d.month  # Monat: 1-12
l = d.day  # Tag: 1-31
unötig = 0

print("Monat:", v)
print("Tag:", l)
if v == 11:
    # Dec
    #    l=l + 1
    #    NR1["background"]= 'blue'
    for unötig in range(l, 24):
        print(unötig)
        tuerchen[unötig].deaktiviere()

# Hilfsgitter einblenden
# Spiel.zeichne_gitter()

# Um das Spiel zu starten, muss Spiel.start() aufgerufen werden. Dies sollte immer die letzte Anweisung sein.
Spiel.starten()
