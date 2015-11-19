import os
import subprocess
import sys
import urllib.request

__author__ = 'Mark Weinreuter'


def download(url, datei_name):
    try:
        response = urllib.request.urlopen(url)
        with open(datei_name, 'wb') as f:
            data = response.read()
            f.write(data)

    except Exception as e:
        print("Download-Fehler: " + url, e)
        exit(-1)


def ist_pygame_installiert():
    try:
        import pygame
        print("Gut! Wir haben pygame", pygame.ver)
        return True

    except Exception as e:
        print("Pygame ist nicht installiert :(", e)
        return False


def ist_py2cd_installiert():
    try:
        import py2cd
        print("Gut! Wir haben py2cd", py2cd.version)
        return True

    except Exception as e:
        print("Py2cd ist nicht installiert :( ", e)
        return False


def install_pygame():
    print("Installiere pygame...\n")

    if vMinor not in ["3", "4", "5"]:
        print("Sorry, für diese Python Version ist dieser Skript nicht ausgelegt.")
        exit(-1)

    datei_name = "pygame-1.9.2a0-cp3%s-none-win32.whl" % vMinor

    # Falls nicht vorhanden runterladen
    if not os.path.isfile(datei_name):
        print("Pygame wheel Datei nicht gefunden. \nLade herunter. Bitte warten...")
        download("http://weinreuter.org/python/" + datei_name, datei_name)
        print("Fertig heruntergeladen.")

    fertig = False
    pip_pfad = "pip"
    pip_code = -1

    # Pip ist nicht immer im Pfad vorhanden
    while not fertig:
        try:
            # In neuem Prozess versuchen zu installieren
            process = subprocess.Popen([pip_pfad, "install", "--use-wheel", datei_name])
            pip_code = process.wait()
            fertig = True

        except FileNotFoundError as e:
            print("Fehler beim Installieren mit pip: ", e)
            pip_pfad = input("Pip konnte nicht gefunden werden. Bitte gib den Pfad zu pip an (z.B.: C:\Python34\Scripts\pip.exe) : ")
            print()

    if pip_code == 0:
        print("\n\nDie Installation scheint funktioniert zu haben. Überprüfe die Ausgabe, um sicher zu sein.")
        ist_pygame_installiert()

    else:
        print("\n\nDie Installation hat nicht geklappt. Prüfe die Ausgabe und versuche es erneut.")
        exit(-1)


ver = sys.version
vMajor = ver[0]
vMinor = ver[2]

print("Du verwendest: Python", vMajor + "." + vMinor, "\n")

if vMajor != "3":
    print("Py2cd ist für Python 3 augelegt, du verwendest:", vMajor + "." + vMinor)
    print("Falls du Python3 installiert hast, bitte starte dieses Skript damit.")
    exit(-1)

ist_windows = (os.name == "nt")
hat_pygame = ist_pygame_installiert()
hat_py2cd = ist_py2cd_installiert()

# Windows Info :D
if ist_windows:
    print("Du benutzt Windows.")
else:
    print("Du benutzt kein Windows, gut :)")

# Pygame Installation prüfen
if not hat_pygame:
    print("Pygame ist nicht installiert.")

    if ist_windows:
        install_pygame()
    else:
        print("Sorry, du musst dir pygame selbst installieren. Einfach mal googlen.")
        exit(-1)

# Pygame Installation testen
print()
if not hat_py2cd:
    print("Py2cd ist nicht installiert.")
    print("Installiere Py2cd")
else:
    print("Aktualisiere py2cd...")

process = subprocess.Popen(["python", "setup.py", "install"])
code = process.wait()

if code == 0:
    ist_py2cd_installiert()
    print("Installation erfolgreich!")
else:
    print("Die Installation ist fehlgeschlagen :(\nHast du die nötigen Berechtigungen?")
