from py2cd.bbox import BBox
from py2cd.vektor import Vektor2

__author__ = 'Mark Weinreuter'


class Aktualisierbar(object):
    _aktualisierebare = []
    """
    Liste aller aktualisierbaren Objekte.
    :type: list[py2cd.objekte.Aktualisierbar
    """

    def entferne_aktualisierung(self):
        if self in Aktualisierbar._aktualisierebare:
            Aktualisierbar._aktualisierebare.remove(self)

    def __init__(self):
        Aktualisierbar._aktualisierebare.append(self)

    @classmethod
    def aktualisiere_alle(cls, relativer_zeit_unterschied, zeit_unterschied_ms):
        for aktualisierbar in Aktualisierbar._aktualisierebare:
            aktualisierbar.aktualisiere(relativer_zeit_unterschied, zeit_unterschied_ms)

    def aktualisiere(self, relativer_zeitunterschied, zeit_unterschied_ms):
        raise NotImplementedError("Methode muss überschrieben werden.")


class Zeichenbar(BBox):
    """
    Überklasse für alle zeichenbaren Objekte. Diese haben ein Position (x,y) und eine (Hintergrund-)Farbe.
    """

    def __init__(self, x, y, breite, hoehe, farbe, eltern_flaeche, position_geaendert=None):
        """
        Ein neues Zeichenbares Objekt mit der gegebenen (Hintergrund-)Farbe und Elternfläche.

        :param x:
        :type x: float
        :param y:
        :type y: float
        :param breite:
        :type breite: float
        :param hoehe:
        :type hoehe: float
        :param farbe:
        :type farbe:tuple[int]|None
        :param eltern_flaeche:
        :type eltern_flaeche: py2cd.flaeche.ZeichenFlaeche
        :param position_geaendert: die Funktion, die aufgerufen wird, wenn sich die Position dieses Objekts geändert hat
        :type position_geaendert: () -> None
        """

        super().__init__(x, y, breite, hoehe, eltern_flaeche, position_geaendert)

        self.ignoriere_kamera = False
        """
        Falls dieses Flag gesetzt ist, wird die Kamera bei zeichnen ignoriert.

        :type: bool
        """
        self.farbe = farbe
        """
        Die Farbe dieses Objekts.

        :type: tuple[int]
        """

        self.kollisions_maske = None
        """
        In Arbeit... Um auf pixelbasierte Kollistion zu testen wird diese 2-dimensionale Liste benötigt.
        """

        self.__sichtbar = True
        """ Ob das Objekt gezeichnet werden soll."""

        self._eltern_flaeche = eltern_flaeche
        """
        :type: py2cd.flaeche.ZeichenFlaeche
        """

        # füge das Element zum Elternelement hinzu
        if self._eltern_box is not None:
            self._eltern_flaeche.fuege_hinzu(self)

        # die Position wurde aktualisiert
        self.position_geaendert()

    def render(self, pyg_zeichen_flaeche, x_offset=0, y_offset=0):
        """
        Zeichnet dieses Objekt.

        :param pyg_zeichen_flaeche: die Elternfläche
        :type pyg_zeichen_flaeche: pygame.Surface
        :return:
        :rtype: pygame.Rect
        """
        raise NotImplementedError("render() Methode muss überschrieben werden!")

    def zeichne(self, x_offset=0, y_offset=0):
        """
        Zeichnet das aktuelle Objekt, genauer ruft render() auf, falls das Objekt sichtbar ist.
        :param y_offset:
        :type y_offset:
        :param x_offset: optional offset
        :type x_offset: int

        """
        in_rechteck = (
            self.eltern_box is not None and self.beruehrt_rechteck(0 - x_offset, 0 - y_offset,
                                                                   self.eltern_box.breite, self.eltern_box.hoehe))

        if self.__sichtbar and in_rechteck:  # sichtbar und in elternbox sichtbar
            self.render(self._eltern_flaeche.pyg_flaeche, x_offset, y_offset)

    def verstecke(self):
        """
        Versteckt dieses Objekt.
        """
        self.__sichtbar = False

    def selbst_entfernen(self):
        """
        Entfernt dieses Objekt von seiner Elternfläche und wird damit nicht mehr gezeichnet.
        """
        if self._eltern_flaeche is None:
            print("Das Objekt ist nicht an eine Elternfläche gebunden! Wurde es bereits entfernt?")
        else:
            self._eltern_flaeche.entferne(self)

    def ist_sichtbar(self):
        """
        Gibt an, ob das Objekt sichtbar ist
        :return: True, falls sichtbar
        :rtype: bool
        """
        return self.__sichtbar

    def zeige(self):
        """
        Zeigt dieses Objekt an, nachdem es versteckt wurde.
        """
        self.__sichtbar = True

    def nach_vorne(self):
        """
        Sorgt dafür, dass dieses Objekt als Letztes und damit ganz oben gezeichnet wird.
        """
        self._eltern_flaeche.zeichenbare_objekte.remove(self)
        self._eltern_flaeche.zeichenbare_objekte.append(self)

    def nach_hinten(self):
        """
        Sorgt dafür, dass dieses Objekt als erstes und damit ganz unten gezeichnet wird.
        """
        self._eltern_flaeche.zeichenbare_objekte.remove(self)
        self._eltern_flaeche.zeichenbare_objekte.insert(0, self)


class ZeichenbaresElement(Zeichenbar):
    def __init__(self, x, y, breite, hoehe, farbe, eltern_flaeche=None, position_geaendert=None):
        """

        :param x: die x-Koordinate
        :type x: float
        :param y: die y-Koordinate
        :type y: float
        :param breite: die Breite des umgebenden Rechtecks
        :type breite: float
        :param hoehe: die Höhe des umgebenden Rechtecks
        :type hoehe: float
        :param farbe: die (Hintergrund-) Farbe
        :type farbe: None|tuple[int]
        :param eltern_flaeche: die Elternfläche (Standard: Spiel.haupt_flaeche)
        :type eltern_flaeche: py2cd.flaeche.Flaeche
        :param position_geaendert: die Funktion, die bei Positonsänderung aufgerufen wird
        :type position_geaendert: () -> None
        """
        if eltern_flaeche is None:
            # falls keine Elternfläche angegeben wurde, dann wir die Haupt-Zeichenfläche verwendet
            from py2cd.spiel import Spiel

            eltern_flaeche = Spiel.standard_flaeche

        self.__abprallen = False
        """
        Falls gesetzt, wird beim Aufruf von bewege() auf Kollision mit dem Rand überprüft

        :type: bool
        """

        self.__geschwindigkeit = Vektor2(0, 0)
        """
        Die Bewegung in X/Y-Richtung

        :type: py2cd.vektor.Vektor2
        """

        super().__init__(x, y, breite, hoehe, farbe, eltern_flaeche, position_geaendert)

    def klone(self, x, y):
        raise NotImplementedError("Muss überschrieben werden")

    def pralle_vom_rand_ab(self, abprallen=True):
        """
        Wird aprallen auf Wahr gesetzt, dann prallt diese vom Rand ab, falls die bewege-Funktion verwendet wird.
        :param abprallen:
        :type abprallen:
        :return:
        :rtype:
        """
        self.__abprallen = abprallen

    @property
    def x_geschwindigkeit(self):
        """
        Gibt die x-Geschwindigkeit zurück, d.h. die Strecke in Pixeln,
        die pro bewege()-Aufruf weiter bewegt wird.

        :return: die x-Geschwindigkeit
        :rtype: float
        """
        return self.__geschwindigkeit.x

    @property
    def y_geschwindigkeit(self):
        """
        Gibt die y-Geschwindigkeit zurück, d.h. die Strecke in Pixeln,
        die pro bewege()-Aufruf weiter bewegt wird.

        :return: die y-Geschwindigkeit
        :rtype: float
        """

        return self.__geschwindigkeit.y

    @x_geschwindigkeit.setter
    def x_geschwindigkeit(self, value):
        self.__geschwindigkeit.x = value

    @y_geschwindigkeit.setter
    def y_geschwindigkeit(self, value):
        self.__geschwindigkeit.y = value

    def x_bewegung_umkehren(self):
        """
        Kehrt die Bewegungsrichtung um. D.h. falls das Objekt sich zur Zeit nach rechts bewegt (eine positive x-Geschwindigkeit hat),
        wird diese Geschwindigkeit invertiert und die Bewegung findet nun in die entgegengesetze Richtung (nach links) statt.
        """
        self.__geschwindigkeit.x *= -1

    def y_bewegung_umkehren(self):
        """
        Kehrt die Bewegungsrichtung um. D.h. falls das Objekt sich zur Zeit nach unten bewegt (eine positive y-Geschwindigkeit hat),
        wird diese Geschwindigkeit invertiert und die Bewegung findet nun in die entgegengesetze Richtung (nach oben) statt.
        """
        self.__geschwindigkeit.y *= -1

    def setze_geschwindigkeit(self, x=5, y=5):
        """
        Setzt die x- und y-Geschwindigkeit für dieses Objekt.

        :param x: x-Geschwindigkeit
        :type x: float
        :param y: y-Geschwindigkeit
        :type y: float
        """
        self.__geschwindigkeit.setze(x, y)

    def aendere_geschwindigkeit(self, x=0, y=0):
        """
        Ändert die x- und y-Geschwindigkeit für dieses Objekt um den gegenenen Wert.

        :param x: x-Geschwindigkeit
        :type x: float
        :param y: y-Geschwindigkeit
        :type y: float
        """

        self.__geschwindigkeit.aendere(x, y)

    def gib_geschwindigkeit(self):
        """
        Gibt die aktuelle Geschwindigkeit dieses Objekts als Tupel zurück.

        :return: x-, y-Geschindigkeit als Tupel
        :rtype: tuple[float]
        """
        return self.__geschwindigkeit.x, self.__geschwindigkeit.y

    def bewege(self, dt=1):
        """
        Bewegt dieses Objekt um die gegebene Anzahl an Schritten mit der definierten Geschwindigkeit. Falls die gewünscht wird auch auf Kollision
        mit dem Rand überprüft.

        :param dt: relative Zeitdelta
        :type dt: float
        """
        if self.__abprallen:
            if self.beruehrt_oberen_oder_unteren_rand():
                self.y_bewegung_umkehren()

            if self.beruehrt_linken_oder_rechten_rand():
                self.x_bewegung_umkehren()

        self.aendere_position(self.__geschwindigkeit.x * dt, self.__geschwindigkeit.y * dt)

    def mache_schritte(self, schritte=1, dt=1):
        """
        Bewegt dieses Objekt um die gegebene Anzahl an Schritten mit der definierten Geschwindigkeit. Falls die gewünscht wird auch auf Kollision
        mit dem Rand überprüft.

        :param schritte: die Anzahl an Schritten
        :type schritte: int
        """

        while schritte > 0:
            if self.__abprallen:
                if self.beruehrt_oberen_oder_unteren_rand():
                    self.y_bewegung_umkehren()

                if self.beruehrt_linken_oder_rechten_rand():
                    self.x_bewegung_umkehren()

            self.aendere_position(self.__geschwindigkeit.x * dt, self.__geschwindigkeit.y * dt)

            schritte -= 1

    def render(self, pyg_zeichen_flaeche, x_offset=0, y_offset=0):
        """
        Diese Methode muss überschrieben werden.

        :param pyg_zeichen_flaeche:
        :type pyg_zeichen_flaeche:
        :return:
        :rtype:pygame.Rect
        """
        raise NotImplementedError("render() Methode muss überschrieben werden!")


class SkalierbaresElement:
    """
    Klasse für skalierbare Element. Skalieren und Rotieren ist kombiniert in einem Aufruf von rotozoom.
    Tranformationen sind kostenintensive Operationen!
    """

    def __init__(self, zeichenbaresElement):
        self._winkel = 0
        self._skalierung = 1.0
        self.__zeichenbaresElement = zeichenbaresElement

    def setze_rotation(self, winkel):
        self.rotiere_und_skaliere(winkel, self._skalierung)

    def aendere_rotation(self, winkel_aenderung):
        self.rotiere_und_skaliere(self._winkel + winkel_aenderung, self._skalierung)

    def setze_skalierung(self, skalierung):
        self.rotiere_und_skaliere(self._winkel, skalierung)

    def aendere_skalierung(self, skalierungs_aenderung):
        self.rotiere_und_skaliere(self._winkel, self._skalierung + skalierungs_aenderung)

    def aendere_rotation_und_skalierung(self, winkel_aenderung, skalierungs_aenderung):
        self.rotiere_und_skaliere(self._winkel + winkel_aenderung, self._skalierung + skalierungs_aenderung)

    def rotiere_und_skaliere(self, winkel, skalierung):
        """
        Rotiert und skaliert das aktuelle Objekt um den gegebenen Winkel
        und skaliert das Objekt um den angebenen Faktor.

        :param winkel: Rotation in Grad
        :type winkel: float
        :param skalierung: Skalierung, 1.0 ist die Orginalgröße
        :type skalierung: float
        """
        self._winkel = winkel
        self._skalierung = skalierung

        # die Mitte ist ein Fixpunkt! so können wir später die Position wieder herstellen
        alte_mitte = self.__zeichenbaresElement.mitte

        neue_dimension = self._rotation_skalierung_anwenden()
        self.__zeichenbaresElement._aendere_groesse(*neue_dimension)
        self.mitte = alte_mitte

    def _rotation_skalierung_anwenden(self):
        """

        Diese Methode wird von rotiere_und_skaliere() aufgerufen. Hier muss die eigentliche Operation
        implementiert werden.

        :return: ein Tupel mit der neuen Größe
        :rtype: (float, float)
        """
        raise NotImplementedError("Muss überschrieben werden!")


"""
    def _mitte_nach_rotation_zurueck_setzen(self, alte_mitte):
        ""
        Diese Methode wird aufgerufen, nachdem rotiert wurde und die Postion wiederhergestellt werden muss.
        In den meisten Fällen ist self.mitte = alte_mitte genug

        :param alte_mitte: die alte Mitte
        :type alte_mitte: (float, float)
        ""
        raise NotImplementedError("Muss überschrieben werden!")
"""
