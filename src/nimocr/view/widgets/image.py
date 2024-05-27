import logging
from typing import Optional

from PIL import Image
from PyQt6.QtCore import QEvent, QMimeData, QPoint, Qt
from PyQt6.QtGui import QAction, QImage, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMenu,
    QMessageBox,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

logger = logging.getLogger(__name__)


class ImageWidget(QWidget):
    """
    ImageWidget for displaying images.

    Attributes:
    ----------
        image: The image to be displayed.
        path: The path of the image.
    """

    def __init__(
        self, image: Optional[Image.Image] = None, path: Optional[str] = None
    ) -> None:
        super(ImageWidget, self).__init__()
        self._label = QLabel(self)
        self.image = image
        self.path = path
        # self.setStyleSheet("border: 1px solid black;")
        self._label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding
        )
        # Set right click menu
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_menu)

        layout = QVBoxLayout()
        layout.addWidget(self._label)
        self.setLayout(layout)

        logger.info("Image widget initialized")

    def set_image(self, image: Image.Image) -> None:
        """Set the image in the imageWidget."""
        logger.info("Image widget received image")
        self.image = image.convert("RGB")

        qImg = QImage(
            image.tobytes(),
            image.width,
            image.height,
            image.width * 3,  # Assuming RGB
            QImage.Format.Format_RGB888,
        )
        pixmap = QPixmap.fromImage(qImg)
        self._label.setPixmap(pixmap)
        self._update_image()

    def set_path(self, path: str) -> None:
        """Set the path of the image."""
        logger.info("Image widget received path")
        self.path = path

    def _show_menu(self, pos: QPoint) -> None:
        """Show the right click menu."""
        logger.info(f"Image widget received right click at {pos}")
        # Create the menu
        menu = QMenu(self)
        # Create copy action
        copy_action = QAction("Copy Image", self)
        copy_action.triggered.connect(self._copy_image)
        # Create open property action
        open_property_action = QAction("Properties", self)
        open_property_action.triggered.connect(self._open_property)
        # Add copy action to the menu
        menu.addAction(copy_action)
        # Add open property action to the menu
        menu.addAction(open_property_action)
        # Show the menu
        menu.exec(self.mapToGlobal(pos))

    def _copy_image(self) -> None:
        """Copy the image to the clipboard."""
        logger.info("Image widget received copy image request")
        data = QMimeData()
        data.setImageData(self._label.pixmap().toImage())
        clipboard = QApplication.clipboard()
        clipboard.setMimeData(data)

    def _open_property(self) -> None:
        """Open propery dialog and show the path when right click on the image"""
        logger.info("Image widget received open property request")
        # Create message box
        msg = QMessageBox()
        msg.setWindowTitle("Image Properties")
        msg.setText(f"Path: {self.path}")
        msg.exec()

    def _update_image(self) -> None:
        """Update the image in the imageWidget."""
        if self.image is None:
            return

        # Resize pixmap to fit the label
        pixmap = self._label.pixmap()
        width, height = self._label.width(), self._label.height()
        scaled_pixmap = pixmap.scaled(
            width - 5,
            max(height - 5, 5),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self._label.setPixmap(scaled_pixmap)

    def resizeEvent(self, event: QEvent) -> None:
        """Handle the resize event."""
        logger.info("Image widget resized")
        self._update_image()
        super().resizeEvent(event)

    def set_empty(self) -> None:
        """Set the widget to be empty."""
        logger.info("Image widget set to empty")
        self.image = Image.new("RGB", (10, 10), (255, 255, 255))
        self._label.clear()


if __name__ == "__main__":
    import sys

    from PyQt6.QtWidgets import QApplication, QMainWindow

    app = QApplication(sys.argv)
    window = QMainWindow()
    image_widget = ImageWidget()
    image = Image.new("RGB", (100, 100), (255, 0, 255))
    image_widget.set_image(image)
    window.setCentralWidget(image_widget)
    window.show()
    sys.exit(app.exec())
