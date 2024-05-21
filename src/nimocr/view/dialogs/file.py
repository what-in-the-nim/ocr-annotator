import logging

from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QDialog, QFormLayout, QHBoxLayout, QLineEdit, QPushButton

from .browse_file import BrowseFileDialog

logger = logging.getLogger(__name__)


class FileDialog(QDialog):
    def __init__(self, parent=None) -> None:
        """Initialize the dialog."""
        super().__init__(parent)
        self.setWindowTitle("Browse File")
        self.filename = None

        hboxlayout = QHBoxLayout()
        self.path_line_edit = QLineEdit()
        self.path_line_edit.setReadOnly(False)
        self.path_line_edit.textChanged.connect(self.on_path_line_edit_text_changed)

        self.browse_button = QPushButton("Browse")
        # Set fixed width to default size
        self.browse_button.setFixedWidth(self.browse_button.sizeHint().width())
        self.browse_button.clicked.connect(self.on_browse_button_clicked)
        hboxlayout.addWidget(self.path_line_edit)
        hboxlayout.addWidget(self.browse_button)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.accept)

        layout = QFormLayout()
        layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        layout.addRow("File Path:", hboxlayout)
        layout.addWidget(self.submit_button)
        self.setLayout(layout)

        default_size = self.sizeHint()
        self.setFixedHeight(default_size.height())
        self.setMinimumWidth(int(default_size.width()))
        self.setMaximumWidth(int(default_size.width() * 1.5))

    @pyqtSlot()
    def on_browse_button_clicked(self) -> None:
        """Open the file dialog to browse label file and set the path to the line edit"""
        logger.info("Browse button clicked")
        file_dialog = BrowseFileDialog()
        if file_dialog.exec():
            selected_file = file_dialog.selectedFiles()[0]
            self.path_line_edit.setText(selected_file)
            self.filename = selected_file

    @pyqtSlot()
    def on_path_line_edit_text_changed(self) -> None:
        """Set the filename when the path line edit text is changed"""
        logger.info("Path line edit text changed")
        self.filename = self.path_line_edit.text()
