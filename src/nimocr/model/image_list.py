import os.path as op
from dataclasses import dataclass, field
from typing import Iterable

import pandas as pd

from .file_handler import FileHandler
from .image_handler import ImageHandler


class ImageListSortType:
    """Enum for the sort type.

    Attributes:
        CER (str): Sort by CER.
        LENGTH (str): Sort by length.
    """

    CER = "cer"
    LENGTH = "length"


@dataclass
class ImageListModel:
    """Model for the image list.

    This class is used to store the image list and the labels. It will load image from the path only when needed.

    Attributes:
        index (int): The current index of the image.
        label_df (pd.DataFrame): The dataframe containing the labels.
        csv_path (str): The path of the csv file.
        path_column_name (str): The name of the column containing the path.
        text_column_name (str): The name of the column containing the text.

    Methods:
        image: Return the current image.
        text: Return the text of the current image.
        path: Return the path of the current image.
        length: Return the length of the dataframe.
        _load_csv: Load the csv file.
        load_file: Set the label path and reload the csv file.
        save_file: Save the current list to a csv file.
        rotate_image: Rotate the current image.
        delete_row: Delete the current row.
        set_text: Set the text of the current row.
        prev: Move to the previous image.
        next: Move to the next image.
        move_to: Move to the specified index.
    """

    index: int = 0
    df: pd.DataFrame = None
    path_column_name: str = "path"
    text_column_name: str = "text"
    _file_handler: FileHandler = field(default_factory=FileHandler)
    _image_handler: ImageHandler = field(default_factory=ImageHandler)

    @property
    def image(self) -> None:
        """Return the current image."""
        return self._image_handler.open(self.path)

    @property
    def text(self) -> str:
        """Return the text of the current image."""
        return self.df.iloc[self.index][self.text_column_name]

    @property
    def path(self) -> str:
        """Return the path of the current image."""
        _path = self.df.iloc[self.index][self.path_column_name]
        dirname = op.dirname(self._file_handler.path)
        return op.join(dirname, _path)

    @property
    def length(self) -> int:
        """Return the length of the dataframe."""
        return len(self.df)

    @property
    def columns(self) -> tuple[str, ...]:
        """Return the columns of the dataframe."""
        return tuple(self.df.columns)

    @staticmethod
    def validate_paths(paths: Iterable[str]) -> bool:
        """Validate the paths."""
        return all(op.isexists(path) for path in paths)

    def load_file(self, label_path: str, check_corrupted_file: bool = True) -> None:
        """Set the label path and reload the csv file."""
        self.df = self._file_handler.load(label_path)
        if check_corrupted_file:
            path_valid = self.validate_paths(self.df[self.path_column_name])
            if not path_valid:
                return FileExistsError("Some of the paths do not exist.")

    def save_file(self, save_path: str) -> None:
        """Save the current list to a csv file."""
        self._file_handler.save(self.df, filename=save_path)

    def rotate_image(self) -> None:
        """Rotate the current image and save it."""
        rotated_image = self._image_handler.rotate(self.image)
        rotated_image.save(self.path)

    def delete_item(self) -> None:
        """Delete the current row."""
        self.df.drop(self.index, inplace=True)
        self.df.reset_index(drop=True, inplace=True)

    def set_text(self, text: str) -> None:
        """Set the text of the current image."""
        self.df.loc[self.index, self.text_column_name] = text

    def set_path_column_name(self, path_column_name: str) -> None:
        """Set the path column name."""
        self.path_column_name = path_column_name

    def set_text_column_name(self, text_column_name: str) -> None:
        """Set the text column name."""
        self.text_column_name = text_column_name

    def move_to(self, index: int) -> None:
        """Move the index to the given index."""
        if index < 0 or index >= self.length:
            return
        self.index = index

    def next(self) -> None:
        """Shift the index to the next image."""
        self.move_to(self.index + 1)

    def prev(self) -> None:
        """Shift the index to the previous image."""
        self.move_to(self.index - 1)

    def reset(self) -> None:
        """Sort the index of datafrane."""
        self.df = self.df.sort_index()

    def sort(self, column_name: str) -> None:
        """Sort the dataframe by the given column."""
        self.df = self.df.sort_values(by=column_name)
