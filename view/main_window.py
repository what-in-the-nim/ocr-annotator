from PyQt6.QtWidgets import QMainWindow, QStatusBar, QSpinBox, QLineEdit
from PyQt6.QtGui import QKeySequence
from PyQt6.QtCore import Qt, pyqtSignal, QEvent

from .widget import AnnotatorWidget
import logging

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    open_selected_file = pyqtSignal(str)
    request_next_image = pyqtSignal()
    request_prev_image = pyqtSignal()
    request_save_file = pyqtSignal()
    request_image_rotate = pyqtSignal()
    request_delete_item = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("OCR Annotator")
        self.resize(800, 600)

        # Set central widget
        self.annotatorWidget = AnnotatorWidget()
        self.setCentralWidget(self.annotatorWidget)

        # Add status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        # Add tool bar
        self.toolBar = self.addToolBar("Tools")
        self.toolBar.setMovable(False)

        # Add load button on tool bar
        self.loadAction = self.toolBar.addAction("Load")
        self.loadAction.setShortcut("Ctrl+O")
        self.loadAction.triggered.connect(self.load_file)

        # Add save button on tool bar
        self.saveAction = self.toolBar.addAction("Save")
        self.saveAction.setShortcut("Ctrl+S")
        self.saveAction.triggered.connect(self.request_save_file.emit)

        # Add seperator line on tool bar
        self.toolBar.addSeparator()

        # Add previous button on tool bar
        self.prevAction = self.toolBar.addAction("Prev")
        self.prevAction.setShortcut(QKeySequence(Qt.Key.Key_Left))  # Set the left arrow key shortcut
        self.prevAction.triggered.connect(self.request_prev_image.emit)

        # Add next button on tool bar
        self.nextAction = self.toolBar.addAction("Next")
        self.nextAction.setShortcut(QKeySequence(Qt.Key.Key_Right))  # Set the right arrow key shortcut
        self.nextAction.triggered.connect(self.request_next_image.emit)

        # Add seperator line on tool bar
        self.toolBar.addSeparator()

        # Add rotate button on tool bar
        self.rotateAction = self.toolBar.addAction("Rotate")
        self.rotateAction.setShortcut("r")
        self.rotateAction.triggered.connect(self.request_image_rotate.emit)

        # Add delete button on tool bar
        self.deleteAction = self.toolBar.addAction("Delete")
        self.deleteAction.setShortcut("Ctrl+D")
        self.deleteAction.triggered.connect(self.request_delete_item.emit)

        self.addToolBar(self.toolBar)
        self.installEventFilter(self)
        self.show()

        logger.info("Main window initialized")

    def load_file(self) -> None:
        """Get a file path with QFileDialog and load the file."""
        logger.info("Launch file dialog")
        # filename, _ = QFileDialog.getOpenFileName(
        #     parent=self, 
        #     caption="Open File", 
        #     directory="", 
        #     filter="CSV file (*.csv)")

        filename = "Medical/labels.csv"
        if filename:
            logger.info(f'File selected: {filename}')
            self.open_selected_file.emit(filename)
        else:
            logger.info('No file is selected')

    def show_message(self, message: str) -> None:
        """Set the status message."""
        self.statusBar.showMessage(message, msecs=2000)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.MouseButtonPress:
            # Check whether the mouse press occurred outside of the spin box
            if not self.childAt(event.pos()) == obj:
                # Clear the focus of the spin box
                self.findChild(QSpinBox).clearFocus()
                self.findChild(QLineEdit).clearFocus()

        return super().eventFilter(obj, event)
