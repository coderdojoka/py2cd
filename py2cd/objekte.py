__author__ = 'Mark Weinreuter'


class Zeichenbar:
    """
    Überklasse für alle zeichenbaren Objekte. Diese haben ein Position (x,y) und eine (Hintergrund-)Farbe.
    """

    def __init__(self, x, y, breite, hoehe, farbe, eltern_flaeche, position_geändert=lambda: None):
        """
        Ein neues Zeichenbares Objekt mit der gegebenen (Hintergrund-)Farbe und Elternflaeche.

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
        :param position_geändert: die Funktion, die aufgerufen wird, wenn sich die Position dieses Objekts geändert hat
        :type position_geändert: () -> None
        """

        self.farbe = farbe
        """
        Die Farbe dieses Objekts.

        :type: tuple[int]
        """

        self._eltern_flaeche = eltern_flaeche
        """
        Die Elternfläche dieses Objektes, falls es eine gibt.

        :type: py2cd.flaeche.ZeichenFlaeche
        """

        self.__x = x
        """
        Die interne x-Position.

        :type: float """

        self.__y = y
        """
        Die interne y-Position.

        :type: float
        """

        self.__hoehe = hoehe
        """
        Die Höhe der umgebenden Box (Rechteck).

        :type: float
        """

        self.__breite = breite
        """
        Die Breite der umgebenden Box.

        :type: float
        """

        self.kollisions_maske = None
        """
        In Arbeit... Um auf pixelbasierte Kollistion zu testen wird diese 2-dimensionale Liste benötigt.
        """

        self.__sichtbar = True
        """ Ob das Objekt gezeichnet werden soll."""

        self.position_geaendert = position_geändert
        """
        Funktion die aufgerufen wird, wenn die Position geändert wurde.

        :type: (None)->None
        """

        # füge das Element zum Elternelement hinzu
        if self._eltern_flaeche is not None:
            self._eltern_flaeche.fuege_hinzu(self)

        # die Position wurde aktualisiert
        self.position_geaendert()

    def __str__(self):
        """
        Gibt den Typ dieses Objektes, seine Position und seine Größe aus.

        :return: die Objekt-Info
        :rtype: str
        """
        return str(type(self)) + " Pos: %dx%d Größe: %dx%d" % (self.__x, self.__y, self.breite, self.hoehe)

    @property
    def breite(self):
        """
        Die Breite der umgebenden Box.

        :return: die Breite
        :rtype: float
        """
        return self.__breite

    @property
    def hoehe(self):
        """
        Die Höhe der umgebenden Box.

        :return: die Breite
        :rtype: float
        """
        return self.__hoehe

    # x, y sind nicht direkt setzbar, da position_geandert sonst immer 2mal aufgerufen würde
    @property
    def x(self):
        """
        Der x-Wert gemessen am linken Rand des Elternelementes.

        :return:x-Wert
        :rtype: float
        """
        return self.__x

    @property
    def y(self):
        """
        Der y-Wert gemessen am oberern Rand des Elternelementes.

        :return: y-Wert
        :rtype: float
        """
        return self.__y

    @property
    def mitte(self):
        """
        Der Mittelpunkt dieses Objektes, genauer Mittelpunkt des umgebenden Rechtecks.

        :return: der Mittelpunkt
        :rtype: tuple[float]
        """
        return self.x + self.breite / 2, self.y + self.hoehe / 2

    @mitte.setter
    def mitte(self, mitte):
        self.__x = mitte[0] - (self.breite / 2)
        self.__y = mitte[1] - (self.hoehe / 2)
        self.position_geaendert()

    @property
    def oben(self):
        """
        Der Abstand zum oberen Rand der Elternfläche.

        :return: der Abstand
        :rtype: float
        """
        return self.__y

    @oben.setter
    def oben(self, oben):
        self.__y = oben
        self.position_geaendert()

    @property
    def unten(self):
        """
        Der Abstand zum unteren Rand der Elternfläche.

        :return: der Abstand
        :rtype: float
        """
        return self._eltern_flaeche.hoehe - (self.__y + self.hoehe)

    @unten.setter
    def unten(self, unten):
        self.__y = self._eltern_flaeche.hoehe - (unten + self.hoehe)
        self.position_geaendert()

    @property
    def rechts(self):
        """
        Der Abstand zum rechten Rand der Elternfläche.

        :return: der Abstand
        :rtype: float
        """
        return self._eltern_flaeche.breite - (self.__x + self.breite)

    @rechts.setter
    def rechts(self, rechts):
        self.__x = self._eltern_flaeche.breite - (rechts + self.breite)
        self.position_geaendert()

    @property
    def links(self):
        """
        Der Abstand zum linken Rand der Elternfläche.

        :return: der Abstand
        :rtype: float
        """
        return self.__x

    @links.setter
    def links(self, links):
        self.__x = links
        self.position_geaendert()

    def position(self):
        """
        Gibt die aktuelle Position als Tupel zurück.

        :return: die Positon als Tupel
        :rtype: tuple[float]
        """
        return self.__x, self.__y

    def render(self, pyg_zeichen_flaeche):
        """
        Zeichnet dieses Objekt.

        :param pyg_zeichen_flaeche: die Elternfläche
        :type pyg_zeichen_flaeche: pygame.Surface
        :return:
        :rtype: pygame.Rect
        """
        raise NotImplementedError("render() Methode muss überschrieben werden!")

    def zeichne(self):
        """
        Zeichnet das aktuelle Objekt, genauer ruft render() auf, falls das Objekt sichtbar ist.

        """
        if self.__sichtbar:
            self.render(self._eltern_flaeche.pyg_flaeche)

    def aendere_position(self, x, y):
        """
        Ändert die Position um den gegebenen Wert, d.h: self._x = self._x + x.

        :param x: Änderung des x-Wertes
        :type x: float
        :param y: Änderung des y-Wertes
        :type y: float
        """

        self.__x += x
        self.__y += y
        self.position_geaendert()

    def setze_position(self, x=0, y=0):
        """
        Setzt die Postion dieses Objektes auf die angegebenen Koordinaten.

        :param x: x-Koordinate
        :type x: float
        :param y: y-Koordinate
        :type y: float
        """
        self.__x = x
        self.__y = y
        self.position_geaendert()

    def zentriere(self):
        """
        Zentriert dieses Objekt in seiner Elternflaeche.

        """
        d_breite = self._eltern_flaeche.breite - self.breite
        d_hoehe = self._eltern_flaeche.hoehe - self.hoehe
        self.__x = d_breite / 2
        self.__y = d_hoehe / 2
        self.position_geaendert()

    def zentriere_vertikal(self):
        """
        Zentriert dieses Objekt vertikal in seiner Elternflaeche.
        """
        d_hoehe = self._eltern_flaeche.hoehe - self.hoehe
        self.__y = d_hoehe / 2
        self.position_geaendert()

    def zentriere_horizontal(self):
        """
        Zentriert dieses Objekt horizontal in seiner Elternflaeche.
        """
        d_breite = self._eltern_flaeche.breite - self.breite
        self.__x = d_breite / 2
        self.position_geaendert()

    def zentriere_in_objekt(self, objekt):
        """
        Zentriert dieses Objekt in dem angegebenen Objekt.
        """
        if not isinstance(objekt, Zeichenbar):
            raise ValueError("Objekt muss Zeichenbar sein.")

        self.mitte = objekt.mitte

    def lese_welt_position(self):
        """
        Falls das Objekt in einer geschachtelten Elternfläche ist, wird die Positon aller Elternflächen berücksichtigt.
        :return: die Position
        :rtype: tuple[float]
        """
        x = self.x
        y = self.y

        obj = self._eltern_flaeche

        while obj is not None:
            x += obj.x
            y += obj.y
            obj = obj._eltern_flaeche

        return x, y

    def verstecke(self):
        """
        Versteckt dieses Objekt.
        """
        self.__sichtbar = False

    def zeige(self):
        """
        Zeigt dieses Objekt an, nachdem es versteckt wurde.
        """
        self.__sichtbar = True

    def nach_vorne(self):
        """
        Sorgt dafür, dass dieses Objekt als Letztes und damit ganz oben gezeichnet wird.
        """
        self._eltern_flaeche._zeichenbareObjekte.remove(self)
        self._eltern_flaeche._zeichenbareObjekte.append(self)

    def selbst_entfernen(self):
        """
        Entfernt dieses Objekt von seiner Elternfläche und wird damit nicht mehr gezeichnet.
        """
        self._eltern_flaeche.entferne(self)

    def punkt_in_rechteck(self, punkt):
        """
        Überprüft, ob der Punkt im umgebenden Rechteckt liegt.

        :param punkt: Der zu testende Punkt
        :type punkt:tuple(float)
        :return: Wahr, falls der Punkt innerhalb des Rechtecks ist
        :rtype: bool
        """
        start = self.lese_welt_position()

        left = (start[0] <= punkt[0] <= (start[0] + self.breite))
        top = (start[1] <= punkt[1] <= (start[1] + self.hoehe))

        return left and top

    def beruehrt_rechteck(self, r2_links, r2_oben, breite, hoehe):
        """
        Überprüft ob das umgebende Rechteck das Rechteck mit den angegeben Eckdaten berührt.

        :param r2_links: x-Wert
        :type r2_links: float
        :param r2_oben: y-Wert
        :type r2_oben: float
        :param breite: die Breite des Rechtecks
        :type breite: float
        :param hoehe:  die Höhe des Rechtecks
        :type hoehe: float
        :return: Wahr, falls berührt
        :rtype: bool
        """
        r1_rechts = self.x + self.breite
        r1_unten = self.y + self.hoehe

        r2_rechts = r2_links + breite
        r2_unten = r2_oben + hoehe

        # print("Ich: ", self.x, self.y, self.breite, self.hoehe)
        # print("Du: ", r2_links, r2_oben, r2_rechts, r2_unten)

        return not (r2_links > r1_rechts or r2_rechts < self.x or r2_oben > r1_unten or r2_unten < self.y)

    def ueberschneidung_rechteck(self, r2_links, r2_oben, breite, hoehe):
        """
        Berechnet das Überschneidungsrechteck.

        :param r2_links:
        :type r2_links:
        :param r2_oben:
        :type r2_oben:
        :param breite:
        :type breite:
        :param hoehe:
        :type hoehe:
        :return:
        :rtype:
        """

        if (self.beruehrt_rechteck(r2_links, r2_oben, breite, hoehe)):
            return None

        if self.__x > r2_links:
            links = self.__x
        else:
            links = r2_links

        if self.__x + self.breite < r2_links + breite:
            rechts_oben = self.__x + self.breite
        else:
            rechts_oben = r2_links + breite

        if self.__y > r2_oben:
            oben = self.__y
        else:
            oben = r2_oben

        if self.__y + self.hoehe < r2_oben + hoehe:
            links_unten = self.__y + self.hoehe
        else:
            links_unten = r2_oben + hoehe

        # Die überlagernde Region
        return [links, oben, rechts_oben - links, links_unten - oben]

    def beruehrt_objekt(self, zeichenbar):
        """
        Überprüft, ob dieses Objekt das übergebene Objekt berührt. Genauer, ob das umgebende Rechteck dieses Objektes, das umgebende Rechteckt
        des andren Objektes berührt.

        :param zeichenbar: das andere Objekt
        :type zeichenbar: Zeichenbar
        :return: True oder False
        :rtype: bool
        """
        return self.beruehrt_rechteck(zeichenbar.x, zeichenbar.y, zeichenbar.breite, zeichenbar.hoehe)

    def beruehrt_linken_oder_rechten_rand(self):
        """
        Überprüft, ob dieses Objekt den linken oder rechten Rand der Elternfläche berührt.

        :return: True oder False
        :rtype: bool
        """
        return self.beruehrt_linken_rand() or self.beruehrt_rechten_rand()

    def beruehrt_oberen_oder_unteren_rand(self):
        """
        Überprüft, ob dieses Objekt den oberen oder unteren Rand der Elternfläche berührt.

        :return: True oder False
        :rtype: bool
        """
        return self.beruehrt_oberen_rand() or self.beruehrt_unternen_rand()

    def beruehrt_rand(self):
        """
        Überprüft, ob dieses Objekt den Rand der Elternfläche an irgendeiner Stelle berührt.

        :return: Wahr, falls berührt
        :rtype: bool
        """
        return self.beruehrt_linken_rand() or self.beruehrt_oberen_rand() or self.beruehrt_rechten_rand() or self.beruehrt_unternen_rand()

    def beruehrt_oberen_rand(self):
        """
        Überprüft, ob dieses Objekt den oberen Rand der Elternfläche berührt.

        :return: True oder False
        :rtype: bool
        """
        return self.__y <= 0

    def beruehrt_unternen_rand(self):
        """
        Überprüft, ob dieses Objekt den unteren Rand der Elternfläche berührt.

        :return: True oder False
        :rtype: bool
        """
        return self.__y + self.hoehe >= self._eltern_flaeche.hoehe

    def beruehrt_linken_rand(self):
        """
        Überprüft, ob dieses Objekt den linken Rand der Elternfläche berührt.

        :return: True oder False
        :rtype: bool
        """
        return self.__x <= 0

    def beruehrt_rechten_rand(self):
        """
        Überprüft, ob dieses Objekt den rechten Rand der Elternfläche berührt.

        :return: True oder False
        :rtype: bool
        """
        return self.__x + self.breite >= self._eltern_flaeche.breite

    def _aendere_groesse(self, breite, hoehe):
        """
        Ändert die Größe des umgebenden Rechtecks.

        :param breite: die neue Breite
        :type breite: float
        :param hoehe: die neue Höhe
        :type hoehe: float
        """
        self.__breite = breite
        self.__hoehe = hoehe
        self.position_geaendert()


class ZeichenbaresElement(Zeichenbar):
    def __init__(self, x, y, breite, hoehe, farbe, eltern_flaeche=None, position_geaendert=lambda: None):
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
        :type farbe: tuple[int]
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

        self.__geschwindigkeit_x = 5
        """
        Die Bewegung X-Richtung

        :type: float
        """

        self.__geschwindigkeit_y = 5
        """
        Die Bewegung in Y-Richtung

        :type: float
        """

        super().__init__(x, y, breite, hoehe, farbe, eltern_flaeche, position_geaendert)

    def pralle_vom_rand_ab(self, abprallen=True):
        """
        Wird aprallen auf Wahr gesetzt, dann prallt diese vom Rand ab, falls die bewege-Funktion verwendet wird.
        :param abprallen:
        :type abprallen:
        :return:
        :rtype:
        """
        self.__abprallen = abprallen

    def x_geschwindigkeit(self):
        """
        Gibt die x-Geschwindigkeit zurück, d.h. die Strecke in Pixeln,
        die pro bewege()-Aufruf weiter bewegt wird.

        :return: die x-Geschwindigkeit
        :rtype: float
        """
        return self.__geschwindigkeit_x

    def y_geschwindigkeit(self):
        """
        Gibt die y-Geschwindigkeit zurück, d.h. die Strecke in Pixeln,
        die pro bewege()-Aufruf weiter bewegt wird.

        :return: die y-Geschwindigkeit
        :rtype: float
        """

        return self.__geschwindigkeit_y

    def x_bewegung_umkehren(self):
        """
        Kehrt die Bewegungsrichtung um. D.h. falls das Objekt sich zur Zeit nach rechts bewegt (eine positive x-Geschwindigkeit hat),
        wird diese Geschwindigkeit invertiert und die Bewegung findet nun in die entgegengesetze Richtung (nach links) statt.
        """
        self.__geschwindigkeit_x *= -1

    def y_bewegung_umkehren(self):
        """
        Kehrt die Bewegungsrichtung um. D.h. falls das Objekt sich zur Zeit nach unten bewegt (eine positive y-Geschwindigkeit hat),
        wird diese Geschwindigkeit invertiert und die Bewegung findet nun in die entgegengesetze Richtung (nach oben) statt.
        """
        self.__geschwindigkeit_y *= -1

    def setze_geschwindigkeit(self, x=5, y=5):
        """
        Setzt die x- und y-Geschwindigkeit für dieses Objekt.

        :param x: x-Geschwindigkeit
        :type x: float
        :param y: y-Geschwindigkeit
        :type y: float
        """
        self.__geschwindigkeit_x = x
        self.__geschwindigkeit_y = y

    def aendere_geschwindigkeit(self, x=0, y=0):
        """
        Ändert die x- und y-Geschwindigkeit für dieses Objekt um den gegenenen Wert.

        :param x: x-Geschwindigkeit
        :type x: float
        :param y: y-Geschwindigkeit
        :type y: float
        """

        self.__geschwindigkeit_x += x
        self.__geschwindigkeit_y += y

    def gib_geschwindigkeit(self):
        """
        Gibt die aktuelle Geschwindigkeit dieses Objekts als Tupel zurück.

        :return: x-, y-Geschindigkeit als Tupel
        :rtype: tuple[float]
        """
        return self.__geschwindigkeit_x, self.__geschwindigkeit_y

    def bewege(self, schritte=1):
        """
        Bewegt dieses Objekt um die gegebene Anzahl an Schritten mit der definierten Geschwindigkeit. Falls die gewünscht wird auch auf Kollision
        mit dem Rand überprüft.

        :param schritte: die Anzahl an Schritten
        :type schritte: int
        """

        while schritte:
            if self.__abprallen:
                if self.beruehrt_oberen_oder_unteren_rand():
                    self.__geschwindigkeit_y *= -1

                if self.beruehrt_linken_oder_rechten_rand():
                    self.__geschwindigkeit_x *= -1

            self.aendere_position(self.__geschwindigkeit_x, self.__geschwindigkeit_y)

            schritte -= 1

    def render(self, pyg_zeichen_flaeche):
        """
        Diese Methode muss überschrieben werden.

        :param pyg_zeichen_flaeche:
        :type pyg_zeichen_flaeche:
        :return:
        :rtype:pygame.Rect
        """
        raise NotImplementedError("render() Methode muss überschrieben werden!")
