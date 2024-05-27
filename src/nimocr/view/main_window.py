import logging

from PyQt6.QtCore import QEvent, pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QLineEdit, QMainWindow, QMenuBar, QSpinBox, QStatusBar

from .dialogs import FileDialog, SaveDialog, SelectColumnDialog
from .message_boxs import AboutMessageBox
from .widgets import AnnotatorWidget

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    open_selected_file = pyqtSignal(str)
    request_save_file = pyqtSignal()
    request_image_rotate = pyqtSignal(int)
    request_delete_item = pyqtSignal(int)
    request_change_text = pyqtSignal(int, str)
    request_create_file_dialog = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("OCR Annotator")
        self.setWindowIcon(QIcon("assets/logo.png"))
        self.resize(800, 600)
        # Set up widget.
        self.annotatorWidget = AnnotatorWidget()
        self.setCentralWidget(self.annotatorWidget)
        self.setContentsMargins(10, 10, 10, 10)

        self._setup_menubar()
        self._setup_statusbar()
        self._setup_toolbar()

        self.installEventFilter(self)
        self.show()

        logger.info("Main window initialized")

    def _setup_menubar(self) -> None:
        """Add menu bar to the main window."""
        self.menuBar = QMenuBar()
        self.setMenuBar(self.menuBar)

        # Add file menu
        self.fileMenu = self.menuBar.addMenu("File")

        # Add open file action
        self.aboutAction = self.fileMenu.addAction("About")
        self.aboutAction.triggered.connect(AboutMessageBox(self).exec)

    def _setup_statusbar(self) -> None:
        """Add status bar to the main window."""
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

    def _setup_toolbar(self) -> None:
        """Add toolbar to the main window."""
        self.toolBar = self.addToolBar("Tools")
        self.toolBar.setMovable(False)

        # Add load button on tool bar
        self.loadAction = self.toolBar.addAction("Load")
        self.loadAction.setShortcut("Ctrl+O")
        self.loadAction.triggered.connect(self.load_file)

        # Add save button on tool bar
        self.saveAction = self.toolBar.addAction("Save")
        self.saveAction.setShortcut("Ctrl+S")
        self.saveAction.setEnabled(False)
        self.saveAction.triggered.connect(self.request_save_file.emit)

        self.addToolBar(self.toolBar)

    def load_file(self) -> None:
        """Get a file path with QFileDialog and load the file."""
        logger.info("Launch file dialog to browse label file")
        self.request_create_file_dialog.emit()

    def create_select_column_dialog(self, column_names: list[str]) -> tuple[str, str]:
        """Create a select column dialog."""
        logger.info("Launch column dialog to select column inside label")
        # Launch column dialog for user to select the column
        column_dialog = SelectColumnDialog(self, column_names)
        column_dialog.exec()

        # Get the selected column
        path_column = column_dialog.path_column_name
        text_column = column_dialog.text_column_name

        return (path_column, text_column)

    def create_browse_file_dialog(self) -> None:
        """Create a browse file dialog."""
        logger.info("Launch file dialog to browse label file")
        # Launch file dialog for user to browse the file.
        file_dialog = FileDialog(self)
        file_dialog.exec()

        # If no file is selected, return
        if file_dialog.filename is None:
            logger.info("No file is selected")
        else:
            logger.info(f"File selected: {file_dialog.filename}")
            # Request to load the file
            self.open_selected_file.emit(file_dialog.filename)

    def create_save_file_dialog(self, save_path: str) -> str:
        """Create a save file dialog."""
        logger.info("Launch save dialog to select the save path")
        # Launch save file dialog for user to save the file.
        save_dialog = SaveDialog(self, save_path)
        save_dialog.exec()

        logger.info(f"Save path: {save_dialog.save_path}")
        return save_dialog.save_path

    def show_message(self, message: str) -> None:
        """Set the status message."""
        self.statusBar.showMessage(message, msecs=2000)

    def activate_actions(self) -> None:
        """Enable the actions on the toolbar."""
        logger.info("Enable actions on the toolbar")
        self.saveAction.setEnabled(True)

    def eventFilter(self, obj, event):
        """Filter the event of the click event."""
        if event.type() == QEvent.Type.MouseButtonPress:
            # Check whether the mouse press occurred outside of the spin box
            if not self.childAt(event.pos()) == obj:
                # Clear the focus of the spin box
                self.findChild(QSpinBox).clearFocus()
                self.findChild(QLineEdit).clearFocus()

        return super().eventFilter(obj, event)
