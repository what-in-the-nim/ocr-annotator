import pandas as pd
from PIL import Image
from datetime import datetime


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

    class ImageListSortType:
        """Enum for the sort type.

        Attributes:
            CER (str): Sort by CER.
            LENGTH (str): Sort by length.
        """

        CER = "cer"
        LENGTH = "length"

    def __init__(self) -> None:
        """Initialize the model."""
        self.index = 0
        self.label_df = None
        self.csv_path = None
        self.path_column_name = "path"
        self.text_column_name = "text"

    @property
    def image(self) -> None:
        """Return the current image."""
        return Image.open(self.path).convert("RGB")

    @property
    def text(self) -> str:
        """Return the text of the current image."""
        return self.label_df.iloc[self.index][self.text_column_name]

    @property
    def path(self) -> str:
        """Return the path of the current image."""
        return self.label_df.iloc[self.index][self.path_column_name]

    @property
    def length(self) -> int:
        """Return the length of the dataframe."""
        return len(self.label_df)

    def _load_csv(self) -> None:
        """Load the csv file."""
        self.label_df = pd.read_csv(self.csv_path).sort_values(by=self.path_column_name)

    def load_file(self, label_path: str) -> None:
        """Set the label path and reload the csv file."""
        self.csv_path = label_path
        self._load_csv()

    def save_file(self) -> None:
        """Save the current list to a csv file."""
        current_time = datetime.now().strftime("%Y%m%d_%H%M")
        base_name = self.csv_path.split(".")[0]
        saved_name = f"{base_name}_{current_time}.csv"
        self.label_df.to_csv(saved_name, index=False)

    def rotate_image(self) -> None:
        """Rotate the current image."""
        rotated_image = self.image.rotate(90, expand=True)
        rotated_image.save(self.path)

    def delete_item(self):
        """Delete the current row."""
        self.label_df.drop(self.index, inplace=True)
        self.label_df.reset_index(drop=True, inplace=True)

    def set_text(self, text: str) -> None:
        """Set the text of the current image."""
        self.label_df.loc[self.index, self.text_column_name] = text

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

    def sort_index(self) -> None:
        """Sort the index of datafrane."""
        self.label_df = self.label_df.sort_index()

    def sort(self, by: str) -> None:
        """Sort the dataframe by the given column."""
        self.label_df = self.label_df.sort_values(by=by)
