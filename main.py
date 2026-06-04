
from PyQt6.QtWidgets import QApplication
import sys
from MainWindow import MainWindow

def main():

    print("Running")

    app = QApplication(sys.argv)

    window = MainWindow()

    window.show()

    app.exec()

if __name__ == "__main__":
    main()
