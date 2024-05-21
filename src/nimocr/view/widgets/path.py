import logging
from typing import Optional

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QListWidget, QListWidgetItem

logger = logging.getLogger(__name__)


class PathListWidget(QListWidget):
    """
    PathListWidget is a widget that displays a list of paths.
    User can click on a path to select it.

    Signals:
    --------
        selected_index (int): Signal to emit the selected index.
    """

    selected_index = pyqtSignal(int)

    def __init__(self, paths: Optional[list[str]] = None) -> None:
        """Initialize the PathListWidget."""
        super().__init__()
        self.paths = paths
        self.initUI()

    def initUI(self) -> None:
        """Set up the user interface."""
        if self.paths is not None:
            font = QFont("IBM Plex Sans Thai", 12)
            self.items: list[QListWidgetItem] = []
            for path in self.paths:
                item = QListWidgetItem(path)
                item.setFont(font)
                self.addItem(item)
                self.items.append(item)

            self.itemClicked.connect(self.on_item_clicked)

    def on_item_clicked(self) -> None:
        """Emit the selected_index signal when an item is clicked."""
        logger.info(f"PathListWidget: Selected index: {self.currentRow()}")
        self.selected_index.emit(self.currentRow())

    def remove_item(self, index: int) -> None:
        """Remove an item from the widget."""
        self.takeItem(index)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    # Enable logging
    logging.basicConfig(level=logging.INFO)

    paths = [f"/path/to/file{i}" for i in range(20)]
    widget = PathListWidget(paths)
    widget.show()

    sys.exit(app.exec())
