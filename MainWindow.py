
from PyQt6.QtWidgets import (
    QMainWindow,
    QPlainTextEdit,
    QLabel,
    QPushButton,
    QWidget,
    QVBoxLayout
)

from PyQt6.QtCore import Qt

from DownloadThread import DownloadThread

class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        # Member variables
        self.input = QPlainTextEdit()
        self.input.setPlaceholderText("Enter your text")
        self.input.selectionChanged.connect(self.selection_changed)
        self.input.textChanged.connect(self.text_changed)

        self.status = QLabel()
        self.status.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        self.downloadButton = QPushButton("Download")
        self.downloadButton.pressed.connect(self.download_video)

        self.downloadThread = None

        self.setWindowTitle("YoutubeDL")

        self.setMinimumWidth(700)
        self.setMinimumHeight(700)

        centralWidget = QWidget()

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.input, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.status, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.downloadButton, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addStretch()

        centralWidget.setLayout(layout)

        self.setCentralWidget(centralWidget)

    def download_video(self):

        self.input.setEnabled(False)
        self.status.clear()

        """
https://youtu.be/FHv53DVH48Y?si=Hi13tjAq0j6ZU6Ue
        """
        self.downloadThread = DownloadThread(self.input.toPlainText())

        self.downloadThread.finished_signal.connect(self.download_finished)
        self.downloadThread.success_signal.connect(self.download_successful)
        self.downloadThread.error_signal.connect(self.download_failed)

        self.downloadThread.start()

    def download_finished(self):
        self.input.setEnabled(True)

    def download_successful(self, message):
        self.status.setText(message)

    def download_failed(self, message):
        self.status.setText(message)

    def selection_changed(self):
        print("Selection changed")
        print(self.input.toPlainText())

    def text_changed(self):
        print("Text changed...")
        print(self.input.toPlainText())
