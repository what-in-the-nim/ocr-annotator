from PyQt6.QtWidgets import QFileDialog


class BrowseFileDialog(QFileDialog):
    """BrowseFileDialog is a file dialog to browse the label file."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Open File")
        self.setDirectory("")
        self.setFileMode(QFileDialog.FileMode.ExistingFile)
        # Filter only csv and tsv files at the same time
        self.setNameFilters(["CSV (*.csv)", "TSV (*.tsv)"])
        self.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        self.setModal(True)
