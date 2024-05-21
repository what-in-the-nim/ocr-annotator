import logging

import numpy as np
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QLayout, QSplitter, QVBoxLayout, QWidget, QSizePolicy

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
        request_update_items (list): Signal to request the update of the items.

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
    request_update_items = pyqtSignal(list)

    def __init__(self, item_per_page: int = 4) -> None:
        super().__init__()
        # Set the item per page
        self.item_per_page = item_per_page
        # Set layout.
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setLayout(layout)

        self.initUI()
        self.link_signals()

        logger.info("Annotator widget initialized")

    def initUI(self) -> None:
        """Initialize the user interface."""
        # Add splitter into the layout
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.layout().addWidget(self.splitter)

        # Add widgets to the right side of the splitter.
        item_widget = QWidget()
        item_widget_layout = QVBoxLayout()
        ## Add item widgets to item_widget_layout
        self.item_widgets: list[ItemWidget] = list()
        for i in range(self.item_per_page):
            # Create item widgets
            widget = ItemWidget()
            # Link signals with widget signals
            widget.request_rotate_image.connect(self.request_rotate_image.emit)
            widget.request_change_text.connect(self.request_change_text.emit)
            widget.request_delete_item.connect(self.request_delete_item.emit)
            self.item_widgets.append(widget)
            item_widget_layout.addWidget(widget, i)

        ## Add page widget to item_widget_layout
        self.page_widget = PageWidget(self.item_per_page)
        self.page_widget.setFixedHeight(50)
        item_widget_layout.addWidget(self.page_widget)
        ## Set stretch factor for item_widget_layout
        for i in range(self.item_per_page):
            item_widget_layout.setStretch(i, 1)

        item_widget.setLayout(item_widget_layout)

        # Add path list widget to the left side of the splitter
        self.path_list_widget = PathListWidget()
        self.path_list_widget.setMinimumWidth(200)
        self.path_list_widget.setMaximumWidth(500)
        self.path_list_widget.selected_index.connect(self.page_widget.go_to_index)

        self.splitter.addWidget(self.path_list_widget)
        self.splitter.addWidget(item_widget)

        # Set the stretch factor
        # The left to right ratio is 1:3
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 3)

    def link_signals(self) -> None:
        """Link signals with widget signals."""
        self.page_widget.request_update_items.connect(self.request_update_items)

    def set_total_items(self, total: int) -> None:
        """Set the total number of items."""
        self.page_widget.set_total_items(total)

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

    def disable(self) -> None:
        """Disable the widget."""
        self.path_list_widget.disable()
        self.page_widget.disable()
        for widget in self.item_widgets:
            widget.disable()

    def enable(self) -> None:
        """Enable the widget."""
        self.path_list_widget.enable()
        self.page_widget.enable()
        for widget in self.item_widgets:
            widget.enable()
