from PyQt6.QtWidgets import QApplication
from model.image_list import ImageListModel
from presenter.presenter import Presenter
from view.main_window import MainWindow
import logging

def addLoggingLevel(levelName, levelNum, methodName=None):
    if not methodName:
        methodName = levelName.lower()

    if hasattr(logging, levelName):
        raise AttributeError('{} already defined in logging module'.format(levelName))
    if hasattr(logging, methodName):
        raise AttributeError('{} already defined in logging module'.format(methodName))
    if hasattr(logging.getLoggerClass(), methodName):
        raise AttributeError('{} already defined in logger class'.format(methodName))

    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(levelNum):
            self._log(levelNum, message, args, **kwargs)
    def logToRoot(message, *args, **kwargs):
        logging.log(levelNum, message, *args, **kwargs)

    logging.addLevelName(levelNum, levelName)
    setattr(logging, levelName, levelNum)
    setattr(logging.getLoggerClass(), methodName, logForLevel)
    setattr(logging, methodName, logToRoot)

addLoggingLevel('TRACE', 5)

FORMAT = '%(filename)s - %(levelname)s - %(funcName)s - %(message)s'

def run():
    app = QApplication([])
    model = ImageListModel()
    view = MainWindow()
    presenter = Presenter(model, view)
    app.exec()

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument(
        '--verbose',
        default=False,
        choices=['info', 'debug', 'trace'],
        help='Set logging level to INFO, DEBUG or TRACE, Default is False'
    )
    args = parser.parse_args()

    if args.verbose:
        if args.verbose == 'info':
            logging.basicConfig(level=logging.INFO, format=FORMAT)
            logging.info('Logger initialized with INFO level')
        elif args.verbose == 'debug':
            logging.basicConfig(level=logging.DEBUG, format=FORMAT)
            logging.info('Logger initialized with DEBUG level')
        elif args.verbose == 'trace':
            logging.basicConfig(level=logging.TRACE, format=FORMAT)
            logging.info('Logger initialized with TRACE level')
    
    run()
