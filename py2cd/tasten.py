from py2cd.ereignis import EreignisBearbeiter

__author__ = 'Mark Weinreuter'


class Taste:
    def __init__(self, pyg_konstante, zeichen=""):
        self.pyg_konstante = pyg_konstante
        self.zeichen = zeichen

        self.gedrueckt_bearbeiter = EreignisBearbeiter()
        self.wenn_unten_bearbeiter = EreignisBearbeiter()

    # TODO: do not use the pyg_ereignis
    def unten(self, pyg_ereignis):
        self.gedrueckt_bearbeiter(True, pyg_ereignis)

    def oben(self, pyg_ereignis):
        self.gedrueckt_bearbeiter(False, pyg_ereignis)
