import os.path as op
from dataclasses import dataclass, field
from typing import Iterable

import pandas as pd
from PIL import Image

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
    ----------
    df: pd.DataFrame
        The dataframe that stores the image path and the text.
    path_column_name: str
        The column name for the path.
    text_column_name: str
        The column name for the text.

    Methods:
    --------
    length() -> int
        Return the length of the dataframe.
    columns() -> tuple[str, ...]
        Return the columns of the dataframe.
    get_image(index: int) -> Image.Image
        Return the image at the given index.
    get_text(index: int) -> str
        Return the text at the given index.
    get_path(index: int) -> str
        Return the path at the given index.
    rotate_image(index: int) -> None
        Rotate image at the given index.
    delete_item(index: int) -> None
        Delete the row at the given index.
    change_text(text: str) -> None
        Set the text of the current image.
    load_file(path: str) -> None
        Set the label path and reload the csv file.
    save_file(path: str) -> None
        Save the current list to a csv file.
    set_path_column_name(path_column_name: str) -> None
        Set the path column name.
    set_text_column_name(text_column_name: str) -> None
        Set the text column name.
    """

    df: pd.DataFrame = None
    path_column_name: str = "path"
    text_column_name: str = "text"
    _file_handler: FileHandler = field(default_factory=FileHandler)
    _image_handler: ImageHandler = field(default_factory=ImageHandler)

    @property
    def length(self) -> int:
        """Return the length of the dataframe."""
        return len(self.df)

    @property
    def columns(self) -> tuple[str, ...]:
        """Return the columns of the dataframe."""
        return tuple(self.df.columns)

    @property
    def paths(self) -> list[str]:
        """Return the paths in the dataframe."""
        return self.df[self.path_column_name].tolist()

    @staticmethod
    def _validate_paths(paths: Iterable[str]) -> bool:
        """Validate the paths."""
        return all(op.exists(path) for path in paths)

    def load_file(self, path: str) -> None:
        """Set the label path and reload the csv file."""
        self.df = self._file_handler.load(path)
        path_valid = self._validate_paths(self.df[self.path_column_name])
        if not path_valid:
            return FileExistsError(
                "Some of the paths do not exist or the relative path is incorrect."
            )

    def cast_types(self) -> None:
        # Cast the path to string
        self.df[self.path_column_name] = self.df[self.path_column_name].astype(str)
        # Replace NaN with empty string
        self.df[self.text_column_name] = self.df[self.text_column_name].fillna("")
        # Cast the text to string
        self.df[self.text_column_name] = self.df[self.text_column_name].astype(str)

    def normalize_path(self) -> None:
        """Normalize the path."""
        if self.path_column_name not in self.columns:
            raise ValueError(
                f"Path column name {self.path_column_name} not found in columns {self.columns}."
            )

        self.df = self._file_handler.normalize_path(self.df, self.path_column_name)

    def save_file(self, path: str) -> None:
        """Save the current list to a csv file."""
        self._file_handler.save(self.df, filename=path)

    def get_image(self, index: int) -> Image.Image:
        """Return the image at the given index."""
        path = self.df.iloc[index][self.path_column_name]
        return self._image_handler.open(path)

    def get_text(self, index: int) -> str:
        """Return the text at the given index."""
        return self.df.iloc[index][self.text_column_name]

    def get_path(self, index: int) -> str:
        """Return the path at the given index."""
        return self.df.iloc[index][self.path_column_name]

    def rotate_image(self, index: int) -> None:
        """Rotate image at the given index."""
        path = self.df.iloc[index][self.path_column_name]
        image = self._image_handler.open(path)
        rotated_image = self._image_handler.rotate(image)
        rotated_image.save(path)

    def delete_item(self, index: int) -> None:
        """Delete the row at the given index."""
        self.df.drop(index, inplace=True)
        self.df.reset_index(drop=True, inplace=True)

    def change_text(self, index: int, text: str) -> None:
        """Set the text of the current image."""
        self.df.at[index, self.text_column_name] = text

    def set_path_column_name(self, path_column_name: str) -> None:
        """Set the path column name."""
        self.path_column_name = path_column_name

    def set_text_column_name(self, text_column_name: str) -> None:
        """Set the text column name."""
        self.text_column_name = text_column_name
