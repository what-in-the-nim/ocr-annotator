import logging

from PyQt6.QtGui import QIcon, QFontDatabase, QFont
from PyQt6.QtWidgets import QApplication

from src.nimocr.model import ImageListModel
from src.nimocr.presenter import Presenter
from src.nimocr.view import MainWindow


def main() -> None:
    """Initialize the application."""
    app = QApplication([])
    # Register fonts
    QFontDatabase.addApplicationFont('assets/fonts/IBM_Plex_Sans_Thai/IBMPlexSansThai-Regular.ttf')
    QFontDatabase.addApplicationFont('assets/fonts/IBM_Plex_Sans_Thai/IBMPlexSansThai-Bold.ttf')
    # Set default application fonts
    all_registered_fonts = QFontDatabase.families()
    logging.info(f"Registered fonts: {all_registered_fonts}")
    app.setFont(QFont("IBM Plex Sans Thai", 12))
    app.setWindowIcon(QIcon("assets/logo.png"))

    model = ImageListModel()
    view = MainWindow()
    _ = Presenter(model, view)

    app.exec()


if __name__ == "__main__":
    format = "%(filename)s - %(levelname)s - %(funcName)s - %(message)s"
    logging.basicConfig(
        filename='user.log',
        level=logging.INFO,
        format=format,
        filemode='w',
        encoding='utf-8'
    )
    logging.info("Logger initialized with INFO level")

    main()
