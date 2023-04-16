from PyQt6.QtWidgets import (
    QMessageBox,
    QFileDialog,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QDialog,
)
from PyQt6.QtCore import pyqtSignal, pyqtSlot
import os

class ConfirmDeleteDialog(QMessageBox):
    """ConfirmDeleteDialog is a dialog to confirm the deletion of an item."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Confirm Delete")
        self.setText("Are you sure you want to delete this item?")
        self.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        self.setDefaultButton(QMessageBox.StandardButton.No)
        self.setIcon(QMessageBox.Icon.Question)
        self.setModal(True)


class BrowseFileDialog(QFileDialog):
    """BrowseFileDialog is a file dialog to browse the label file."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Open File")
        self.setDirectory("")
        self.setFileMode(QFileDialog.FileMode.ExistingFile)
        self.setNameFilter("CSV file (*.csv)")
        self.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        self.setModal(True)


class BrowseDirectoryDialog(QFileDialog):
    """BrowseDirectoryDialog is a file dialog to browse the directory."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Open Directory")
        self.setDirectory("")
        self.setFileMode(QFileDialog.FileMode.Directory)
        self.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        self.setModal(True)

    def accept(self) -> None:
        """Override the accept method to emit the signal."""
        os.chdir(self.selectedFiles()[0])
        return super().accept()


class FileDialog(QDialog):
    change_path_column_name = pyqtSignal(str)
    change_text_column_name = pyqtSignal(str)

    def __init__(
        self, path_column_name: str, text_column_name: str, parent=None
    ) -> None:
        """Initialize the dialog."""
        super().__init__(parent)
        self.setWindowTitle("Browse File")

        self.path_line_edit = QLineEdit()
        self.path_line_edit.setReadOnly(True)

        self.browse_button = QPushButton("Browse")
        # Set fixed width to default size
        self.browse_button.setFixedWidth(self.browse_button.sizeHint().width())
        self.browse_button.clicked.connect(self.on_browse_button_clicked)

        self.path_column_line_edit = QLineEdit()
        self.path_column_line_edit.setText(path_column_name)
        self.path_column_line_edit.textChanged.connect(
            self.change_path_column_name.emit
        )
        self.text_column_line_edit = QLineEdit()
        self.text_column_line_edit.setText(text_column_name)
        self.text_column_line_edit.textChanged.connect(
            self.change_text_column_name.emit
        )

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.accept)

        layout = QFormLayout()
        layout.setFieldGrowthPolicy(
            QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow
        )
        layout.addRow("File Path:", self.path_line_edit)
        layout.addWidget(self.browse_button)
        layout.addRow("Path Column Name:", self.path_column_line_edit)
        layout.addRow("Text Column Name:", self.text_column_line_edit)
        layout.addWidget(self.submit_button)
        self.setLayout(layout)

    @pyqtSlot()
    def on_browse_button_clicked(self) -> None:
        """Open the file dialog to browse label file and set the path to the line edit"""
        file_dialog = BrowseFileDialog()
        if file_dialog.exec():
            selected_file = file_dialog.selectedFiles()[0]
            self.path_line_edit.setText(selected_file)

    def update_path_column_name(self, name: str) -> None:
        """Update the path column name in the line edit"""
        self.path_column_line_edit.setText(name)

    def update_text_column_name(self, name: str) -> None:
        """Update the text column name in the line edit"""
        self.text_column_line_edit.setText(name)


class AboutDialog(QMessageBox):
    """
    About dialog for the application.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About")
        self.setText("OCR Annotator")
        self.setInformativeText("Version 1.0.0, Created by: @what_in_the_nim")
        self.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.setIcon(QMessageBox.Icon.Information)
        self.setModal(True)
