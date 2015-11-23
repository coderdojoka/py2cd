## py2cd
Py2cd ist ein einfaches 2D-Zeichen/Spiele-Framework, dass auf [pygame](http://pygame.org) basiert.
Es ist auf Deutsch geschrieben und dient als Python3-Spiele Framework für das CoderDojo in Karlsruhe

### pygameui
py2cd unterstüzt GUI-Elemente mithilfe von [pygameui](https://github.com/fictorial/pygameui). Das Copyright dafür liegt bei dem ursprünglichen Autor.

### Installation

#### pygame installieren

Da py2cd auf pygame basiert, muss pygame zuerst installiert werden.

| Betriebsystem | Anleitung 	|
| :------------ | :-------- 	|
| Windows		| [hier][win]	|
| Linux			| [hier][lin]	|
| Mac			| [hier][mac]	|


#### py2cd installieren oder aktualisieren
 
#### Schritt 1: Aktuelle Version herunterladen:
Zur Installation muss die aktuellste Version als [Zip-Archiv][zip] heruntergeladen und entpackt werden.

#### Schritt 2: 
Zur Installation muss lediglich das Python-Skript _'installation.py'_ ausführt werden.

#### Alternative zu Schritt 2:
Hat die Installation mit mittels _installation.py_ nicht geklappt, kann man folgenden Befehl im entpackten Ordner in der Kommandozeile/Eingabeaufforderung ausführen, um py2cd zu installieren (erfordert u.U. Adminrechte).

```python
python setup.py install
```


#### Schritt 3:
Die Installation kann überprüft werden, indem man ein Beispielprogramm aus dem Beispiele-Ordner, der im Zip-Archiv ebenfalls enthalten ist, startet. 


## Tutorials
Im [Materialien][tuts] Repository sind Tutorials zu py2cd zu finden.

## Beispiele
Im Ordner [Beispiele][bsp] sind einige (kommentierte) Beispielprogramme zu finden. Sowie im [Materialien-Repository][mats]


[mats]: https://github.com/coderdojoka/Materialien/tree/master/Python/Beispiele/py2cd/
[tuts]: https://github.com/coderdojoka/Materialien/tree/master/Python/Fortschritte/Tutorials/py2cd
[bsp]: https://github.com/coderdojoka/py2cd/tree/master/beispiele/


[zip]: https://github.com/coderdojoka/py2cd/archive/master.zip
[win]: https://github.com/coderdojoka/py2cd/blob/master/pygame_windows.md
[lin]: https://github.com/coderdojoka/py2cd/blob/master/pygame_lin.md
[mac]: https://github.com/coderdojoka/py2cd/blob/master/pygame_mac.md