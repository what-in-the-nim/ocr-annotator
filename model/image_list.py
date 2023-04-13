import pandas as pd
from PIL import Image
from datetime import datetime

class ImageListModel:

    def __init__(self) -> None:
        self.index = 0
        self.label_df = None
        self.csv_path = None
        self.path_column_name = None
        self.label_column_name = None

    @property
    def image(self) -> None:
        return Image.open(self.path).convert("RGB")

    @property
    def text(self) -> str:
        return self.label_df.iloc[self.index][self.label_column_name]

    @property
    def path(self) -> str:
        return self.label_df.iloc[self.index][self.path_column_name]

    @property
    def length(self) -> int:
        return len(self.label_df)

    def _load_csv(self) -> None:
        self.label_df = pd.read_csv(self.csv_path)

    def load_file(self, label_path: str, path_column_name: str = "path", label_column_name: str = "text") -> None:
        """Set the label path and reload the csv file."""
        self.csv_path = label_path
        self.path_column_name = path_column_name
        self.label_column_name = label_column_name

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

    def delete_row(self):
        """Delete the current row."""
        self.label_df.drop(self.index, inplace=True)
        self.label_df.reset_index(drop=True, inplace=True)

    def set_text(self, text: str) -> None:
        """Set the text of the current image."""
        self.label_df.loc[self.index, self.label_column_name] = text

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
