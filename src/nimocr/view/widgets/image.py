import logging

from PIL import Image
from PyQt6.QtCore import QMimeData, QPoint, Qt
from PyQt6.QtGui import QAction, QImage, QPixmap, QResizeEvent
from PyQt6.QtWidgets import QApplication, QLabel, QMenu, QMessageBox, QSizePolicy

from ...model import ImageHandler

logger = logging.getLogger(__name__)


class ImageWidget(QLabel):
    """
    ImageWidget for displaying images.

    Attributes:
    ----------
        image: The image to be displayed.
        path: The path of the image.
    """

    def __init__(self):
        super(ImageWidget, self).__init__()
        self.image = None
        self.path = None
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setContentsMargins(5, 5, 5, 5)
        self.setStyleSheet("border: 1px solid black;")

        # Set right click menu
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showMenu)

        logger.info("Image widget initialized")

    def showMenu(self, pos: QPoint) -> None:
        """Show the right click menu."""
        logger.info(f"Image widget received right click at {pos}")
        # Create the menu
        menu = QMenu(self)
        # Create copy action
        copy_action = QAction("Copy Image", self)
        copy_action.triggered.connect(self.copy_image)
        # Create open property action
        open_property_action = QAction("Properties", self)
        open_property_action.triggered.connect(self.open_property)
        # Add copy action to the menu
        menu.addAction(copy_action)
        # Add open property action to the menu
        menu.addAction(open_property_action)
        # Show the menu
        menu.exec(self.mapToGlobal(pos))

    def copy_image(self) -> None:
        """Copy the image to the clipboard."""
        logger.info("Image widget received copy image request")
        data = QMimeData()
        data.setImageData(self.pixmap().toImage())
        clipboard = QApplication.clipboard()
        clipboard.setMimeData(data)

    def set_image(self, image: Image.Image) -> None:
        """Set the image in the imageWidget."""
        logger.info("Image widget received image")
        self.image = image
        self.update_image()

    def set_path(self, path: str) -> None:
        """Set the path of the image."""
        logger.info("Image widget received path")
        self.path = path

    def open_property(self) -> None:
        """Open propery dialog and show the path when right click on the image"""
        logger.info("Image widget received open property request")
        # Create message box
        msg = QMessageBox()
        msg.setWindowTitle("Image Properties")
        msg.setText(f"Path: {self.path}")
        msg.exec()

    def update_image(self) -> None:
        """Update the image in the imageWidget."""
        if self.image is None:
            return

        container_size = (self.width(), self.height())
        self.image = ImageHandler.fit(self.image, container_size)

        # Create a QImage from the padded image data
        width, height = self.image.size

        qImg = QImage(
            self.image.tobytes(),
            width,
            height,
            3 * width,
            QImage.Format.Format_RGB888,
        )
        pixmap = QPixmap.fromImage(qImg)
        self.setPixmap(pixmap)
