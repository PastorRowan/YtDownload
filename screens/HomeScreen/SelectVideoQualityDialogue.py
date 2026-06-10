
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogHeadlineText,
    MDDialogContentContainer,
    MDDialogButtonContainer,
    MDDialogSupportingText,
    MDDialogIcon
)
from kivymd.uix.widget import Widget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import (
    MDButton,
    MDButtonText
)

from kivymd.uix.selectioncontrol import MDCheckbox

class SelectVideoQualityDialogue(MDDialog):

    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            **kwargs
        )

        self.register_event_type("on_confirm")

        self.videoQualityCheckboxes = {}

        self.add_widget(
            MDDialogIcon(
                icon="high-definition-box"
            )
        )
        self.add_widget(
            MDDialogHeadlineText(
                text="Video quality"
            )
        )
        self.add_widget(
            MDDialogSupportingText(
                text="Limit the video quality when multiple are present"
            )
        )

        content = MDDialogContentContainer(
            orientation="vertical",
            spacing="12dp",
            padding="12dp"
        )

        for videoQuality, active in [
            ("Best quality", False),
            ("2160p", False),
            ("1440p", False),
            ("1080p", False),
            ("720p", True),
            ("480p", False),
            ("360p", False),
            ("Lowest quality", False),
        ]:
            checkbox = MDCheckbox(
                group="video_quality",
                active=active
            )

            self.videoQualityCheckboxes[videoQuality] = checkbox

            content.add_widget(
                MDBoxLayout(
                    checkbox,
                    MDLabel(text=videoQuality),
                    orientation="horizontal",
                    adaptive_height=True
                )
            )

        content.add_widget(
            MDDialogButtonContainer(
                Widget(
                    size_hint=(1, None),
                    height=0
                ),
                MDButton(
                    MDButtonText(
                        text="Cancel"
                    ),
                    style="text",
                    on_release=lambda x: self.dismiss()
                ),
                MDButton(
                    MDButtonText(
                        text="Confirm"
                    ),
                    style="text",
                    on_release=lambda x: self._on_confirm()
                ),
                spacing="8dp"
            )
        )

        self.add_widget(content)

    def getSelectedVideoQuality(self):
        for videoQuality, checkbox in self.videoQualityCheckboxes.items():
            if checkbox.active:
                return videoQuality

        return None

    def on_confirm(self, videoQuality):
        """
        Default handler required by Kivy.
        Override or bind to this event externally.
        """
        pass

    def _on_confirm(self):

        selectedVideoQuality = self.getSelectedVideoQuality()

        self.dispatch(
            "on_confirm",
            selectedVideoQuality
        )
