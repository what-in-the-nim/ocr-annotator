from PyQt6.QtCore import pyqtSlot, QObject
from nimocr.model.image_list import ImageListModel
from nimocr.view.main_window import MainWindow
import logging

logger = logging.getLogger(__name__)


class Presenter(QObject):
    def __init__(self, model: ImageListModel, view: MainWindow):
        super().__init__()
        self.model = model
        self.view = view

        # Connect signals
        self.view.annotatorWidget.textWidget.change_text_request.connect(
            self.fix_label
        )
        self.view.annotatorWidget.textWidget.change_index_request.connect(
            self.change_index
        )
        self.view.open_selected_file.connect(self.initialize_file)

        self.view.request_prev_image.connect(self.backward_image)
        self.view.request_next_image.connect(self.forward_image)
        self.view.request_save_file.connect(self.model.save_file)
        self.view.request_image_rotate.connect(self.rotate_image)
        self.view.request_delete_item.connect(self.delete_item)
        self.view.request_change_text_column_name.connect(
            self.model.set_text_column_name
        )
        self.view.request_change_path_column_name.connect(
            self.model.set_path_column_name
        )
        self.view.request_create_file_dialog.connect(self.create_file_dialog)

        logger.info("Presenter initialized")

    @pyqtSlot(int)
    def change_index(self, new_index: int) -> None:
        """Move the index of the model and update the view"""
        logger.info("Presenter received new index: %s", new_index)
        self.model.move_to(new_index)
        self.view.annotatorWidget.set_image(self.model.image)
        self.view.annotatorWidget.set_text(self.model.text)

    @pyqtSlot(str)
    def fix_label(self, new_text: str) -> None:
        """Change the text of the current sample and update the view"""
        logger.info("Presenter received new text: %s", new_text)
        self.view.show_message(
            f"Text change from {self.model.text} to {new_text}"
        )
        self.model.set_text(new_text)

    @pyqtSlot(str)
    def initialize_file(self, file_path: str) -> None:
        """Load the file and update the view"""
        logger.info("Presenter received file path: %s", file_path)
        self.model.load_file(file_path)
        self.view.annotatorWidget.textWidget.initialize_spinbox(
            self.model.length
        )
        self.update_widget()

    @pyqtSlot()
    def rotate_image(self) -> None:
        """Rotate the image 90 degree and update the view"""
        logger.info("Presenter received rotate image request")
        self.model.rotate_image()
        self.view.annotatorWidget.set_image(self.model.image)

    @pyqtSlot()
    def delete_item(self) -> None:
        """Delete the current item and update the view"""
        logger.info("Presenter received delete row request")
        self.model.delete_item()
        self.view.annotatorWidget.textWidget.initialize_spinbox(
            self.model.length
        )
        self.update_widget()

    @pyqtSlot()
    def backward_image(self) -> None:
        logger.info("Presenter received backward image request")
        self.model.prev()
        self.update_widget()

    @pyqtSlot()
    def forward_image(self) -> None:
        logger.info("Presenter received forward image request")
        self.model.next()
        self.update_widget()

    @pyqtSlot()
    def create_file_dialog(self) -> None:
        """Create a file dialog to load a new file"""
        path_column_name = self.model.path_column_name
        text_column_name = self.model.text_column_name
        self.view.create_file_dialog(path_column_name, text_column_name)

    def update_widget(self) -> None:
        self.view.annotatorWidget.set_image(self.model.image)
        self.view.annotatorWidget.set_text(self.model.text)
        self.view.annotatorWidget.set_index(self.model.index)
        self.view.annotatorWidget.set_path(self.model.path)
