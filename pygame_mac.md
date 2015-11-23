## Installation von Python3 und pygame unter Mac OS

> *HINWEIS:* Ich habe selbst keinem Mac, die Anleitung stammt aus anderen Quellen (s. unten). Ich bin froh über Hinweise und Verbesserungen :)

Python3 kann direkt über die Python-Webseite oder über den PaketManager _homebrew_ installiert werden.
Hier verwenden wir _homebrew_, da über diesen auch weitere benötigte Komponenten installiert werden.
_Homebrew_ verwaltet Programme separat von 'normal' installierten Programmen. Diese können in der Regel ohne Probleme koexistieren.
Falls Python3 bereits installiert ist, kann es ggf. zu Problemen kommen. (Beleg dafür?)


#### 1.) _homebrew_ installieren:
Homebrew ist ein Paket-Manager für Mac und über das Terminal bedienbar. Die offizielle Hompage ist [hier][hbhome] zu finden.
Homebrew kann installiert werden, indem man folgenden Befehl im Terminal ausführt (Alle so hervorgehobenen Zeile sind, falls nichts anderweitig angegeben, im Terminal auszuführen):

```
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

##### 1.1) _homebrew_ aktualisieren
Nachdem _homebrew_ installiert ist, ist es ratsam _homebrew_ zu aktualisieren mittels:
```
brew update
```
Ggf. vorhandene Probleme können mittels:
```
brew doctor
```
aufgelistet werden. (Keine Ausgabe ist eine gute Ausgabe)

##### 1.2) Homebrew Programme verwenden
Um Programme, die mittels _homebrew_ installiert werden, verwenden zu können, muss folgende Zeile in die Datei *'.bash_profile'* geschrieben werden:
```
export PATH=/usr/local/bin:$PATH
```
Diese Datei liegt im Home-Verzeichnis eines Benutzers und ist standartmäßig versteckt. Das ganze kann man auch mit folgendem Befehl machen:
```
echo 'export PATH=/usr/local/bin:$PATH' >> ~/.bash_profile
```

#### 2.) Python 3 installieren
Python 3 kann nun installiert werden:
```
brew install python3
```

##### 2.1) Python verifizieren
Nach der Installation sollte nun _python3_ im Terminal bekannt sein. Dafür muss das Terminal allerdings geschlossen und neu gestartet werden!
```
python3 --version
```
Dies sollte die Python-Version anzeigen.

#### 3.) Pygame installieren
Pygame hat einige Abhängigkeiten. Diese müssen zuerst installiert werden.

##### 3.1) X-Code Kommandozeilen-Tools installieren
Die X-Code Kommandozeilen-Tools können wie folgt installiert werden:
```
xcode-select --install
```
Ein Dialog erscheint und muss bestätigt werden.

*Hinweis:* Falls dies nicht funktioniert, muss ggf. zuerst X-Code installiert werden.

##### 3.1) XQuartz installieren:
XQuartz wird benötigt und kann unter [http://www.xquartz.org/](http://www.xquartz.org/) heruntergeladen und normal installiert werden.
Der Rechner muss ggf. neugestartet werden.

##### 3.2) Abhängigkeiten installieren
Es müssen nun noch einige kleine Pakete installiert werden:
```
brew install hg sdl sdl_image sdl_mixer sdl_ttf portmidi
```
Um _smeg_ zu installieren, muss man wie folgt vorgehen:
```
brew tap homebrew/headonly
brew install smpeg --HEAD
```

##### 3.3) Pygame installieren
Nun kann pygame installiert werden. Dies kann einige Zeit dauern und produziert ggf. viele Ausgaben im Terminal
```
pip3 install hg+http://bitbucket.org/pygame/pygame
```

Wenn alles geklappt hat, kann man die Installation testen, indem die folgenden Zeilen nacheinander im Terminal eingibt.
Ggf. muss dafür das Terminal neu gestartet werden.

```
python3
import pygame
exit()
```
Wenn alles funktioniert, werden keine Fehlermeldungen angezeigt :)


#### Quellen:
Pygame Website: [http://pygame.org/wiki/macintosh](http://pygame.org/wiki/macintosh)  
Blog-Eintrag: [http://brysonpayne.com/2015/01/10/setting-up-pygame-on-a-mac/](http://brysonpayne.com/2015/01/10/setting-up-pygame-on-a-mac/)

[hbhome]: http://brew.sh/

