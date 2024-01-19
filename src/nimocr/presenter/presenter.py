import logging
import os.path as op
from datetime import datetime

from PyQt6.QtCore import QObject, pyqtSlot

from ..model import ImageListModel, FileHandler
from ..view import MainWindow

logger = logging.getLogger(__name__)


class Presenter(QObject):
    """
    This class is used to connect the model and the view.
    """

    def __init__(self, model: ImageListModel, view: MainWindow) -> None:
        super().__init__()
        self.model = model
        self.view = view

        # Connect signals
        self.view.annotatorWidget.textWidget.change_text_request.connect(self.fix_label)
        self.view.annotatorWidget.textWidget.change_index_request.connect(self.change_index)
        self.view.open_selected_file.connect(self.load_file)

        self.view.request_prev_image.connect(self.backward_image)
        self.view.request_next_image.connect(self.forward_image)
        self.view.request_save_file.connect(self.save_file)
        self.view.request_image_rotate.connect(self.rotate_image)
        self.view.request_delete_item.connect(self.delete_item)
        self.view.request_create_file_dialog.connect(self.view.create_browse_file_dialog)

        logger.info("Presenter initialized")

    @pyqtSlot(int)
    def change_index(self, new_index: int) -> None:
        """Move the index of the model and update the view"""
        logger.info("Presenter received new index: %s", new_index)
        self.model.move_to(new_index)
        self.refresh_widget()

    @pyqtSlot(str)
    def fix_label(self, new_text: str) -> None:
        """Change the text of the current sample and update the view"""
        logger.info("Presenter received new text: %s", new_text)
        self.view.show_message(f"Text change from {self.model.text} to {new_text}")
        self.model.set_text(new_text)

    @pyqtSlot(str)
    def load_file(self, file_path: str) -> None:
        """Load the file and update the view"""
        logger.info("Presenter received file path: %s", file_path)
        # Load model from the file path.
        self.model.load_file(file_path)
        # Get the path column and text column from the user.
        path_column, text_column = self.view.create_select_column_dialog(self.model.columns)
        # Set the path column and text column to the model.
        self.model.set_path_column_name(path_column)
        self.model.set_text_column_name(text_column)
        # Initialize the spinbox to match the new length.
        total_items = self.model.length
        # Enable the actions on the toolbar.
        self.view.activate_actions()
        # Enable the spinbox.
        self.view.annotatorWidget.textWidget.index_spin_box.setEnable(True)
        self.view.annotatorWidget.textWidget.initialize_spinbox(total_items)
        self.refresh_widget()

    @pyqtSlot()
    def save_file(self) -> None:
        """Save the file and update the view"""
        logger.info("Presenter received save file request")
        # Create a save filedialog and get the save path.
        label_dir = op.dirname(self.model._file_handler.path)
        base_name = FileHandler.get_basename(self.model._file_handler.path)
        current_time = datetime.now().strftime("%Y%m%d_%H%M")
        save_filename = f"{base_name}_{current_time}.{self.model._file_handler.extension}"
        save_path = op.join(label_dir, save_filename)
        save_path = self.view.create_save_file_dialog(save_path)
        # Save model to the save path.
        self.model.save_file(save_path)
        self.view.show_message(f"File saved at: {save_path}")

    @pyqtSlot()
    def rotate_image(self) -> None:
        """Rotate the image 90 degree and update the view"""
        logger.info("Presenter received rotate image request")
        # Rotate the current image.
        self.model.rotate_image()
        self.refresh_widget()

    @pyqtSlot()
    def delete_item(self) -> None:
        """Delete the current item and update the view"""
        logger.info("Presenter received delete row request")
        self.model.delete_item()
        # Reinitialize the spinbox to match the new length.
        total_items = self.model.length
        self.view.annotatorWidget.textWidget.initialize_spinbox(total_items)
        self.refresh_widget()

    @pyqtSlot()
    def backward_image(self) -> None:
        """Move the index backward and update the view"""
        logger.info("Presenter received backward image request")
        # Shift the index to the previous item.
        self.model.prev()
        self.refresh_widget()

    @pyqtSlot()
    def forward_image(self) -> None:
        """Move the index forward and update the view"""
        logger.info("Presenter received forward image request")
        # Shift the index to the next item.
        self.model.next()
        self.refresh_widget()

    def refresh_widget(self) -> None:
        """
        When the model state is updated,
        call this function to update the view.
        """
        image = self.model.image
        # Return if image is exception raised
        if isinstance(image, Exception):
            error_message = str(image)
            self.view.show_message(error_message)
        self.view.annotatorWidget.set_image(image)
        self.view.annotatorWidget.set_text(self.model.text)
        self.view.annotatorWidget.set_index(self.model.index)
        self.view.annotatorWidget.set_path(self.model.path)
