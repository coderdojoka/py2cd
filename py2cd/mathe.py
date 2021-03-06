from py2cd.poly import AALinien

__author__ = 'Mark Weinreuter'


class Plot(AALinien):
    """
    Einfaches Werkzeug um eine mathematische Kurve zu plotten
    """

    def __init__(self, gleichung, start, ende, farbe=(0, 0, 0), vergroesserung_x=10,
                 vergroesserung_y=10, unterteilung=100, eltern_flaeche=None):
        """
        Plottet die gegebenen Gleichung zwischen Start und Endwert
        :param gleichung: Die zu plottende Funktion, z.B: lambda x: x**2
        :type gleichung: (float) -> float
        :param start: Startwert
        :type start: float
        :param ende: Endwert
        :type ende: float
        :param eltern_flaeche:
        :type eltern_flaeche:
        :param farbe:
        :type farbe:
        :param vergroesserung: Ein Vergröerungsfaktor, um die Kurve besser sehen zu können
        :type vergroesserung: float
        :param unterteilung:
        :type unterteilung:
        :return:
        :rtype:
        """

        punkte = []
        # Plotlänge
        delta = ende - start
        # Plotschritte
        diff = delta / unterteilung
        x = start

        # Solange es noch Untereilungen gibt
        while unterteilung >= 0:
            # Punkt berechnen
            punkte.append((x * vergroesserung_x, -gleichung(x) * vergroesserung_y))

            x += diff
            unterteilung -= 1

        # Eltern Konstruktor
        super().__init__(punkte, False, farbe, eltern_flaeche)

    def klone(self, x, y):
        raise NotImplementedError("Sorry, noch nicht implementiert, bzw. wird nicht unterstützt.")
