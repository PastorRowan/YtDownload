
from kivy.uix.widget import Widget
from kivy.graphics import (
    Color,
    Rectangle,
    Ellipse
)

class CustomGraphics():

    @staticmethod
    def set_rect_bg(
        widget: Widget,
        r: float,
        g: float,
        b: float,
        a: float = 1
    ) -> None:

        with widget.canvas.before:

            Color(r, g, b, a)

            widget.bg_rect = Rectangle(pos=widget.pos, size=widget.size)

            def update_rect(
                instance,
                value
            ):
                instance.bg_rect.pos = instance.pos
                instance.bg_rect.size = instance.size

            # listen to size and position changes
            widget.bind(pos=update_rect, size=update_rect)

    @staticmethod
    def set_ellipse_bg(
        widget: Widget,
        r: float,
        g: float,
        b: float,
        a: float = 1
    ) -> None:

        with widget.canvas.before:

            Color(r, g, b, a)  # Ellipse color
            widget.bg_ellipse = Ellipse(pos=widget.pos, size=widget.size)

            def update_circle(
                instance,
                value
            ):
                instance.bg_ellipse.pos = instance.pos
                instance.bg_ellipse.size = instance.size

            # listen to size and position changes
            widget.bind(pos=update_circle, size=update_circle)
