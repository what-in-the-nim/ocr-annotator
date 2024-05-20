from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLineEdit, QSizePolicy


class TextWidget(QLineEdit):
    """
    Text widget for displaying text.
    User can be able to click and edit the text.
    The text will be displayed at the left of the widget.
    If user press enter or focus out, the text will be changed.

    Signals:
    --------
        request_change_text (str): Signal to request the change of the text.

    """

    request_change_text = pyqtSignal(str)

    def __init__(self, text: str = "") -> None:
        super().__init__(text)
        # Set only font size and bold
        font = QFont("IBM Plex Sans Thai", 16, QFont.Weight.Bold)
        self.setFont(font)
        self.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setContentsMargins(5, 5, 5, 5)
        self.setStyleSheet("background-color: #edfcfa; border: 1px solid #999")

    def keyPressEvent(self, event) -> None:
        """When user press enter, does like user clear focus."""
        if event.key() == Qt.Key.Key_Enter:
            self.clearFocus()
        super().keyPressEvent(event)

    def focusOutEvent(self, event) -> None:
        """When user focus out, emit the request_change_text signal."""
        self.request_change_text.emit(self.text())
        super().focusOutEvent(event)
