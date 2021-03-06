from . import callback
from . import focus
from . import label
from . import theme


class Button(label.Label):
    """A button with a text caption.

    Essentially an interactive label.

    Signals

        on_clicked(button, mousebutton)

    """

    def __init__(self, frame, caption):
        if frame.h == 0:
            frame.h = theme.aktive_szene.button_height
        label.Label.__init__(self, frame, caption)
        self._enabled = True
        self.on_clicked = callback.Signal()

    def layout(self):
        label.Label.layout(self)
        if self.frame.w == 0:
            self.frame.w = self.text_size[0] + self.padding[0] * 2
            label.Label.layout(self)

    def maus_hoch(self, button, point):
        focus.set(None)
        self.on_clicked(self, button)
