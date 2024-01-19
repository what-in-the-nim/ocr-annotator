import logging

import numpy as np
from PIL import Image
from PyQt6.QtCore import QPoint, Qt, pyqtSignal, pyqtSlot, QMimeData
from PyQt6.QtGui import QAction, QImage, QPixmap, QResizeEvent, QFont
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMenu,
    QSizePolicy,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from ..model import ImageHandler

logger = logging.getLogger(__name__)

class PreviewTextWidget(QLabel):
    def __init__(self, text, parent=None):
        super(PreviewTextWidget, self).__init__(text, parent)

        # Set only font size and bold
        font = QFont("IBM Plex Sans Thai", 18, QFont.Weight.Bold)
        self.setFont(font)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMaximumHeight(50)

        # Set background color and border
        self.setStyleSheet("background-color: #edfcfa; border: 1px solid #999; border-radius: 5px;")

        # Set padding
        self.setContentsMargins(10, 5, 10, 5)


class ImageWidget(QLabel):
    def __init__(self):
        super().__init__()
        self.image = None
        self.setMinimumSize(1, 30)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logger.info("Image widget initialized")

        # Set right click menu
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showMenu)

    def showMenu(self, pos: QPoint) -> None:
        """Show the right click menu."""
        logger.info(f"Image widget received right click at {pos}")
        # Create the menu
        menu = QMenu(self)
        # Create copy action
        copy_action = QAction("Copy Image", self)
        copy_action.triggered.connect(self.copy_image)
        # Add copy action to the menu
        menu.addAction(copy_action)
        # Show the menu
        menu.exec(self.mapToGlobal(pos))

    def copy_image(self) -> None:
        """Copy the image to the clipboard."""
        logger.info("Image widget received copy image request")
        data = QMimeData()
        data.setImageData(self.pixmap().toImage())
        clipboard = QApplication.clipboard()
        clipboard.setMimeData(data)

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Handle the resize event."""
        self.update_image()

    def set_image(self, image: Image.Image) -> None:
        """Set the image in the imageWidget."""
        logger.info("Image widget received image")
        self.image = image
        self.update_image()

    def update_image(self) -> None:
        """Update the image in the imageWidget."""
        if self.image is None:
            return

        container_size = (self.width(), self.height())
        image = ImageHandler.fit(self.image, container_size)

        # Create a QImage from the padded image data
        width, height = image.size

        qImg = QImage(
            image.tobytes(),
            width,
            height,
            3 * width,
            QImage.Format.Format_RGB888,
        )
        pixmap = QPixmap.fromImage(qImg)
        self.setPixmap(pixmap)


class TextWidget(QGroupBox):
    change_text_request = pyqtSignal(str)
    change_index_request = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.setTitle("Tools")

        layout = QGridLayout()
        self.setLayout(layout)

        # Total amount label
        image_label = QLabel(f"Image: ")
        h_boxlayout = QHBoxLayout()
        self.index_spin_box = QSpinBox()
        self.index_spin_box.setValue(0)
        self.index_spin_box.setMinimum(0)
        self.index_spin_box.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.index_spin_box.setEnabled(False)
        self.index_spin_box.valueChanged.connect(self.send_change_index_request)

        self.total_amount_label = QLabel("/0")
        h_boxlayout.addWidget(self.index_spin_box)
        h_boxlayout.addWidget(self.total_amount_label)
        h_boxlayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(image_label, 0, 0, 1, 1)
        layout.addLayout(h_boxlayout, 0, 1, 1, 1)

        # Path label
        path_label = QLabel("Path: ")
        h_boxlayout = QHBoxLayout()
        self.path_edit = QLineEdit()
        self.path_edit.setReadOnly(True)
        self.path_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        h_boxlayout.addWidget(self.path_edit)

        layout.addWidget(path_label, 1, 0, 1, -1)
        layout.addLayout(h_boxlayout, 1, 1, 1, -1)

        # Label line edit
        line_label = QLabel("Label:")
        h_boxlayout = QHBoxLayout()
        self.line_edit = QLineEdit()
        self.line_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        # Send the change_text_request when the user presses Enter
        self.line_edit.returnPressed.connect(self.send_change_text_request)
        self.line_edit.textChanged.connect(self.send_change_text_request)
        # Deselect the textWidget when the user presses Enter
        self.line_edit.returnPressed.connect(self.line_edit.clearFocus)
        h_boxlayout.addWidget(self.line_edit)

        layout.addWidget(line_label, 2, 0, 1, -1)
        layout.addLayout(h_boxlayout, 2, 1, 1, -1)

    def initialize_spinbox(self, max_value: int):
        self.index_spin_box.setMaximum(max_value)
        self.total_amount_label.setText(f"/{max_value}")

    @pyqtSlot(int)
    def set_index(self, index: int) -> None:
        """Display the index in the SpinBox."""
        self.index_spin_box.setValue(index)

    @pyqtSlot(str)
    def set_path(self, path: str) -> None:
        """Display the path in the pathLabel."""
        self.path_edit.setText(path)

    @pyqtSlot(str)
    def set_text(self, text: str) -> None:
        """Display the text in the textWidget."""
        self.current_text = text
        self.line_edit.setText(text)

    @pyqtSlot()
    def send_change_text_request(self) -> None:
        """Send the fix_label_request signal."""
        logger.info("Fix label request sent")
        text_in_line_edit = self.line_edit.text()
        if self.current_text != text_in_line_edit:
            self.current_text = text_in_line_edit
            self.change_text_request.emit(self.current_text)

    @pyqtSlot()
    def send_change_index_request(self) -> None:
        """Send the change_index_request signal."""
        logger.info("Change index request sent")
        index = self.index_spin_box.value()
        self.change_index_request.emit(index)


class AnnotatorWidget(QWidget):
    image_rotate_request = pyqtSignal()
    change_label_request = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.imageWidget = ImageWidget()
        self.previewTextWidget = PreviewTextWidget("")
        self.textWidget = TextWidget()

        # Deselect the textWidget when the user clicks on the imageWidget
        self.imageWidget.mousePressEvent = lambda event: self.textWidget.line_edit.clearFocus()
        self.previewTextWidget.mousePressEvent = lambda event: self.textWidget.line_edit.clearFocus()

        # Update preview text when the user changes the text
        self.textWidget.change_text_request.connect(self.previewTextWidget.setText)

        # Add the widgets to the layout
        layout.addWidget(self.previewTextWidget)
        layout.addWidget(self.imageWidget)
        layout.addWidget(self.textWidget)

        logger.info("Annotator widget initialized")

    def set_image(self, image: np.ndarray) -> None:
        """Display the image in the imageWidget."""
        logger.info("Annotator widget received image")
        self.imageWidget.set_image(image)

    def set_text(self, text: str) -> None:
        """Display the text in the textWidget."""
        logger.info("Annotator widget received text: '%s'", text)
        self.previewTextWidget.setText(text)
        self.textWidget.set_text(text)

    def set_path(self, path: str) -> None:
        """Display the path in the textWidget."""
        logger.info("Annotator widget received path: '%s'", path)
        self.textWidget.set_path(path)

    def set_index(self, index: int):
        """Display the amount in the textWidget."""
        logger.info("Annotator widget received amount: %s", index)
        self.textWidget.set_index(index)
