# py2cd
Py2cd ist ein simples 2D-Zeichen/Spiele-Framework, dass auf [pygame](http://pygame.org) basiert.
Es ist auf Deutsch geschrieben und dient als Python3-Spiele Framework für das CoderDojo in Karlsruhe

## pygame-Installation
Als Abhängigkeit wird pygame benötigt. Dies muss zuerst installiert werden.

### Windows
Für Windows kann [hier](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame) die Datei _pygame‑1.9.2a0‑cp34‑none‑win32.whl_
herunterladen werden. In der Kommandozeile/Konsole kann pygame dann mittels:    
```
pip install --use-wheel pygame‑1.9.2a0‑cp34‑none‑win32.whl
```
installiert werden.   
__TIpp:__ Hält man im Windows-Explorer die Shift-Taste gedrückt und Rechts-klickt auf den Ordner, so kann man im Menü den Eintrag: 'Kommandozeile hier öffnen' auswählen.

Eine detailiertere Anleitung ist [hier](https://github.com/coderdojoka/Materialien/raw/master/Installation/installation_pygame.pdf) zu finden.

### Linux

Die Installation ist abhängig von der jeweiligen Distribution. Z.B:

#### Arch Linux
```
pacman -S python-pygame
```

#### Ubuntu
Für Ubuntu ist es komplizierter, da die pygame für Python3 selbst kompiliert werden muss. Eine Anleitung kann z.B. [hier](http://askubuntu.com/questions/401342/how-to-download-pygame-in-python3-3) finden.


## py2cd-Installation
Das Repository Klonen oder als [Zip-Datei](https://github.com/coderdojoka/py2cd/archive/master.zip) herunterladen und entpacken.

Da py2cd sich noch im Entwicklungsstatus befindet ist es am Besten, py2cd als Development-Version zu installieren. D.h. wenn die Source-Dateien aktualisiert werden, bleibt py2cd aktuell, der heruntergeladene Ordner muss allerdings an der gleichen Stelle bleiben!    

Im heruntergeladenen Ordner dann folgenden Befehl in der Kommandozeile/Konsole ausführen:
```
python setup.py develop
```


Alternativ als normale Installation (erfordert u.U. Adminrechte) mit:
```python
python setup.py install
```
## Tutorials
Im [Materialien](https://github.com/coderdojoka/Materialien/tree/master/Python/Roter%20G%C3%BCrtel/Tutorials/py2cd) Repository sind Tutorials zu py2cd zu finden.

## Beispiele
Im Ordner [Beispiele](https://github.com/coderdojoka/py2cd/tree/master/beispiele/) sind ein paar (kommentierte) Beispielprogramme zu finden. Sowie im [Materialien-Repository](https://github.com/coderdojoka/Materialien/tree/master/Python/Beispiele/py2cd/)