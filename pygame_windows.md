#### Windows

##### Detailierte Anleitung
Eine detailiertere Anleitung ist [hier](https://github.com/coderdojoka/Materialien/raw/master/Installation/installation_pygame.pdf) zu finden.

##### Kurzanleitung
##### 1.) Installationsdatei herunterladen
Für Windows kann [hier](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame) die pygame-Installationsdatei heruntergeladen werden. Es gibt dort verschiedene Versionen und man muss die richtige Datei auswählen.

Es wird unterschieden nach Pythonversion und Python-Art (32-bit oder 64-bit).
Führt man folgenden Befehl in der Eingabeaufforderung aus, erhält man Informationen über die Python version.

```
python --version
```

Der Dateiname setzt sich wie folgt zusammen:

_pygame‑1.9.2a0‑cp[VERSION]‑none‑[ART].whl_

Beispiel: die Python Version, sind zwei Zahlen hintereinander z.B. '34' für Python 3.4. Die Art ist z.B. 'win32' oder 'amd64'.

Für Python 3.4 mit 32-bit ergibt sich also:

_pygame‑1.9.2a0‑cp34‑none‑win32.whl_

Die entsprechende Datei muss nun heruntergeladen werden.

__Hinweis:__ die Seite braucht u.U. lange bis sie fertig geladen ist


##### 2.) Pygame installieren
Nun kann man die zuvor heruntergeladene Datei mit folgendem Befehl installieren:    
```
pip install --use-wheel pygame‑1.9.2a0‑cp34‑none‑win32.whl
```

__TIpp:__ Hält man im Windows-Explorer die Shift-Taste gedrückt und Rechts-klickt auf den Ordner, so kann man im Menü den Eintrag: 'Eingabeaufforderung/Kommandozeile hier öffnen' auswählen.
