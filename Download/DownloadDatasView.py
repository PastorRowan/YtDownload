
from typing import (
    List
)

from kivymd.uix.boxlayout import MDBoxLayout

from kivy.properties import (
    ListProperty
)
from kivy.metrics import dp

import Colors

from .DownloadData import DownloadData
from .DownloadDataView import DownloadDataView

DownloadDatas = List[DownloadData]

class DownloadDatasView(MDBoxLayout):

    downloadDatas: DownloadDatas = ListProperty([])

    def __init__(self, **kwargs):

        kwargs.setdefault("spacing", dp(12))
        kwargs.setdefault("padding", dp(12))

        super().__init__(
            orientation="vertical",
            size_hint=(1, None),
            size_hint_x=1,
            size_hint_y=None,
            adaptive_height=True,
            **kwargs
        )

        self.bind(
            downloadDatas=lambda instance, value: self._onDownloadDatasChanged(instance, value),
        )

        self._onDownloadDatasChanged(self, self.downloadDatas)

    def _onDownloadDatasChanged(self, instance, value):

        downloadDatas: DownloadDatas = value            

        self.clear_widgets()

        for downloadData in downloadDatas:
            downloadDataView = DownloadDataView(
                downloadData=downloadData
            )
            self.add_widget(downloadDataView)
