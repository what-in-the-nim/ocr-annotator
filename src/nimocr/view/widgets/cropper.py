import sys
from typing import Optional

from PIL import Image, ImageQt
from PyQt6.QtCore import QPoint, QRect, Qt
from PyQt6.QtGui import QBrush, QColor, QPainter, QPen, QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget


class ImageCropper(QWidget):

    AREA_COLOR = QColor(0, 0, 0, 50)
    CROSS_COLOR = QColor(255, 0, 0)

    def __init__(
        self,
        image: Optional[Image.Image] = None,
        size: Optional[QPoint] = None,
        area_color: Optional[QColor] = None,
        cross_color: Optional[QColor] = None,
    ):
        super().__init__()
        self.init_ui()
        # Resize widget to the given size
        if size:
            self.resize(*size)
            self.setFixedSize(*size)

        self.area_color = area_color if area_color is not None else self.AREA_COLOR
        self.cross_color = cross_color if cross_color is not None else self.CROSS_COLOR
        self.original_image = None
        self.thumbnail_image = None
        self.hires_image = None
        self.set_image(image)

    def init_ui(self):
        self.setWindowTitle("Image Cropper")
        layout = QVBoxLayout()

        self.display_label = QLabel()
        layout.addWidget(
            self.display_label,
            alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft,
        )

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_image)
        layout.addWidget(self.reset_button)

        self.setLayout(layout)

        self.selection_rect = QRect()
        self.dragging = False

    def set_image(self, image: Optional[Image.Image]) -> None:
        """Set the image to the widget."""
        if image is not None:
            self.original_image = image

            self.hires_image = image.copy()

            self.thumbnail_image = image.copy()
            self.thumbnail_image.thumbnail(
                (self.display_label.width(), self.display_label.height()),
                Image.Resampling.LANCZOS,
            )
            self.update_pixmap()

    def reset_image(self):
        if self.original_image:
            self.hires_image = self.original_image.copy()

            self.thumbnail_image = self.original_image.copy()
            self.thumbnail_image.thumbnail(
                (self.width(), self.height()), Image.Resampling.LANCZOS
            )

            self.update_pixmap()
            self.selection_rect = QRect()
            self.update()

    def update_pixmap(self):
        qimage = ImageQt.ImageQt(self.thumbnail_image)
        pixmap = QPixmap.fromImage(qimage)
        self.display_label.setPixmap(pixmap)
        # self.resize(self.display_label.width(), self.display_label.height())

    def resizeEvent(self, event):
        """Resize the image when the widget is resized."""
        super().resizeEvent(event)
        if self.thumbnail_image:
            self.thumbnail_image.thumbnail(
                (self.width(), self.height()), Image.Resampling.LANCZOS
            )
            self.update_pixmap()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.thumbnail_image:
            pixmap = self.thumbnail_image.toqpixmap().copy()
            painter = QPainter(pixmap)

            if self.selection_rect.isValid():
                painter.setPen(QPen(self.cross_color, 1, Qt.PenStyle.SolidLine))
                painter.setBrush(QBrush(self.area_color))
                painter.drawRect(self.selection_rect)

                # Draw cross
                center = self.selection_rect.center()
                painter.drawLine(center.x(), 0, center.x(), pixmap.height())
                painter.drawLine(0, center.y(), pixmap.width(), center.y())

            painter.end()
            self.display_label.setPixmap(pixmap)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.selection_rect.setTopLeft(event.pos() - self.display_label.pos())
            self.selection_rect.setBottomRight(event.pos() - self.display_label.pos())
            self.update()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.selection_rect.setBottomRight(event.pos() - self.display_label.pos())
            self.update()
        else:
            # Draw line
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            if self.selection_rect.isValid():
                self.crop_image()
            self.update()

    def crop_image(self):
        if self.selection_rect.isValid():
            x1 = max(self.selection_rect.left(), 0)
            y1 = max(self.selection_rect.top(), 0)
            x2 = min(self.selection_rect.right(), self.thumbnail_image.width)
            y2 = min(self.selection_rect.bottom(), self.thumbnail_image.height)

            # Convert coordinates to original image scale
            orig_x1 = int(x1 * self.hires_image.width / self.thumbnail_image.width)
            orig_y1 = int(y1 * self.hires_image.height / self.thumbnail_image.height)
            orig_x2 = int(x2 * self.hires_image.width / self.thumbnail_image.width)
            orig_y2 = int(y2 * self.hires_image.height / self.thumbnail_image.height)

            self.cropped_image = self.hires_image.crop(
                (orig_x1, orig_y1, orig_x2, orig_y2)
            )
            self.update_pixmap_with_cropped()
            self.selection_rect = QRect()

    def update_pixmap_with_cropped(self):
        self.hires_image = self.cropped_image.copy()

        self.thumbnail_image = self.cropped_image.copy()
        self.thumbnail_image.thumbnail((self.width(), self.height()), Image.ANTIALIAS)
        self.update_pixmap()

    @property
    def image(self):
        return self.cropped_image if self.cropped_image else self.original_image


def main():
    app = QApplication(sys.argv)
    input_image = Image.open("20240302_105643.jpg")
    cropper = ImageCropper(
        image=input_image,
        size=(800, 600),
        area_color=QColor(0, 255, 0, 50),
        cross_color=QColor(0, 0, 255),
    )
    cropper.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
