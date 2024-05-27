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
        # Set only font size and bold
        super().__init__()
        self.current_text = text
        font = QFont("IBM Plex Sans Thai", 16, QFont.Weight.Bold)
        self.setFont(font)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumHeight(40)
        self.setMaximumHeight(50)
        self.setMinimumWidth(80)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setContentsMargins(5, 5, 5, 5)
        self.setStyleSheet("background-color: #edfcfa; border: 1px solid #999")

    def keyPressEvent(self, event) -> None:
        """When user press enter, does like user clear focus."""
        key_pressed = event.key()
        if key_pressed == Qt.Key.Key_Enter or key_pressed == Qt.Key.Key_Return:
            self.clearFocus()
        super().keyPressEvent(event)

    def focusOutEvent(self, event) -> None:
        """When user focus out, emit the request_change_text signal."""
        if self.text() != self.current_text:
            self.current_text = self.text()
            self.request_change_text.emit(self.current_text)
        super().focusOutEvent(event)

    def disable(self) -> None:
        """Disable the text widget."""
        self.setReadOnly(True)

    def enable(self) -> None:
        """Enable the text widget."""
        self.setReadOnly(False)

    def setText(self, text: str) -> None:
        """Set the text in the text widget."""
        self.current_text = text
        super().setText(text)


if __name__ == "__main__":
    import sys

    from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget

    app = QApplication(sys.argv)
    widget = QWidget()
    layout = QVBoxLayout()
    text_widget = TextWidget("Hello, World!")
    layout.addWidget(text_widget)
    widget.setLayout(layout)
    widget.show()
    sys.exit(app.exec())
