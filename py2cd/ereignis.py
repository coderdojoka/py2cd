import collections

__author__ = 'Mark Weinreuter'


class EreignisBearbeiter(object):
    def __init__(self):
        self.registrierte_bearbeiter = []

    def registriere(self, bearbeiter):
        if not isinstance(bearbeiter, collections.Callable):
            raise AttributeError("Der Bearbeiter muss aufrufbar sein.")

        self.registrierte_bearbeiter.append(bearbeiter)

    def entferne(self, bearbeiter):
        if bearbeiter in self.registrierte_bearbeiter:
            self.registrierte_bearbeiter.remove(bearbeiter)
        else:
            print("Bearbeiter war nicht registriert!")

    def __call__(self, *args, **kwargs):
        for bearbeiter in self.registrierte_bearbeiter:
            bearbeiter(*args, **kwargs)

    def entferne_alle(self):
        self.registrierte_bearbeiter.clear()


class Ereignis(object):
    pass
