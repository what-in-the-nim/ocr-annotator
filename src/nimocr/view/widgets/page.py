from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QSpinBox, QStyle, QWidget


class PageWidget(QWidget):
    """
    PageWidget is a widget that displays a button to navigate to the previous page or the next page.
    The widget also displays the item per page, current page, and total page.
    The widget accepts total items and items per page as arguments and it will acts as the controller
    to navigate through the pages.
    The left-most button is a spinbox that allows the user to change the items per page.
    The center widget is a group of two buttons that allows the user to navigate to the previous page or the next page.
    The right-most widget is a spinbox of the current page/the total page and label of the total items.

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
    """

    def __init__(self, items_per_page: int, total_items: int) -> None:
        """Initialize the PageWidget."""
        super().__init__()
        # Set up state.
        self.items_per_page = items_per_page
        self.total_items = total_items
        self.current_page = 1
        self._indices = [i for i in range(min(self.items_per_page, self.total_items))]

        # Set up layout
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        # Set up items per page spinbox
        item_per_page_layout = QHBoxLayout()
        label = QLabel("Item per pages:")
        self.items_per_page_spinbox = QSpinBox()
        self.items_per_page_spinbox.setRange(1, 10)
        self.items_per_page_spinbox.setValue(items_per_page)
        self.items_per_page_spinbox.setFixedWidth(30)
        self.items_per_page_spinbox.setFixedHeight(30)
        self.items_per_page_spinbox.valueChanged.connect(self.set_items_per_page)
        item_per_page_layout.addWidget(label)
        item_per_page_layout.addWidget(self.items_per_page_spinbox)
        layout.addLayout(item_per_page_layout)

        # Add button group
        self.button_layout = QHBoxLayout()
        # Set up previous page button
        self.prev_page_button = QPushButton()
        self.prev_page_button.setFixedWidth(30)
        self.prev_page_button.setFixedHeight(30)
        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowBack)
        self.prev_page_button.setIcon(icon)
        self.prev_page_button.clicked.connect(self.prev_page)
        self.button_layout.addWidget(self.prev_page_button)
        # Set up next page button
        self.next_page_button = QPushButton()
        self.next_page_button.setFixedWidth(30)
        self.next_page_button.setFixedHeight(30)
        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowForward)
        self.next_page_button.setIcon(icon)
        self.next_page_button.clicked.connect(self.next_page)
        self.button_layout.addWidget(self.next_page_button)

        layout.addLayout(self.button_layout)

        # Set up current page spinbox
        self.current_page_spinbox = QSpinBox()
        self.current_page_spinbox.setRange(1, self.total_pages)
        self.current_page_spinbox.setValue(1)
        self.current_page_spinbox.setFixedWidth(30)
        self.current_page_spinbox.setFixedHeight(30)
        self.current_page_spinbox.valueChanged.connect(self.go_to_page)
        layout.addWidget(
            self.current_page_spinbox, alignment=Qt.AlignmentFlag.AlignRight
        )

    @property
    def total_pages(self) -> int:
        """Return the total pages."""
        return self.total_items // self.items_per_page

    @property
    def indices(self) -> list[int]:
        """Return the indices."""
        return self._indices

    def _setup_indices(self, start_index: int, stop_index: int) -> None:
        """Setup the indices."""
        self._indices = [i for i in range(start_index, stop_index)]

    def set_total_items(self, total_items: int) -> None:
        """Set the total items."""
        self.total_items = total_items
        self._setup_indices(
            self.current_page - 1,
            min(self.current_page * self.items_per_page, self.total_items),
        )

    def set_items_per_page(self, items_per_page: int) -> None:
        """Set the items per page."""
        self.items_per_page = items_per_page
        # Make the current page stay the same
        self._setup_indices(
            self.current_page - 1,
            min(self.current_page * self.items_per_page, self.total_items),
        )

    def go_to_page(self, page: int) -> None:
        """Go to the specified page."""
        if 1 <= page <= self.total_pages:
            start_index = (page - 1) * self.items_per_page
            stop_index = min(page * self.items_per_page, self.total_items)
            self._setup_indices(start_index, stop_index)

    def next_page(self) -> None:
        """Go to the next page."""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.go_to_page(self.current_page)

    def prev_page(self) -> None:
        """Go to the previous page."""
        if self.current_page > 1:
            self.current_page -= 1
            self.go_to_page(self.current_page)
