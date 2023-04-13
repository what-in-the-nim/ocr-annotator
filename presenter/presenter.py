from PyQt6.QtCore import pyqtSlot, QObject
from model.image_list import ImageListModel
from view.main_window import MainWindow
import logging

logger = logging.getLogger(__name__)

class Presenter(QObject):
    def __init__(self, model: ImageListModel, view: MainWindow):
        super().__init__()
        self.model = model
        self.view = view

        # Connect signals
        self.view.annotatorWidget.textWidget.change_text_request.connect(self.fix_label)
        self.view.annotatorWidget.textWidget.change_index_request.connect(self.change_index)
        self.view.open_selected_file.connect(self.initialize_file)

        self.view.request_prev_image.connect(self.backward_image)
        self.view.request_next_image.connect(self.forward_image)
        self.view.request_save_file.connect(self.model.save_file)
        self.view.request_image_rotate.connect(self.rotate_image)
        self.view.request_delete_item.connect(self.delete_row)

        logger.info("Presenter initialized")

    @pyqtSlot(int)
    def change_index(self, new_index: int) -> None:
        logger.info("Presenter received new index: %s", new_index)
        self.model.move_to(new_index)
        self.view.annotatorWidget.set_image(self.model.image)
        self.view.annotatorWidget.set_text(self.model.text)

    @pyqtSlot(str)
    def fix_label(self, new_text: str) -> None:
        logger.info("Presenter received new text: %s", new_text)
        self.view.show_message(f"Text change from {self.model.text} to {new_text}")
        self.model.set_text(new_text)

    @pyqtSlot(str)
    def initialize_file(self, file_path: str):
        logger.info("Presenter received file path: %s", file_path)
        self.model.load_file(file_path)
        self.view.annotatorWidget.textWidget.initialize_spinbox(self.model.length)
        self.update_widget()

    @pyqtSlot()
    def rotate_image(self):
        logger.info("Presenter received rotate image request")
        self.model.rotate_image()
        self.view.annotatorWidget.set_image(self.model.image)

    @pyqtSlot()
    def delete_row(self):
        logger.info("Presenter received delete row request")
        self.model.delete_row()
        self.view.annotatorWidget.textWidget.initialize_spinbox(self.model.length)
        self.update_widget()

    def backward_image(self):
        logger.info("Presenter received backward image request")
        self.model.prev()
        self.update_widget()

    def forward_image(self):
        logger.info("Presenter received forward image request")
        self.model.next()
        self.update_widget()

    def update_widget(self):
        self.view.annotatorWidget.set_image(self.model.image)
        self.view.annotatorWidget.set_text(self.model.text)
        self.view.annotatorWidget.set_index(self.model.index)
        self.view.annotatorWidget.set_path(self.model.path)
