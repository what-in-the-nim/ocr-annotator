from PyQt6.QtWidgets import QMessageBox


class AboutMessageBox(QMessageBox):
    """
    AboutMessageBox for the application.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About")
        self.setText("OCR Annotator")
        self.setInformativeText("Version 1.0.0, Created by: @what_in_the_nim")
        self.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.setIcon(QMessageBox.Icon.Information)
        self.setModal(True)
