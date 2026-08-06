
from typing import Callable, TypedDict

from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import (
    ListProperty,
    NumericProperty,
    ObjectProperty,
    StringProperty,
)

from kivymd.uix.list import (
    MDListItem,
    MDListItemLeadingIcon,
    MDListItemSupportingText,
    MDListItemTrailingIcon,
)
from kivymd.uix.menu import MDDropdownMenu

class _DropDownMenuItem(TypedDict):
    text: str
    on_release: Callable[[], None]

class DropDownSelector(MDListItem):

    icon = StringProperty("menu")
    values: list[_DropDownMenuItem] = ListProperty([])
    selected_index = NumericProperty(0)

    formatter = ObjectProperty(lambda value: str(value))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.leadingIcon = MDListItemLeadingIcon()
        self.textLabel = MDListItemSupportingText()
        self.trailingIcon = MDListItemTrailingIcon(icon="menu-down")

        self.add_widget(self.leadingIcon)
        self.add_widget(self.textLabel)
        self.add_widget(self.trailingIcon)

        self.menu = MDDropdownMenu(
            caller=self,
            items=[],
            position="bottom",
            hor_growth="right",
            ver_growth="down",
        )

        self.bind(
            icon=self._update_icon,
            values=self._update_menu,
            selected_index=self._update_selection,
        )

        self.bind(
            on_release=lambda *_: self.open_menu()
        )

        self._update_icon()
        self._update_menu()
        self._update_selection()

        self.register_event_type("on_selection_changed")

    def _update_icon(self, *_):
        self.leadingIcon.icon = self.icon

    def _update_menu(self, *_):

        self.menu.items = []

        for index, value in enumerate(self.values):
            self.menu.items.append({
                "text": self.formatter(value),
                "height": dp(36),
                "on_release": lambda i=index: self.select(i),
            })

    def _update_selection(self, *_):

        if not self.values:
            self.textLabel.text = ""
            return

        value = self.values[self.selected_index]
        self.textLabel.text = self.formatter(value)

    def on_selection_changed(self, value):
        """
        Fired whenever the selected item changes.
        """
        pass

    def select(self, index: int):

        self.selected_index = index
        self.menu.dismiss()

        self.dispatch(
            "on_selection_changed",
            self.selected_value
        )

    @property
    def selected_value(self):
        if not self.values:
            return None
        return self.values[self.selected_index]

    def open_menu(self):

        def _open(*_):
            self.menu.open()
            self.menu.width = self.width

            wx, wy = self.to_window(*self.pos)
            self.menu.x = wx
            self.menu.y = wy - self.menu.height

        Clock.schedule_once(_open)
