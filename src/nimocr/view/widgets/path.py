from PyQt6.QtWidgets import QApplication, QListWidget, QListWidgetItem, QVBoxLayout, QWidget
from PyQt6.QtGui import QFont, QIcon

class PathListWidget(QWidget):
    """
    PathListWidget is a widget that displays a list of paths.
    """

    def __init__(self, paths: list[str]) -> None:
        """Initialize the PathListWidget."""
        super().__init__()
        
        self.paths = paths
        self.initUI()
        
    def initUI(self) -> None:
        """Set up the user interface."""
        layout = QVBoxLayout()
        
        self.list_widget = QListWidget()
        for path in self.paths:
            item = QListWidgetItem(path)
            item.setFont(QFont("Arial", 12))  # Set font
            item.setIcon(QIcon("path/to/icon.png"))  # Set icon if needed
            self.list_widget.addItem(item)
        
        layout.addWidget(self.list_widget)
        self.setLayout(layout)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    
    paths = [f"/path/to/file{i}" for i in range(20)]
    widget = PathListWidget(paths)
    widget.show()
    
    sys.exit(app.exec())
