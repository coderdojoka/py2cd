import py2cd.ereignis
import py2cd.vektor

__author__ = 'Mark Weinreuter'


class BBox:
    LINKS = 1
    RECHTS = 2
    OBEN = 3
    UNTEN = 4

    def __init__(self, x, y, breite, hoehe, eltern_box, position_geaendert=None):
        """
        Ein neue Box, die positioniert werden kann.

        :param x:
        :type x: float
        :param y:
        :type y: float
        :param breite:
        :type breite: float
        :param hoehe:
        :type hoehe: float
        :param eltern_box:
        :type eltern_box: py2cd.bbox.BBox
        :param position_geaendert: die Funktion, die aufgerufen wird, wenn sich die Position dieses Objekts geändert hat
        :type position_geaendert: () -> None
        """

        self._eltern_box = eltern_box
        """
        Die Elternfläche dieses Objektes, falls es eine gibt.

        :type: py2cd.bbox.BBox
        """

        self.__position = py2cd.vektor.Vektor2(x, y)
        """
        Die Position der Box.

        :type: py2cd.vektor.Vektor2
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

        self.position_geaendert = py2cd.ereignis.EreignisBearbeiter()
        """
        Funktion die aufgerufen wird, wenn die Position geändert wurde.

        :type: py2cd.EreignisBearbeiter
        """
        if position_geaendert is not None:
            self.position_geaendert.registriere(position_geaendert)

        # die Position wurde aktualisiert
        self.position_geaendert()

    def __str__(self):
        """
        Gibt den Typ dieses Objektes, seine Position und seine Größe aus.

        :return: die Objekt-Info
        :rtype: str
        """
        return str(type(self)) + " Pos: %dx%d Größe: %dx%d" % (self.__position.x, self.__position.y, self.breite, self.hoehe)

    @property
    def eltern_box(self):
        return self._eltern_box

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
        return self.__position.x

    @property
    def y(self):
        """
        Der y-Wert gemessen am oberern Rand des Elternelementes.

        :return: y-Wert
        :rtype: float
        """
        return self.__position.y

    @property
    def mitte(self):
        """
        Der Mittelpunkt dieses Objektes, genauer Mittelpunkt des umgebenden Rechtecks.

        :return: der Mittelpunkt
        :rtype: py2cd.vektor.Vektor2
        """
        return py2cd.vektor.Vektor2(self.x + self.breite / 2, self.y + self.hoehe / 2)

    @mitte.setter
    def mitte(self, mitte):
        self.__position.setze(mitte[0] - (self.breite / 2), mitte[1] - (self.hoehe / 2))
        self.position_geaendert()

    @property
    def oben(self):
        """
        Der Abstand zum oberen Rand der Elternfläche.

        :return: der Abstand
        :rtype: float
        """
        return self.__position.y

    @oben.setter
    def oben(self, oben):
        self.__position.y = oben
        self.position_geaendert()

    @property
    def unten(self):
        """
        Der Abstand zum unteren Rand der Elternfläche.

        :return: der Abstand
        :rtype: float
        """
        return self._eltern_box.hoehe - (self.__position.y + self.hoehe)

    @unten.setter
    def unten(self, unten):
        self.__position.y = self._eltern_box.hoehe - (unten + self.hoehe)
        self.position_geaendert()

    @property
    def rechts(self):
        """
        Der Abstand zum rechten Rand der Elternfläche.

        :return: der Abstand
        :rtype: float
        """
        return self._eltern_box.breite - (self.__position.x + self.breite)

    @rechts.setter
    def rechts(self, rechts):
        self.__position.x = self._eltern_box.breite - (rechts + self.breite)
        self.position_geaendert()

    @property
    def links(self):
        """
        Der Abstand zum linken Rand der Elternfläche.

        :return: der Abstand
        :rtype: float
        """
        return self.__position.x

    @links.setter
    def links(self, links):
        self.__position.x = links
        self.position_geaendert()

    def position(self):
        """
        Gibt die aktuelle Position als Tupel zurück.

        :return: die Positon als Tupel
        :rtype: py2cd.vektor.Vektor2
        """
        return self.__position.klone()

    def gehe_nach_rechts(self, wert):
        self.__position.x += wert
        self.position_geaendert()

    def gehe_nach_links(self, wert):
        self.__position.y -= wert
        self.position_geaendert()

    def aendere_position(self, x, y=None):
        """
        Ändert die Position um den gegebenen Wert, d.h: self._x = self._x + x.

        :param x: Änderung des x-Wertes oder ein Tupeltyp
        :type x: float|(float, float)
        :param y: Änderung des y-Wertes
        :type y: float
        """

        if y is not None:
            self.__position.aendere(x, y)
        else:
            self.__position.aendere(x[0], x[1])
        self.position_geaendert()

    def setze_position(self, x, y=None):
        """
        Setzt die Position dieses Objektes auf die angegebenen Koordinaten.

        :param x: x-Koordinate oder ein Tupeltyp
        :type x: float|(float,float)
        :param y: y-Koordinate
        :type y: float
        """
        if y is not None:
            self.__position.setze(x, y)
        else:
            self.__position.setze(x[0], x[1])
        self.position_geaendert()

    def zentriere(self):
        """
        Zentriert dieses Objekt in seiner Elternflaeche.

        """
        d_breite = self._eltern_box.breite - self.breite
        d_hoehe = self._eltern_box.hoehe - self.hoehe
        self.__position.setze(d_breite / 2, d_hoehe / 2)
        self.position_geaendert()

    def zentriere_vertikal(self):
        """
        Zentriert dieses Objekt vertikal in seiner Elternflaeche.
        """
        d_hoehe = self._eltern_box.hoehe - self.hoehe
        self.__position.y = d_hoehe / 2
        self.position_geaendert()

    def zentriere_horizontal(self):
        """
        Zentriert dieses Objekt horizontal in seiner Elternflaeche.
        """
        d_breite = self._eltern_box.breite - self.breite
        self.__position.x = d_breite / 2
        self.position_geaendert()

    def zentriere_in_objekt(self, objekt):
        """
        Zentriert dieses Objekt in dem angegebenen Objekt.
        """
        if not isinstance(objekt, BBox):
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

        obj = self._eltern_box

        while obj is not None:
            x += obj.x
            y += obj.y
            obj = obj._eltern_box

        return x, y

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

        if self.beruehrt_rechteck(r2_links, r2_oben, breite, hoehe):
            return None

        if self.__position.x > r2_links:
            links = self.__position.x
        else:
            links = r2_links

        if self.__position.x + self.breite < r2_links + breite:
            rechts_oben = self.__position.x + self.breite
        else:
            rechts_oben = r2_links + breite

        if self.__position.y > r2_oben:
            oben = self.__position.y
        else:
            oben = r2_oben

        if self.__position.y + self.hoehe < r2_oben + hoehe:
            links_unten = self.__position.y + self.hoehe
        else:
            links_unten = r2_oben + hoehe

        # Die überlagernde Region
        return [links, oben, rechts_oben - links, links_unten - oben]

    def kollision_links_rechts(self, box, bx):

        if (self.y + self.hoehe) <= box.y or self.y >= (box.y + box.hoehe):
            # keine kollision
            return None

        if bx > 0 and (self.x + self.breite) <= box.x:  # bewegung nach rechts

            self_rechts = self.x + self.breite
            # kollision nur wenn die untere kante innerhalb des blocks
            if box.x < self_rechts + bx < box.x + box.breite:
                return box.x - self_rechts, BBox.RECHTS

        elif bx < 0 and self.x >= (box.x + box.breite):

            box_rechts = box.x + box.breite
            # kollision nur wenn die obere kante innerhalb des blocks
            if box.x <= self.x + bx <= box.x + box.breite:
                return box_rechts - self.x, BBox.LINKS

        return None

    def kollision_oben_unten(self, box, by):

        if (self.x + self.breite) <= box.x or self.x >= (box.x + box.breite):
            # keine kollision
            return None

        if by > 0:  # bewegung nach unten

            self_unten = self.y + self.hoehe
            if box.y < self_unten + by < box.y + box.hoehe:  # kollision nur wenn die untere kante innerhalb des blocks
                return box.y - self_unten, BBox.UNTEN

        elif by < 0:

            box_unten = box.y + box.hoehe
            if box.y < self.y + by < box.y + box.hoehe:  # kollision nur wenn die obere kante innerhalb des blocks
                return self.y - box_unten, BBox.OBEN

        return None

    def sichtbar_in_elternbox(self):
        return self.eltern_box or self.beruehrt_objekt(self.eltern_box)

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
        return self.beruehrt_oberen_rand() or self.beruehrt_unteren_rand()

    def beruehrt_rand(self):
        """
        Überprüft, ob dieses Objekt den Rand der Elternfläche an irgendeiner Stelle berührt.

        :return: Wahr, falls berührt
        :rtype: bool
        """
        return self.beruehrt_linken_rand() or self.beruehrt_oberen_rand() or self.beruehrt_rechten_rand() or self.beruehrt_unteren_rand()

    def beruehrt_oberen_rand(self):
        """
        Überprüft, ob dieses Objekt den oberen Rand der Elternfläche berührt.

        :return: True oder False
        :rtype: bool
        """
        return self.__position.y <= 0

    def beruehrt_unteren_rand(self):
        """
        Überprüft, ob dieses Objekt den unteren Rand der Elternfläche berührt.

        :return: True oder False
        :rtype: bool
        """
        return self.__position.y + self.hoehe >= self._eltern_box.hoehe

    def beruehrt_linken_rand(self):
        """
        Überprüft, ob dieses Objekt den linken Rand der Elternfläche berührt.

        :return: True oder False
        :rtype: bool
        """
        return self.__position.x <= 0

    def beruehrt_rechten_rand(self):
        """
        Überprüft, ob dieses Objekt den rechten Rand der Elternfläche berührt.

        :return: True oder False
        :rtype: bool
        """
        return self.__position.x + self.breite >= self._eltern_box.breite

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
