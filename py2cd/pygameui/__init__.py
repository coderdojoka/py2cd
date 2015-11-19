"""A simple GUI framework for Pygame.

This framework is not meant as a competitor to PyQt or other, perhaps more
formal, GUI frameworks. Instead, pygameui is but a simple framework for game
prototypes.

The app is comprised of a stack of scenes; the top-most or current scene is
what is displayed in the window. Scenes are comprised of Views which are
comprised of other Views. pygameui contains view classes for things like
labels, buttons, and scrollbars.

pygameui is a framework, not a library. While you write view controllers in the
form of scenes, pygameui will run the overall application by running a loop
that receives device events (mouse button clicks, keyboard presses, etc.) and
dispatches the events to the relevant view(s) in your scene(s).

Each view in pygameui is rectangular in shape and whose dimensions are
determined by the view's "frame". A view is backed by a Pygame surface.
Altering a view's frame requires that you call 'relayout' which will resize the
view's backing surface and give each child view a chance to reposition and/or
resize itself in response.

Events on views can trigger response code that you control. For instance, when
a button is clicked, your code can be called back. The click is a "signal" and
your code is a "slot". The view classes define various signals to which you
connect zero or more slots.

    a_button.on_clicked.connect(click_callback)

"""

AUTHOR = 'Brian Hammond <brian@fictorial.com>'
COPYRIGHT = 'Copyright (C) 2012 Fictorial LLC.'
LICENSE = 'MIT'

__version__ = '0.2.0'

from . import focus
from . import szene
from . import theme
from . import window
from .alert import *
from .button import *
from .callback import *
from .checkbox import *
from .dialog import *
from .flipbook import *
from .grid import *
from .imagebutton import *
from .imageview import *
from .label import *
from .listview import *
from .notification import *
from .progress import *
from .render import *
from .resource import *
from .scroll import *
from .select import *
from .slider import *
from .spinner import *
from .szene import Szene
from .textfield import *
from .view import *

Rect = pygame.Rect
down_in_view = None


def init(breite, hoehe):
    # pygame.key.set_repeat(200, 50)
    window.rect = pygame.Rect((0, 0), (breite, hoehe))
    theme.init()


def zeichne(pyg_flaeche):
    szene.aktive_szene.zeichne()
    pyg_flaeche.blit(szene.aktive_szene.surface, (0, 0))


def reagiere(e):
    global down_in_view

    bubble_event = True
    mouse_point = pygame.mouse.get_pos()

    if e.type == pygame.MOUSEBUTTONDOWN:
        hit_view = szene.aktive_szene.hit(mouse_point)
        logger.debug('hit %s' % hit_view)

        if (hit_view is not None and
                not isinstance(hit_view, szene.Szene)):
            focus.set(hit_view)
            down_in_view = hit_view
            pt = hit_view.from_window(mouse_point)
            hit_view.maus_unten(e.button, pt)

            bubble_event = False

        else:
            focus.set(None)


    elif e.type == pygame.MOUSEBUTTONUP:

        hit_view = szene.aktive_szene.hit(mouse_point)

        if hit_view is not None:

            if down_in_view and hit_view != down_in_view:
                down_in_view.blurred()
                focus.set(None)
            pt = hit_view.from_window(mouse_point)
            hit_view.maus_hoch(e.button, pt)

            bubble_event = True

        # Reset view
        down_in_view = None

    elif e.type == pygame.MOUSEMOTION:

        if down_in_view and down_in_view.draggable:
            pt = down_in_view.from_window(mouse_point)
            down_in_view.maus_gezogen(pt, e.rel)

            bubble_event = False
        else:
            szene.aktive_szene.maus_bewegt(mouse_point)

    elif e.type == pygame.KEYDOWN:

        if focus.view:
            focus.view.taste_unten(e.key, e.unicode)
            bubble_event = False
        else:
            szene.aktive_szene.taste_unten(e.key, e.unicode)

    elif e.type == pygame.KEYUP:

        if focus.view:
            focus.view.taste_oben(e.key)
            bubble_event = False
        else:
            szene.aktive_szene.taste_oben(e.key)

    return bubble_event


def aktualisiere(vergangene_zeit):
    szene.aktive_szene.aktualisiere(vergangene_zeit / 1000.0)
