
import ColorTypes

from kivy.uix.widget import Widget
from kivy.graphics import (
    Color,
    Rectangle,
    Ellipse,
    Line
)

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

def set_border(
    widget: Widget,
    color: ColorTypes.ColorTuple,
    widthP: int = 1
) -> None:
    
    print(widget.background_color)

    print(widget.background_normal)

    print(widget.background_active)

    print(widget.size_hint_y)


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