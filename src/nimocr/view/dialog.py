import logging
from typing import List

from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMessageBox,
    QPushButton,
)

logger = logging.getLogger(__name__)


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
        # Filter only csv and tsv files at the same time
        self.setNameFilters(["CSV (*.csv),TSV (*.tsv)"])
        self.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        self.setModal(True)


class SelectColumnDialog(QDialog):
    """
    SelectColumnDialog is a dialog to select the path and text column name.
    The structure consists of two labels and two combo boxes. When initialized, all
    the column names need to be passed to the dialog.
    At first, all combo boxes will have all the column names. When the user selects
    a column name in one of the combo boxes, the other combo box will remove the
    selected column name. If user changes the selected column name in one of the
    combo boxes, the other combo box will add the previously selected column name
    back to the list. The choice of the column names will be saved in the dialog
    and can be accessed by the path_column_name and text_column_name attributes.
    """

    def __init__(self, parent=None, column_names: List[str] = None):
        super().__init__(parent)
        self.setWindowTitle("Select Column")
        self.column_names = column_names
        self.path_column_name = None
        self.text_column_name = None

        self.path_combo_box = QComboBox()
        self.path_combo_box.addItems(self.column_names)
        self.path_combo_box.activated.connect(
            self.on_path_combo_box_current_index_changed
        )

        self.text_combo_box = QComboBox()
        self.text_combo_box.addItems(self.column_names)
        self.text_combo_box.activated.connect(
            self.on_text_combo_box_current_index_changed
        )

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.accept)

        layout = QFormLayout()
        layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        layout.addRow("Path Column:", self.path_combo_box)
        layout.addRow("Text Column:", self.text_combo_box)
        layout.addWidget(self.submit_button)
        self.setLayout(layout)

        # Set the default column names
        self.path_column_name = self.column_names[0]
        self.text_column_name = self.column_names[1]
        self.path_combo_box.setCurrentText(self.column_names[0])
        self.text_combo_box.setCurrentText(self.column_names[1])

    @pyqtSlot()
    def on_path_combo_box_current_index_changed(self) -> None:
        """Remove the selected column name from the text combo box."""
        logger.info("Path combo box current index changed")
        self.path_column_name = self.path_combo_box.currentText()

        # Check if the text is the same as the path
        current_text = self.text_combo_box.currentText()
        if current_text == self.path_column_name:
            # If the text is the same as the path, select the next item
            next_index = self.text_combo_box.currentIndex() + 1
            next_index %= self.text_combo_box.count()
            self.text_combo_box.setCurrentIndex(next_index)

    @pyqtSlot()
    def on_text_combo_box_current_index_changed(self) -> None:
        """Remove the selected column name from the path combo box."""
        logger.info("Text combo box current index changed")
        self.text_column_name = self.text_combo_box.currentText()

        # Check if the path is the same as the text
        current_text = self.path_combo_box.currentText()
        if current_text == self.text_column_name:
            # If the path is the same as the text, select the next item
            next_index = self.path_combo_box.currentIndex() + 1
            next_index %= self.path_combo_box.count()
            self.path_combo_box.setCurrentIndex(next_index)


class FileDialog(QDialog):
    def __init__(self, parent=None) -> None:
        """Initialize the dialog."""
        super().__init__(parent)
        self.setWindowTitle("Browse File")
        self.filename = None

        hboxlayout = QHBoxLayout()
        self.path_line_edit = QLineEdit()
        self.path_line_edit.setReadOnly(False)

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


class SaveDialog(QDialog):
    """SaveDialog has a line_edit which will set a default file path to save.
    This path is given when initialized. If user edit and press the submit button,
    the save_path will be saved in the dialog's attribute..
    """

    def __init__(self, parent=None, default_path: str = None):
        """Initialize the dialog."""
        super().__init__(parent)
        self.setWindowTitle("Save File")
        self.save_path = default_path

        self.path_line_edit = QLineEdit()
        self.path_line_edit.setText(default_path)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.accept)

        layout = QFormLayout()
        layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        layout.addRow("Save Path:", self.path_line_edit)
        layout.addWidget(self.submit_button)
        self.setLayout(layout)

        default_size = self.sizeHint()
        self.setFixedHeight(default_size.height())
        self.setMinimumWidth(int(default_size.width()))
        self.setMaximumWidth(int(default_size.width() * 1.5))

    def accept(self) -> None:
        """Set the save_path and close the dialog."""
        logger.info("Save dialog accepted")
        self.save_path = self.path_line_edit.text()
        super().accept()


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
