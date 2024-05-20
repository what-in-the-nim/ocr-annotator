import logging

import numpy as np
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QVBoxLayout, QListWidget, QWidget

from .item import ItemWidget

logger = logging.getLogger(__name__)


class AnnotatorWidget(QWidget):
    """
    ANnotator widget for displaying images and texts. It contains multiple item widgets.

    Attributes:
    ----------
        item_per_page: The number of items per page.
        item_widgets: The list of item widgets.

    Signals:
    --------
        request_rotate_image (int): Signal to request the rotation of the image.
        request_change_text (int, str): Signal to request the change of the label.
        request_delete_item (int): Signal to request the deletion of the item.

    Methods:
    --------
        set_images(images: np.ndarray) -> None:
            Set the images in the image widgets.
        set_texts(texts: list[str]) -> None:
            Set the texts in the text widgets.
        set_paths(paths: list[str]) -> None:
            Set the paths in the text widgets.
        set_indices(indices: list[int], total: int) -> None:
            Set the index and total in the index label.
    """

    request_rotate_image = pyqtSignal(int)
    request_change_text = pyqtSignal(int, str)
    request_delete_item = pyqtSignal(int)

    def __init__(self, item_per_page: int = 6) -> None:
        super().__init__()
        # Set layout.
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setLayout(layout)

        # Set the item per page
        self.set_item_per_page(item_per_page)
        logger.info("Annotator widget initialized")

    def _create_item_widgets(self) -> None:
        """Create item widgets."""
        self.item_widgets: list[ItemWidget] = list()
        for i in range(self.item_per_page):
            # Create widgets
            widget = ItemWidget()
            self.item_widgets.append(widget)
            self.layout().addWidget(widget, i, alignment=Qt.AlignmentFlag.AlignLeft)

            # Link signals with widget signals
            widget.request_rotate_image.connect(self.request_rotate_image)
            widget.request_change_text.connect(self.request_change_text)
            widget.request_rotate_image.connect(self.request_rotate_image)

    def set_item_per_page(self, item_per_page: int) -> None:
        """Set the number of items per page."""
        self.item_per_page = item_per_page
        self._create_item_widgets()

    def set_images(self, images: np.ndarray) -> None:
        """Set the images in the image widgets."""
        for widget, image in zip(self.item_widgets, images):
            widget.set_image(image)

    def set_texts(self, texts: list[str]) -> None:
        """Set the texts in the text widgets."""
        for widget, text in zip(self.item_widgets, texts):
            widget.set_text(text)

    def set_paths(self, paths: list[str]) -> None:
        """Set the paths in the text widgets."""
        for widget, path in zip(self.item_widgets, paths):
            widget.set_path(path)

    def set_indices(self, indices: list[int], total: int) -> None:
        """Set the index and total in the index label."""
        for index, widget in zip(indices, self.item_widgets):
            widget.set_index(index, total)
