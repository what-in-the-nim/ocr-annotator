import os.path as op
from datetime import datetime
from typing import Optional

import pandas as pd
from pandas import DataFrame


class FileHandler:
    def __init__(self) -> None:
        """Initialize the model."""
        self.path: Optional[str] = None
        self.extension: Optional[str] = None

    @staticmethod
    def get_basename(path: str) -> str:
        """Return the base name of the file."""
        filename = path.split("/")[-1]
        basename = filename.split(".")[0]
        return basename

    @staticmethod
    def get_delimiter(extension: str) -> str:
        """Return the delimiter of the file."""
        if extension == "csv":
            return ","
        elif extension == "tsv":
            return "\t"
        else:
            raise ValueError(f"Unknown extension: {extension}")

    @staticmethod
    def get_quotechar(extension: str) -> str:
        """Return the quotechar of the file."""
        if extension == "csv":
            return '"'
        elif extension == "tsv":
            return ""
        else:
            raise ValueError(f"Unknown extension: {extension}")

    @staticmethod
    def get_extension(path: str) -> str:
        """Return the extension of the file."""
        return path.split(".")[-1]

    def load(self, path: str) -> DataFrame:
        """Load the label file and return the dataframe."""
        self.path = path
        self.extension = FileHandler.get_extension(path)
        delimiter = FileHandler.get_delimiter(self.extension)
        df = pd.read_csv(path, sep=delimiter)
        return df

    def normalize_path(self, df: DataFrame, path_column_name: str) -> DataFrame:
        """Normalize the path to be relative to the label file."""
        df[path_column_name] = df[path_column_name].apply(lambda x: op.normpath(op.join(op.dirname(self.path), x)))
        return df

    def save(self, df: DataFrame, filename: Optional[str] = None) -> None:
        """Save the dataframe to a file."""
        if filename is None:
            # Create a save filename if not provided
            current_time = datetime.now().strftime("%Y%m%d_%H%M")
            base_name = FileHandler.get_basename(self.path)
            filename = f"{base_name}_{current_time}.{self.extension}"

        delimiter = FileHandler.get_delimiter(self.extension)
        df.to_csv(filename, sep=delimiter, index=False)
