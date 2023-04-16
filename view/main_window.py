from PyQt6.QtWidgets import (
    QMainWindow,
    QStatusBar,
    QSpinBox,
    QLineEdit,
    QMessageBox,
    QMenuBar,
    QToolButton,
    QMenu,
)
from PyQt6.QtGui import QKeySequence, QIcon
from PyQt6.QtCore import Qt, pyqtSignal, QEvent

from .dialog import (
    ConfirmDeleteDialog,
    BrowseDirectoryDialog,
    AboutDialog,
    FileDialog,
)
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
    request_change_text_column_name = pyqtSignal(str)
    request_change_path_column_name = pyqtSignal(str)
    request_create_file_dialog = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("OCR Annotator")
        self.setWindowIcon(QIcon("assets/logo.png"))
        self.resize(800, 600)

        # Set central widget
        self.annotatorWidget = AnnotatorWidget()
        self.setCentralWidget(self.annotatorWidget)

        self._setup_menubar()
        self._setup_statusbar()
        self._setup_toolbar()

        self.installEventFilter(self)
        self.show()

        logger.info("Main window initialized")

    def _setup_menubar(self) -> None:
        self.menuBar = QMenuBar()
        self.setMenuBar(self.menuBar)

        # Add file menu
        self.fileMenu = self.menuBar.addMenu("File")

        # Add open file action
        self.aboutAction = self.fileMenu.addAction("About")
        self.aboutAction.triggered.connect(AboutDialog(self).exec)

        # Add browse directory action
        self.browseAction = self.fileMenu.addAction("Browse Directory")
        self.browseAction.triggered.connect(BrowseDirectoryDialog(self).exec)

    def _setup_statusbar(self) -> None:
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

    def _setup_toolbar(self) -> None:
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

        # Add seperator line on tool bar
        self.toolBar.addSeparator()

        # Add previous button on tool bar
        self.prevAction = self.toolBar.addAction("Prev")
        self.prevAction.setShortcut(
            QKeySequence(Qt.Key.Key_Left)
        )  # Set the left arrow key shortcut
        self.prevAction.setEnabled(False)
        self.prevAction.triggered.connect(self.request_prev_image.emit)

        # Add next button on tool bar
        self.nextAction = self.toolBar.addAction("Next")
        self.nextAction.setShortcut(
            QKeySequence(Qt.Key.Key_Right)
        )  # Set the right arrow key shortcut
        self.nextAction.setEnabled(False)
        self.nextAction.triggered.connect(self.request_next_image.emit)

        # Add seperator line on tool bar
        self.toolBar.addSeparator()

        # Add rotate button on tool bar
        self.rotateAction = self.toolBar.addAction("Rotate")
        self.rotateAction.setShortcut("r")
        self.rotateAction.setEnabled(False)
        self.rotateAction.triggered.connect(self.request_image_rotate.emit)

        # Add delete button on tool bar
        self.deleteAction = self.toolBar.addAction("Delete")
        self.deleteAction.setShortcut("Ctrl+D")
        self.deleteAction.setEnabled(False)
        self.deleteAction.triggered.connect(self.confirm_delete)

        # Add sort button menu on tool bar

        # Create sort order menu
        self.sortOrderMenu = QMenu("Order", self)
        self.ascending_action = self.sortOrderMenu.addAction("Ascending")
        self.descending_action = self.sortOrderMenu.addAction("Descending")
        self.sortOrderToolButton = QToolButton()
        self.sortOrderToolButton.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.sortOrderToolButton.setMenu(self.sortOrderMenu)

        # Create sort by menu
        self.sortByMenu = QMenu("By", self)
        self.text_action = self.sortByMenu.addAction("Text")
        self.path_action = self.sortByMenu.addAction("Path")
        self.sortByToolButton = QToolButton()
        self.sortByToolButton.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.sortByToolButton.setMenu(self.sortByMenu)

        # Create main sort menu
        self.sortMenu = QMenu("Sort", self)
        self.sortMenu.addMenu(self.sortOrderMenu)
        self.sortMenu.addMenu(self.sortByMenu)
        self.sortToolButton = QToolButton()
        self.sortToolButton.setText("Sort")
        self.sortToolButton.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.sortToolButton.setMenu(self.sortMenu)

        # Add sort button on tool bar
        self.sortAction = self.toolBar.addWidget(self.sortToolButton)
        self.sortAction.setEnabled(False)

        self.addToolBar(self.toolBar)

    def confirm_delete(self) -> None:
        """Show a confirm dialog before deleting the item."""
        confirm_dialog = ConfirmDeleteDialog(self)
        result = confirm_dialog.exec()

        if result == QMessageBox.StandardButton.Yes:
            self.request_delete_item.emit()

    def load_file(self) -> None:
        """Get a file path with QFileDialog and load the file."""
        logger.info("Launch file dialog")
        self.request_create_file_dialog.emit()

    def create_file_dialog(self, path_column_name: str, text_column_name: str) -> None:
        """Create a file dialog."""
        dialog = FileDialog(path_column_name, text_column_name, parent=self)
        dialog.change_path_column_name.connect(
            self.request_change_path_column_name.emit
        )
        dialog.change_text_column_name.connect(
            self.request_change_text_column_name.emit
        )
        dialog.exec()

        filename = dialog.selected_file

        if filename:
            logger.info(f"File selected: {filename}")
            self.open_selected_file.emit(filename)
            self.activate_actions()
        else:
            logger.info("No file is selected")

    def show_message(self, message: str) -> None:
        """Set the status message."""
        self.statusBar.showMessage(message, msecs=2000)

    def activate_actions(self) -> None:
        """Enable the actions on the toolbar."""
        self.saveAction.setEnabled(True)
        self.prevAction.setEnabled(True)
        self.nextAction.setEnabled(True)
        self.rotateAction.setEnabled(True)
        self.deleteAction.setEnabled(True)
        self.sortAction.setEnabled(True)

    def eventFilter(self, obj, event):
        """Filter the event of the click event."""
        if event.type() == QEvent.Type.MouseButtonPress:
            # Check whether the mouse press occurred outside of the spin box
            if not self.childAt(event.pos()) == obj:
                # Clear the focus of the spin box
                self.findChild(QSpinBox).clearFocus()
                self.findChild(QLineEdit).clearFocus()

        return super().eventFilter(obj, event)
