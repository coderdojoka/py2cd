---
autor: Mark Weinreuter  
version: 0.1  
kapitel: 1  
minted_ausgabe: tmp_latex  
inhaltsverzeichnis: ja  
titel: py2cd - Übersicht
---


# Grundgerüst
Jedes py2cd-Program muss folgendes Grundgerüst haben:

``` python
# Dies Modul muss immer importiert werden
from py2cd import *
# Für vordefinierte Farben wird dieses Modul benötigt
from py2cd.farben import *

# Das Spiel muss zuerst initialisiert werden!
Spiel.init(640, 480, "Mein Spiel") # Breite, Höhe, Titel


# RESTLICHES PROGRAMM STEHT HIER


# Startet das Spiel. Anweisungen danach werden NICHT ausgeführt
Spiel.starten()
```
**Hinweis:** Alle folgenden Beispiele benötigen dieses Grundgerüst.
Oftmals steht es allerdings nicht dabei damit die Beispiele kürzer werden!
 
# Vorhandene Objekte
Es stehen verschiedene vordefinierte Objekte zur Verfügung.
Die Position dieser Objekte bezieht sich immer auf deren **linke obere Ecke**!

## Rechtecke
Benötigte Werte: x, y (linke obere Ecke), Breite,  Höhe und Farbe.
``` python
r1 = Rechteck(270, 200, 100, 100, GELB)
```

## Kreise
Benötigte Werte: x, y (linke obere Ecke), Radius und Farbe.

``` python
k1 = Kreis(390, 110, 70, MATT_GRUEN)
```


## Linie
Benötigte Werte: Start- und Endpunkt, jeweils x- und y-Koordinate in einem Tupel z.B. `(100, 140)`, Farbe,  Dicke (optional). 

``` python
l1 = Linie((100, 300), (540, 300), ROT, 2)
```

## Ovale
Benötigte Werte: x, y (linke obere Ecke), Breite-Radius, Höhe-Radius und Farbe.

``` python
o1 = Oval(100, 50, 20, 30, GELB)
```

## Text
Benötigte Werte: Der Text, x, y (linke obere Ecke) und Farbe.
``` python
t1 = Text('Hallo', 100, 200, SCHWARZ)
```

## Polygone (Vielecke)
Benötigte Werte: Liste aller Eckpunkte, jeweils x- und y-Koordinate in einem Tupel z.B. `(100, 140)`. 
``` python
ecken_liste = [(190, 242), (195, 238), (200, 242)]
p1 = Polygon(ecken_liste, BLAU)
```

## Bilder
Bilder werden über den `BilderSpeicher` verwaltet, müssen einmal geladen werden und können dann beliebig oft angezeigt werden.  
Benötigte Werte: Interne Name für das Bild (frei wählbar), der Pfad/Dateiname des Bildes auf dem Computer.
``` python
# Das Bild EINMAL in Speicher laden.
# Das Bild liegt in dem Order 'bilder' und heißt 'scratch.png'
BildSpeicher.lade_bild("scratch", "bilder/scratch.png")

# Das Bild zweimal an verschiedenen Stellen anzeigen
bild1 = BildSpeicher.gib_bild("scratch", 100, 100)
bild2 = BildSpeicher.gib_bild("scratch", 300, 250)
```


## Animationen
Animation sind einfach ein Liste von Bildern, die schnell hintereinander angezeigt werden.
``` python
namen_liste = ['bilder/n1.png', 'bider/n2.png']
a1 = BildAnimation(namen_liste)

# Animation steuern
a1.start() # Animation starten
a1.pause() # Animation pausieren
a1.stop() # Animation stoppen

a1.setze_wiederhole(True) # Animation endlos wiederholen
```
**Hinweis:** Die Bildernamen können ENTWEDER, der interne Name im Bildspeicher (z.B. oben 'scratch') 
ODER der Dateipfad/Dateiname des Bildes sein.


# Objekte bewegen
Sämtliche oben aufgeführten Objekte besitzen die hier genannten Funktionen. Man ruft diese Funktionen über den Namen der Variablen in der das Objekt gespeichert ist auf. Z.B.: `r1.aendere_position(20, 20)`. 

## Position ändern
**Ändert** die Position eines Objektes **um** einen bestimmten Wert.
Benötigte Werte: x-, y-Wert
``` python
r1 = Rechteck(20, 20, 100, 100, GELB)
r1.aendere_position(100, 100)
```

## Position setzen
**Setzt** die Position eines Objektes **auf** einen bestimmten Wert.  
Benötigte Werte: x-, y-Wert.
``` python
r1 = Rechteck(20, 20, 100, 100, GELB)
r1.setze_position(100, 100)
```

## Position abfragen
Benötigte Werte: Keine.  
Gibt zurück: Ein Tupel (x-, y-Wert)
``` python
r1 = Rechteck(20, 20, 100, 100, GELB)
pos = r1.position() # = (20, 20)
```

## Mitte eines Objektes setzen
Setzt die Mitte eines Objektes, **NICHT** seine linke obere Ecke. Nützlich bei z.B. Kreisen.  
Benötigte Werte: x-, y-Wert.
``` python
k1 = Kreis(450, 150, 10, ROT)
k11.mitte = (455, 155)
```

## Mitte eines Objektes abfragen
Fragt die Mitte eines Objektes ab, NICHT seine linke obere Ecke.  
Benötigte Werte: Keine.  
Gibt zurück: Ein Tupel (x-, y-Wert)
``` python
k1 = Kreis(450, 150, 10, ROT)
mitte = k11.mitte # = (455, 155)
```