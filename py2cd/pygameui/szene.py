from . import focus
from . import view
from . import window

stack = []
aktive_szene = None


def push(scene):
    global aktive_szene
    stack.append(scene)
    aktive_szene = scene
    aktive_szene.aktiviere()
    focus.set(None)


def pop():
    global aktive_szene

    if len(stack) > 0:
        aktive_szene.deaktiviere()
        stack.pop()

    if len(stack) > 0:
        aktive_szene = stack[-1]
        aktive_szene.aktiviere()

    focus.set(None)


class Szene(view.View):
    """A view that takes up the entire window content area."""

    def __init__(self, mit_hintergrund=True):
        view.View.__init__(self, window.rect)
        self._mit_hintergrund = mit_hintergrund

    def taste_unten(self, key, code):
        from . import pygame

        if key == pygame.K_ESCAPE:
            pop()

    def deaktiviere(self):
        pass

    def aktiviere(self):
        self.stylize()

        if self._mit_hintergrund:
            # Keine Hintergrundfarbe zulassen, da sonst eine Mischung aus Spiel und GUI
            # nicht möglich wäre, um allerdings dropshadows zu erlauben
            # überzeichnen wir den Hintergrund mit einem transparenten Schwarz
            self.background_color = (0, 0, 0, 0)

    def zeichne(self):
        super().zeichne()
