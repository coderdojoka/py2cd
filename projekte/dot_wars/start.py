import time

from arena import Arena

__author__ = 'Mark Weinreuter'

print("Willkommen zum Kampf der Programme\n")
print("Der heutige Kampf wird ausgetragen zwischen:")
algo1 = input("In der linken Ecke (z.B. zufall.Zufall1): ").strip()
algo2 = input("In der rechten Ecke (z.B. zufall.Zufall1): ").strip()

if len(algo1) < 2:
    algo1 = "zufall.Zufall1"
if len(algo2) < 2:
    algo2 = "zufall.Zufall1"

algo1_mod, algo1_name = algo1.split(".")
algo2_mod, algo2_name = algo2.split(".")

GRENZE = 10
algo1_stats = {"name": algo1_name, "siege": 0, "punkte": [], "zuege": []}
algo2_stats = {"name": algo2_name, "siege": 0, "punkte": [], "zuege": []}

for runde in range(0, GRENZE):

    # Immer abwechselnd Spieler1 und Spieler2 laufen lassen
    if runde % 2 == 0:
        arena = Arena(algo1_mod, algo1_name, algo2_mod, algo2_name)
        a1 = algo1_stats
        a2 = algo2_stats
    else:
        arena = Arena(algo2_mod, algo2_name, algo1_mod, algo1_name)
        a1 = algo2_stats
        a2 = algo1_stats

    arena.start()

    punkte1 = []
    punkte2 = []

    print()
    print("Runde: ", runde)
    print()

    while arena.laueft_noch():
        p1, p2 = arena.aktualisiere()
        punkte1.extend(p1)
        punkte2.extend(p2)
        print("Punkte: %s = %d, %s = %d" % (a1["name"], len(punkte1), a2["name"], len(punkte2)))
        time.sleep(.01)

    print()
    print("Züge gesamt: %d, augeteilt: %d|%d" % tuple(arena.zuege_uebersicht))
    print("Punkte: %d|%d" % tuple(arena.punkte))

    if arena.punkte[0] > arena.punkte[1]:
        print("Algorithmus 1 gewinnt!")
        a1["siege"] += 1
    else:
        print("Algorithmus 2 gewinnt!")
        a2["siege"] += 1

    a1["zuege"].append(arena.zuege_uebersicht[1])
    a2["zuege"].append(arena.zuege_uebersicht[2])

    a1["punkte"].append(arena.punkte[0])
    a2["punkte"].append(arena.punkte[1])

print("Algorithmus 1: ", algo1_stats)
print("Algorithmus 2: ", algo2_stats)
