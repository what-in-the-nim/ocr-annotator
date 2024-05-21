import logging

from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QComboBox, QDialog, QFormLayout, QPushButton

logger = logging.getLogger(__name__)


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

    def __init__(self, parent=None, column_names: list[str] = None):
        super().__init__(parent)
        self.setWindowTitle("Select Column")
        self.column_names = column_names
        self.path_column_name = None
        self.text_column_name = None

        self.path_combo_box = QComboBox()
        self.path_combo_box.addItems(self.column_names)
        self.path_combo_box.activated.connect(self.on_path_combo_box_current_index_changed)

        self.text_combo_box = QComboBox()
        self.text_combo_box.addItems(self.column_names)
        self.text_combo_box.activated.connect(self.on_text_combo_box_current_index_changed)

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
