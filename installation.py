import sys
import subprocess
import os
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

    # In neuem Prozess versuchen zu installieren
    process = subprocess.Popen(["pip", "install", "--use-wheel", datei_name])
    code = process.wait()

    if code == 0:
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
    print("Aktualisiere py2cd")


variante = "install"
"""
erg = input(
    "Willst du py2cd als Entwicklungsversion installieren?\nWenn du dir nicht sicher bist antworte mit n. Tippe 'j' für Ja und 'n' für nein. [j/n]:")


if erg[0].lower() == "j":
    variante = "develop"
"""

process = subprocess.Popen(["python", "setup.py", variante])
code = process.wait()

if code == 0:
    ist_py2cd_installiert()
    print("Installation erfolgreich!")
else:
    print("Die Installation ist fehlgeschlagen :(\nHast du die nötigen Berechtigungen?")
