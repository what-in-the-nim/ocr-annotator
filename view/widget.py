from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy, QLineEdit, QGroupBox, QHBoxLayout, QSpinBox
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot, QEvent
import numpy as np
import cv2
import logging


logger = logging.getLogger(__name__)


class ImageWidget(QLabel):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logger.info("Image widget initialized")

    def set_image(self, image: np.ndarray) -> None:
        """Display the image in the imageWidget."""
        logger.info("Image widget received image")
        image = self.resize_image(image)
        height, width, _ = image.shape

        qImg = QImage(image.data, width, height, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qImg)
        self.setPixmap(pixmap)

    def resize_image(self, image: np.ndarray) -> np.ndarray:
        """Resize the image to fit the imageWidget."""
        height, width, _ = image.shape
        container_width, container_height = self.width(), self.height()

        # Calculate the aspect ratio of the image
        aspect_ratio = width / height

        # Calculate the target size of the image based on the aspect ratio and the container size
        target_width = container_width
        target_height = int(target_width / aspect_ratio)

        # If the calculated height is greater than the container height, adjust the target size
        if target_height > container_height:
            target_height = container_height
            target_width = int(target_height * aspect_ratio)

        # Resize the image to the target size
        resized_image = cv2.resize(image, (target_width, target_height))

        return resized_image


class TextWidget(QGroupBox):
    change_text_request = pyqtSignal(str)
    change_index_request = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.setTitle("Label")

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Total amount label
        h_boxlayout = QHBoxLayout()
        self.image_label = QLabel(f"Image: ")
        self.index_spin_box = QSpinBox()
        self.index_spin_box.setValue(0)
        self.index_spin_box.setMinimum(0)
        self.index_spin_box.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.index_spin_box.valueChanged.connect(self.send_change_index_request)

        self.total_amount_label = QLabel("/0")
        h_boxlayout.addWidget(self.image_label)
        h_boxlayout.addWidget(self.index_spin_box)
        h_boxlayout.addWidget(self.total_amount_label)
        h_boxlayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addLayout(h_boxlayout)

        # Path label
        h_boxlayout = QHBoxLayout()
        self.path_label = QLabel("Path: ")
        self.path_edit = QLineEdit()
        self.path_edit.setReadOnly(True)
        self.path_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        h_boxlayout.addWidget(self.path_label)
        h_boxlayout.addWidget(self.path_edit)
        layout.addLayout(h_boxlayout)

        # Label line edit
        h_boxlayout = QHBoxLayout()
        line_label = QLabel("Label:")
        self.line_edit = QLineEdit()
        self.line_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        # Send the change_text_request when the user presses Enter
        self.line_edit.returnPressed.connect(self.send_change_text_request)
        # Deselect the textWidget when the user presses Enter
        self.line_edit.returnPressed.connect(self.line_edit.clearFocus)
        h_boxlayout.addWidget(line_label)
        h_boxlayout.addWidget(self.line_edit)
        layout.addLayout(h_boxlayout)

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
        self.textWidget = TextWidget()

        # Deselect the textWidget when the user clicks on the imageWidget
        self.imageWidget.mousePressEvent = lambda event: self.textWidget.line_edit.clearFocus()

        # Add the widgets to the layout
        layout.addWidget(self.imageWidget)
        layout.addWidget(self.textWidget)

        logger.info("Annotator widget initialized")

    def set_image(self, image: np.ndarray) -> None:
        """Display the image in the imageWidget."""
        logger.info("Annotator widget received image")
        self.imageWidget.set_image(image)

    def set_text(self, text: str) -> None:
        """Display the text in the textWidget."""
        logger.info("Annotator widget received text: %s", text)
        self.textWidget.set_text(text)

    def set_path(self, path: str) -> None:
        """Display the path in the textWidget."""
        logger.info("Annotator widget received path: %s", path)
        self.textWidget.set_path(path)

    def set_index(self, index: int):
        """Display the amount in the textWidget."""
        logger.info("Annotator widget received amount: %s", index)
        self.textWidget.set_index(index)
