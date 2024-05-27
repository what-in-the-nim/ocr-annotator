import logging

import numpy as np
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QStyle,
    QVBoxLayout,
    QWidget,
)

from ..message_boxs import ConfirmDeleteMessageBox
from .image import ImageWidget
from .text import TextWidget

logger = logging.getLogger(__name__)


class ItemWidget(QWidget):
    """
    This widget holds a single piece of data, which can be displayed and edited.
    The widget will have a thin black border.

    The rotate button can be used to rotate the image, which place on the top left of the widget.
    The trash button can be used to delete the item at the right of the rotate button.
    The index/total label is placed at the top right of the widget.
    The image widget is placed below both buttons.
    The text widget is placed below the image widget.

    Attributes:
    ----------
        index: The index of the item.

    Signals:
    --------
        request_delete_item (int): Signal to request the deletion of the item.
        request_rotate_image (int): Signal to request the rotation of the image.
        request_change_text (int, str): Signal to request the change of the text.

    Methods:
    --------
        set_image(image: np.ndarray) -> None:
            Set the image in the image widget.
        set_text(text: str) -> None:
            Set the text in the text widget.
        set_path(path: str) -> None:
            Set the path in the text widget.
        set_index(index: int, total: int) -> None:
            Set the index and total in the index label.
    """

    # Send the index of the item to be changed
    request_delete_item = pyqtSignal(int)
    request_rotate_image = pyqtSignal(int)
    request_change_text = pyqtSignal(int, str)

    def __init__(self):
        super().__init__()
        # Set the state of the widget
        self.index = None
        # Make the widget height unchangeable
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.initUI()
        self.disable()

    def initUI(self) -> None:
        """Set up the user interface."""
        item_layout = QVBoxLayout()
        image_layout = QHBoxLayout()

        # Create tool widget.
        tool_widget = QWidget()
        tool_widget.setSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum
        )
        tool_layout = QVBoxLayout()
        # Create path label
        font = QFont("IBM Plex Sans Thai", 12)
        self.path_label = QLabel()
        self.path_label.setFont(font)
        item_layout.addWidget(self.path_label)

        # Create rotate button from logo
        self.rotate_button = QPushButton()
        self.rotate_button.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        rotate_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload)
        self.rotate_button.setIcon(rotate_icon)
        self.rotate_button.clicked.connect(self._rotate_image)
        tool_layout.addWidget(self.rotate_button)

        # Create trash button from logo
        self.trash_button = QPushButton()
        self.trash_button.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        trash_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_TrashIcon)
        self.trash_button.setIcon(trash_icon)
        self.trash_button.clicked.connect(self._delete_item)
        tool_layout.addWidget(self.trash_button)

        # Create index/total label
        self.index_label = QLabel("-")
        self.index_label.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        tool_layout.addWidget(self.index_label)
        tool_layout.addStretch()
        tool_widget.setLayout(tool_layout)

        image_layout.addWidget(tool_widget)

        # Create image and text widgets
        self.image_widget = ImageWidget()
        image_layout.addWidget(self.image_widget)
        item_layout.addLayout(image_layout)

        self.text_widget = TextWidget()
        self.text_widget.request_change_text.connect(self._change_text)
        item_layout.addWidget(self.text_widget)

        self.setLayout(item_layout)

    def _delete_item(self) -> None:
        """Emit the request_delete_item signal."""
        confirm_dialog = ConfirmDeleteMessageBox(self)
        result = confirm_dialog.exec()

        if result == QMessageBox.StandardButton.Yes:
            logger.info(f"Delete item request sent for index: {self.index}")
            self.request_delete_item.emit(self.index)

    def _rotate_image(self) -> None:
        """Emit the request_image_rotate signal."""
        logger.info("Rotate image request sent")
        self.request_rotate_image.emit(self.index)

    def _change_text(self, text: str) -> None:
        """Emit the request_change_text signal."""
        logger.info("Change text request sent")
        self.request_change_text.emit(self.index, text)

    def set_image(self, image: np.ndarray) -> None:
        """Set the image in the image widget."""
        self.image_widget.set_image(image)

    def set_text(self, text: str) -> None:
        """Set the text in the text widget."""
        self.text_widget.setText(text)

    def set_path(self, path: str) -> None:
        """Set the path in the image widget."""
        self.image_widget.set_path(path)
        self.path_label.setText(path)

    def set_index(self, index: int) -> None:
        """Set the index and total in the index label."""
        self.index = index
        self.index_label.setText(f"{index}")

    def set_empty(self) -> None:
        """Set the widget to be empty."""
        self.image_widget.set_empty()
        self.text_widget.setText("")
        self.path_label.setText("")
        self.index_label.setText("-")

    def disable(self) -> None:
        """Set the widget to be disabled."""
        self.rotate_button.setEnabled(False)
        self.trash_button.setEnabled(False)
        self.text_widget.disable()

    def enable(self) -> None:
        """Set the widget to be enabled."""
        self.rotate_button.setEnabled(True)
        self.trash_button.setEnabled(True)
        self.text_widget.enable()


if __name__ == "__main__":
    import sys

    from PyQt6.QtWidgets import QApplication, QVBoxLayout

    app = QApplication(sys.argv)
    widget = ItemWidget()
    widget.show()
    sys.exit(app.exec())
