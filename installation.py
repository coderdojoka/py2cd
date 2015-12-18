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

    print("Sorry, du musst zuerst pygame installieren.")
    print("Hier gibts Infos dazu: https://github.com/coderdojoka/py2cd")
    exit(-1)

# Pygame Installation testen
print()
if not hat_py2cd:
    print("Py2cd ist nicht installiert.")
    print("Installiere Py2cd")
else:
    print("Aktualisiere py2cd...")

process = subprocess.Popen(["python3", "setup.py", "install"])
code = process.wait()

if code == 0:
    ist_py2cd_installiert()
    print("Installation erfolgreich!")
else:
    print("Die Installation ist fehlgeschlagen :(\nHast du die nötigen Berechtigungen?")
