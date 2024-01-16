from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from nimocr.model import ImageListModel
from nimocr.presenter import Presenter
from nimocr.view import MainWindow
import logging


def setup_logger():
    format = "%(filename)s - %(levelname)s - %(funcName)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=format)
    logging.info("Logger initialized with INFO level")


def run():
    app = QApplication([])
    app.setWindowIcon(QIcon("assets/logo.png"))

    model = ImageListModel()
    view = MainWindow()
    presenter = Presenter(model, view)

    app.exec()


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument(
        "--verbose", action="store_true", help="Enable verbose logging"
    )
    args = parser.parse_args()

    if args.verbose:
        setup_logger()
    run()
