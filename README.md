# py2cd
Py2cd ist ein simples 2D-Zeichen/Spiele-Framework, dass auf [pygame](http://pygame.org) basiert.
Es ist auf Deutsch geschrieben und dient als Python3-Spiele Framework für das CoderDojo in Karlsruhe

## Variante 1: Installations-Skript
Die einfachst Möglichkeite py2cd und pygame zu installieren, ist das Installationsskript _installation.py_ auszuführen. Dieses installiert pygame und py2cd. Dafür lädt es, falls benögtigt, die pygame-Installationsdatei herunter. Dies funktioniert allerdings nur unter Windows. Für andere Betriebssysteme muss pygame manuell installiert werden.

Py2cd kann immer über dieses Skript installiert/aktualisiert werden.      
 
#### Schritt 1: 
 Zur Installation muss die neuste Version als [Zip-Archiv](https://github.com/coderdojoka/py2cd/archive/master.zip) heruntergeladen und entpackt werden.

#### Schritt 2:
Anschließend wird die Installation gestartet, indem man das Python-Skript _'installation.py'_ ausführt.
 Hat alles geklappt, können die unten stehenden Installations-Schritte übersprungen werden. 

#### Schritt 3:
Die Installation kann überprüft werden, indem man ein Beispielprogramm aus dem Beispiele-Ordner, der im Zip-Archiv ebenfalls enthalten ist, startet. 

## Variante 2: Manuelle Installation
### pygame-Installation
Als Abhängigkeit wird pygame benötigt. Dies muss zuerst installiert werden.

#### Windows

##### Detailierte Anleitung
Eine detailiertere Anleitung ist [hier](https://github.com/coderdojoka/Materialien/raw/master/Installation/installation_pygame.pdf) zu finden.

##### Kurzanleitung
Für Windows kann [hier](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame) die Datei _pygame‑1.9.2a0‑cp34‑none‑win32.whl_
herunterladen werden. In der Kommandozeile/Konsole kann pygame dann mittels:    
```
pip install --use-wheel pygame‑1.9.2a0‑cp34‑none‑win32.whl
```
installiert werden.   
__TIpp:__ Hält man im Windows-Explorer die Shift-Taste gedrückt und Rechts-klickt auf den Ordner, so kann man im Menü den Eintrag: 'Eingabeaufforderung/Kommandozeile hier öffnen' auswählen.



#### Linux

Die Installation ist abhängig von der jeweiligen Distribution. Z.B:

##### Arch Linux
```
pacman -S python-pygame
```

##### Ubuntu
Für Ubuntu ist es komplizierter, da die pygame für Python3 selbst kompiliert werden muss. Eine Anleitung kann z.B. [hier](http://askubuntu.com/questions/401342/how-to-download-pygame-in-python3-3) finden.


### py2cd-Installation
Das Repository Klonen oder als [Zip-Datei](https://github.com/coderdojoka/py2cd/archive/master.zip) herunterladen und entpacken.
 

Im heruntergeladenen Ordner folgenden Befehl in der Kommandozeile/Eingabeaufforderung ausführen, um py2cd zu installieren (erfordert u.U. Adminrechte):
```python
python setup.py install
```
__TIpp:__ Hält man im Windows-Explorer die Shift-Taste gedrückt und Rechts-klickt auf den Ordner, so kann man im Menü den Eintrag: 'Eingabeaufforderung/Kommandozeile hier öffnen' auswählen.

## Tutorials
Im [Materialien](https://github.com/coderdojoka/Materialien/tree/master/Python/Roter%20G%C3%BCrtel/Tutorials/py2cd) Repository sind Tutorials zu py2cd zu finden.

## Beispiele
Im Ordner [Beispiele](https://github.com/coderdojoka/py2cd/tree/master/beispiele/) sind ein paar (kommentierte) Beispielprogramme zu finden. Sowie im [Materialien-Repository](https://github.com/coderdojoka/Materialien/tree/master/Python/Beispiele/py2cd/)
