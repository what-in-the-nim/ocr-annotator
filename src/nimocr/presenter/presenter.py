import logging
import os.path as op
from datetime import datetime

from PyQt6.QtCore import QObject, pyqtSlot

from ..model import FileHandler, ImageListModel
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

        self.is_loaded = False

        self.link_signals()

        logger.info("Presenter initialized")

    def link_signals(self) -> None:
        """Link signals between the view and the presenter."""
        # Connect signals of AnnotationWidget to the presenter.
        self.view.annotatorWidget.request_rotate_image.connect(self.handle_rotate_image)
        self.view.annotatorWidget.request_change_text.connect(self.handle_change_text)
        self.view.annotatorWidget.request_delete_item.connect(self.handle_delete_item)
        self.view.annotatorWidget.request_update_items.connect(self.refresh_widget)

        self.view.open_selected_file.connect(self.load_file)

        # Connect signals of MainWindow to the presenter.
        self.view.request_save_file.connect(self.save_file)
        self.view.request_image_rotate.connect(self.handle_rotate_image)
        self.view.request_delete_item.connect(self.handle_delete_item)
        self.view.request_create_file_dialog.connect(self.view.create_browse_file_dialog)


    @pyqtSlot(int)
    def handle_rotate_image(self, index: int) -> None:
        """Rotate the image 90 degree and update the view"""
        if not self.is_loaded:
            return
        logger.info("Presenter received rotate image request")
        # Rotate the current image.
        self.model.rotate_image(index)
        # Update the view.
        current_indices = self.view.annotatorWidget.page_widget.indices
        self.refresh_widget(current_indices)

    @pyqtSlot(int, str)
    def handle_change_text(self, index: int, new_text: str) -> None:
        """Change the text of the current sample and update the view"""
        if not self.is_loaded:
            return

        logger.info("Presenter received new text: %s", new_text)
        text = self.model.get_text(index)
        self.view.show_message(f"Text change from {text} to {new_text}")
        self.model.change_text(index, new_text)
        current_indices = self.view.annotatorWidget.page_widget.indices
        self.refresh_widget(current_indices)

    @pyqtSlot(int)
    def handle_delete_item(self, index: int) -> None:
        """Delete the current item and update the view"""
        if not self.is_loaded:
            return
        logger.info("Presenter received delete row request")
        self.model.delete_item(index)
        self.view.annotatorWidget.path_list_widget.remove_item(index)
        # Reinitialize the spinbox to match the new length.
        total_items = self.model.length
        self.view.annotatorWidget.set_total_items(total_items)

    @pyqtSlot(str)
    def load_file(self, path: str) -> None:
        """Load the file and update the view"""
        logger.info("Presenter received file path: %s", path)
        # Load model from the file path.
        self.model.load_file(path)
        # Get the path column and text column from the user.
        path_column, text_column = self.view.create_select_column_dialog(self.model.columns)
        # Set the path column and text column to the model.
        self.model.set_path_column_name(path_column)
        self.model.set_text_column_name(text_column)
        # Cast the types of the columns.
        self.model.cast_types()
        # Normalize the path.
        self.model.normalize_path()
        # Enable the actions on the toolbar.
        self.view.activate_actions()
        # Enable the spinbox.
        self.view.annotatorWidget.enable()
        self.view.annotatorWidget.set_total_items(self.model.length)
        self.view.annotatorWidget.path_list_widget.set_paths(self.model.paths)
        self.is_loaded = True

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

    @pyqtSlot(list)
    def refresh_widget(self, indices: list[int]) -> None:
        """
        When the model state is updated,
        call this function to update the view.
        """
        logger.info("Refreshing widget")

        images = [self.model.get_image(index) for index in indices]
        texts = [self.model.get_text(index) for index in indices]
        paths = [self.model.get_path(index) for index in indices]

        self.view.annotatorWidget.set_images(images)
        self.view.annotatorWidget.set_texts(texts)
        self.view.annotatorWidget.set_paths(paths)
        self.view.annotatorWidget.set_indices(indices, self.model.length)

