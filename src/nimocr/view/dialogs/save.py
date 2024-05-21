import logging

from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton

logger = logging.getLogger(__name__)


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
