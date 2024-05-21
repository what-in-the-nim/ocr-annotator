from PyQt6.QtWidgets import QMessageBox


class ConfirmDeleteMessageBox(QMessageBox):
    """ConfirmDeleteMessageBox is a dialog to confirm the deletion of an item."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Confirm Delete")
        self.setText("Are you sure you want to delete this item?")
        self.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        self.setDefaultButton(QMessageBox.StandardButton.No)
        self.setIcon(QMessageBox.Icon.Question)
        self.setModal(True)
