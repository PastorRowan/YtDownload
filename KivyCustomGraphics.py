
import ColorTypes

from kivy.uix.widget import Widget
from kivy.graphics import (
    Color,
    Rectangle,
    Ellipse,
    Line
)

from kivy.metrics import dp

from kivy.core.window import Window

def set_rect_bg(
    widget: Widget,
    color: ColorTypes.ColorTuple
) -> None:

    if len(color) == 3:
        r, g, b = color
        a = 1.0
    else:
        r, g, b, a = color

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

def set_ellipse_bg(
    widget: Widget,
    color: ColorTypes.ColorTuple
) -> None:

    if len(color) == 3:
        r, g, b = color
        a = 1.0
    else:
        r, g, b, a = color

    with widget.canvas.before:

        widget.bg_ellipse_color = Color(r, g, b, a)
        widget.bg_ellipse = Ellipse()

        def _update_ellipse(*args):
            w, h = widget.size

            # ellipse size = widget size (you can change this if needed)
            ew, eh = w, h

            # TRUE center alignment
            widget.bg_ellipse.pos = (
                widget.center_x - ew * 0.75,
                widget.center_y
            )

            widget.bg_ellipse.size = (ew, eh)

        # listen to size and position changes
        widget.bind(
            pos=lambda instance, value: _update_ellipse(instance, value),
            size=lambda instance, value: _update_ellipse(instance, value)
        )

        _update_ellipse()

def set_border(
    widget: Widget,
    color: ColorTypes.ColorTuple,
    widthP: int = 1
) -> None:

    if len(color) == 3:
        r, g, b = color
        a = 1.0
    else:
        r, g, b, a = color

    with widget.canvas.after:

        Color(r, g, b, a)

        widget.custom_border = Line(
            rectangle=(
                widget.x,
                widget.y,
                widget.width,
                widget.height
            ),
            width=widthP
        )

        def update_border(
            instance,
            value
        ):
            instance.custom_border.rectangle = (
                instance.x,
                instance.y,
                instance.width,
                instance.height
            )

        # listen to size and position changes
        widget.bind(pos=update_border, size=update_border)

def set_max_width( 
    widget,
    max_width,
    margin=0
):

    widget.size_hint_x = None

    def update(*_):
        if not widget.parent:
            return

        available = widget.parent.width - margin
        available = max(0, available)

        widget.width = min(available, max_width)

    def on_parent(instance, value):
        parent = value
        if parent:
            parent.bind(size=update)
            update()

    widget.bind(parent=on_parent)

def set_max_height(
    widget,
    reference_widget,
    max_height,
    margin
):

    # IMPORTANT: you take control of height
    widget.size_hint_y = None

    def update(*args):
        widget.height = min(reference_widget.height - margin, max_height)

    reference_widget.bind(size=update)

    update()
