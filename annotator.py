from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from model.image_list import ImageListModel
from presenter.presenter import Presenter
from view.main_window import MainWindow
import logging


def run():
    app = QApplication([])
    model = ImageListModel()
    view = MainWindow()
    presenter = Presenter(model, view)
    app.setWindowIcon(QIcon("assets/logo.png"))
    app.exec()

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    args = parser.parse_args()

    if args.verbose:
        format = '%(filename)s - %(levelname)s - %(funcName)s - %(message)s'
        logging.basicConfig(level=logging.INFO, format=format)
        logging.info('Logger initialized with INFO level')
    
    run()
