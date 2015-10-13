# py2cd
Py2cd ist ein simples 2D-Zeichen/Spiele-Framework, dass auf [pygame](http://pygame.org) basiert.
Es ist auf Deutsch geschrieben und dient als Python3-Spiele Framework für das CoderDojo in Karlsruhe

## pygame-Installation
Als Abhängigkeit wird pygame benötigt. Dies muss zuerst installiert werden.

### Windows
Für Windows kann [hier](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame) die Datei pygame‑1.9.2a0‑cp34‑none‑win32.whl
herunterladen und mittels:    
```
pip install --use-wheel pygame‑1.9.2a0‑cp34‑none‑win32.whl
```
installiert werden.   

Eine detailierter Anleitung ist [hier](https://github.com/coderdojoka/Materialien/raw/master/Installation/installation_pygame.pdf) zu finden.

### Linux

Die Installation ist abhängig von der jeweiligen Distribution. Z.B:

#### Arch Linux
```
pacman -S python-pygame
```

#### Ubuntu
Für Ubuntu ist es komplizierter, da die pygame für Python3 selbst kompiliert werden muss. Eine Anleitung kann z.B. [hier](http://askubuntu.com/questions/401342/how-to-download-pygame-in-python3-3) finden.


## py2cd-Installation
Da py2cd sich noch im Entwicklungsstatus befindet ist es am Besten, py2cd als Development-Version zu installieren. D.h. wenn die Source-Dateien aktualisiert werden, bleibt py2cd aktuell:    
```
python setup.py develop
```
Alternativ als normale Installation (erfordert u.U. Adminrechte) mit:
```python
python setup.py install
```

## Beispiele
Im Ordner Beispiele sind ein paar (kommentierte) Beispileprogramme zu finden.