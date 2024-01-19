import logging

from PyQt6.QtGui import QIcon, QFontDatabase, QFont
from PyQt6.QtWidgets import QApplication

from src.nimocr.model import ImageListModel
from src.nimocr.presenter import Presenter
from src.nimocr.view import MainWindow


def setup_logger() -> None:
    """Setup the logger with INFO level."""
    format = "%(filename)s - %(levelname)s - %(funcName)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=format)
    logging.info("Logger initialized with INFO level")


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
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    args = parser.parse_args()

    if args.verbose:
        setup_logger()
    main()
