import logging

import numpy as np
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QLayout, QSplitter, QVBoxLayout, QWidget

from .item import ItemWidget
from .page import PageWidget
from .path import PathListWidget

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

    def __init__(self, item_per_page: int = 4) -> None:
        super().__init__()
        # Set layout.
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setLayout(layout)

        # Set the item per page
        self.set_item_per_page(item_per_page)
        logger.info("Annotator widget initialized")

        self.initUI()

    def initUI(self) -> None:
        """Initialize the user interface."""
        # Add splitter into the layout
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.layout().addWidget(self.splitter)

        # Add path list widget to the left side of the splitter
        self.path_list_widget = PathListWidget()
        self.path_list_widget.setMinimumWidth(200)
        self.path_list_widget.setMaximumWidth(500)
        self.splitter.addWidget(self.path_list_widget)

        # Add widgets to the right side of the splitter.
        item_widget = QWidget()
        item_widget_layout = QVBoxLayout()
        ## Add item widgets to item_widget_layout
        self.item_widgets: list[ItemWidget] = list()
        for i in range(self.item_per_page):
            # Create item widgets
            widget = ItemWidget()
            self.item_widgets.append(widget)
            item_widget_layout.addWidget(widget, i)

            # Link signals with widget signals
            widget.request_rotate_image.connect(self.request_rotate_image)
            widget.request_change_text.connect(self.request_change_text)
            widget.request_rotate_image.connect(self.request_rotate_image)

        ## Add page widget to item_widget_layout
        self.page_widget = PageWidget(self.item_per_page, 0)
        self.page_widget.setFixedHeight(50)
        item_widget_layout.addWidget(self.page_widget)
        for i in range(self.item_per_page):
            item_widget_layout.setStretch(i, 1)

        item_widget.setLayout(item_widget_layout)
        self.splitter.addWidget(item_widget)

        # Set the stretch factor
        # The left to right ratio is 1:3
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 3)

    def set_item_per_page(self, item_per_page: int) -> None:
        """Set the number of items per page."""
        self.item_per_page = item_per_page

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
