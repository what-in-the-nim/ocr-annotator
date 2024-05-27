import logging

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QSpinBox, QStyle, QWidget

logger = logging.getLogger(__name__)


class PageWidget(QWidget):
    """
    PageWidget is a widget that displays a button to navigate to the previous page or the next page.
    The widget also displays the item per page, current page, and total page.
    The widget accepts total items and items per page as arguments and it will act as the controller
    to navigate through the pages.
    The left-most button is a spinbox that allows the user to change the items per page.
    The center widget is a group of two buttons that allows the user to navigate to the previous page or the next page.
    The right-most widget is a spinbox of the current page/the total page and a label of the total items.

    Attributes:
    ----------
        indices: list[int]
            The indices of the items in the current page.
        total_items: int
            The total items in the list.
        items_per_page: int
            The number of items per page.
        current_page: int
            The current page.

    Methods:
    --------
        set_total_items(total_items: int) -> None:
            Set the total items.
        set_items_per_page(items_per_page: int) -> None:
            Set the items per page.
        go_to_page(page: int) -> None:
            Go to the specified page.
        next_page() -> None:
            Go to the next page.
        prev_page() -> None:
            Go to the previous page.
    """

    request_update_items = pyqtSignal(list)

    def __init__(self, items_per_page: int, total_items: int = 0) -> None:
        """Initialize the PageWidget."""
        super().__init__()
        self.items_per_page = items_per_page
        self.total_items = total_items

        self.current_page = 1
        self._page = []

        if self.total_items > 0 and self.items_per_page > 0:
            self.reset_indices()

        self.initUI()
        self.disable()

        logger.info("PageWidget initialized")

    def reset_indices(self) -> list[list[int]]:
        """Return the indices of the items in each page."""
        indices = []
        for i in range(0, self.total_items, self.items_per_page):
            indices.append(
                list(range(i, min(i + self.items_per_page, self.total_items)))
            )
        self._page = indices
        logger.info(f"Indices: {self._page}")

    def initUI(self) -> None:
        """Set up the user interface."""
        layout = QHBoxLayout()
        layout.setSpacing(0)

        # Set up previous page button.
        self.prev_page_button = QPushButton()
        self.prev_page_button.setFixedWidth(30)
        self.prev_page_button.setFixedHeight(30)
        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowBack)
        self.prev_page_button.setIcon(icon)
        self.prev_page_button.clicked.connect(self.prev_page)

        # Set up next page button.
        self.next_page_button = QPushButton()
        self.next_page_button.setFixedWidth(30)
        self.next_page_button.setFixedHeight(30)
        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowForward)
        self.next_page_button.setIcon(icon)
        self.next_page_button.clicked.connect(self.next_page)

        # Set up current page spinbox
        self.page_spinbox = QSpinBox()
        self.page_spinbox.setRange(1, self.total_pages)
        self.page_spinbox.setValue(1)
        self.page_spinbox.setFixedWidth(50)
        self.page_spinbox.setFixedHeight(30)
        self.page_spinbox.valueChanged.connect(self._handle_spinbox)

        # Set up total page label
        self.total_page_label = QLabel(f"/{self.total_pages}")

        # Add all widgets to the layout
        layout.addStretch()
        layout.addWidget(self.prev_page_button, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.page_spinbox)
        layout.addWidget(self.total_page_label)
        layout.addWidget(self.next_page_button, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addStretch()

        self.setLayout(layout)

    @property
    def indices(self) -> list[int]:
        """Return the indices."""
        return self._page[self.current_page - 1]

    @property
    def total_pages(self) -> int:
        """Return the total pages."""
        return len(self._page)

    def _handle_spinbox(self, text: str) -> None:
        """Handle spinbox text value before emitting the signal."""
        page = int(text)
        self.go_to_page(page)
        logger.info(f"Page spinbox value changed to {page}")

    def set_total_items(self, total_items: int) -> None:
        """Set the total items."""
        # Update the total items
        self.total_items = total_items

    def update_label(self) -> None:
        # Update the label and spinbox
        self.total_page_label.setText(f"/{self.total_pages}")
        self.page_spinbox.setRange(1, self.total_pages)

        # Ensure the current page is within the valid range
        if self.current_page > self.total_pages and self.total_pages > 0:
            self.current_page = self.total_pages

        # Update the page spinbox value
        self.page_spinbox.setValue(self.current_page)

        logger.info(f"Total items: {self.total_items}")
        logger.info(f"Total pages: {self.total_pages}")
        logger.info(f"Current page: {self.current_page}")

    def go_to_page(self, page: int) -> None:
        """Go to the specified page."""
        if 1 <= page <= self.total_pages:
            self.current_page = page
            # Request to update items
            self.request_update_items.emit(self.indices)

            logger.info(f"Go to page {page}")
            logger.info(f"Current page: {self.current_page}")
            logger.info(f"Indices: {self.indices}")

    def go_to_index(self, index: int) -> None:
        """Go to the page that contains the specified index."""
        # Find which page contains the index
        page_index = None
        for i, page in enumerate(self._page):
            if index in page:
                page_index = i
                break
        self.current_page = page_index + 1
        self.page_spinbox.setValue(self.current_page)
        # Update indices and request to update items
        self.request_update_items.emit(self.indices)

    def remove_index(self, index_to_remove: int) -> None:
        """Remove the index from the page and shift the indices."""
        logger.info(f"Removing index {index_to_remove}")
        logger.info(f"Pages: {self._page}")
        # Flatten the list of pages into a single list
        flat_list = [item for sublist in self._page for item in sublist]

        # Remove the specified index
        flat_list.remove(index_to_remove)

        # Reshape the list back into pages
        new_pages = []
        for i in range(0, len(flat_list), self.items_per_page):
            new_pages.append(flat_list[i : i + self.items_per_page])

        # Remove empty page if it exists at the end
        if new_pages and not new_pages[-1]:
            new_pages.pop()

        self._page = new_pages
        # Make sure the current page is within the valid range
        if self.current_page > self.total_pages:
            self.current_page = self.total_pages
            self.page_spinbox.setValue(self.current_page)
            self.update_label()

        logger.info(f"Pages after removing index: {self._page}")

    def next_page(self) -> None:
        """Go to the next page."""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.page_spinbox.setValue(self.current_page)
            # Update indices and request to update items
            self.request_update_items.emit(self.indices)

            logger.info("Next page button clicked")
            logger.info(f"Current page: {self.current_page}")
            logger.info(f"Indices: {self.indices}")

    def prev_page(self) -> None:
        """Go to the previous page."""
        if self.current_page > 1:
            self.current_page -= 1
            self.page_spinbox.setValue(self.current_page)
            # Update indices and request to update items
            self.request_update_items.emit(self.indices)

            logger.info("Previous page button clicked")
            logger.info(f"Current page: {self.current_page}")
            logger.info(f"Indices: {self.indices}")

    def disable(self) -> None:
        """Disable the buttons."""
        self.prev_page_button.setEnabled(False)
        self.next_page_button.setEnabled(False)
        self.page_spinbox.setEnabled(False)

    def enable(self) -> None:
        """Enable the buttons."""
        self.prev_page_button.setEnabled(True)
        self.next_page_button.setEnabled(True)
        self.page_spinbox.setEnabled(True)


if __name__ == "__main__":
    import sys

    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    # Enable logging
    logging.basicConfig(level=logging.INFO)

    item_per_page = 4
    total_items = 100

    page_widget = PageWidget(10, 100)
    page_widget.enable()
    page_widget.show()

    sys.exit(app.exec())
