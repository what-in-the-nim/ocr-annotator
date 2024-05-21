import os
from tempfile import NamedTemporaryFile

import pandas as pd
import pytest

from nimocr.model import FileHandler

@pytest.fixture
def file_handler():
    return FileHandler()


def test_get_basename():
    assert FileHandler.get_basename("/path/to/file.txt") == "file"


def test_get_delimiter():
    assert FileHandler.get_delimiter("csv") == ","
    assert FileHandler.get_delimiter("tsv") == "\t"
    with pytest.raises(ValueError):
        FileHandler.get_delimiter("txt")


def test_get_quotechar():
    assert FileHandler.get_quotechar("csv") == '"'
    assert FileHandler.get_quotechar("tsv") == ""
    with pytest.raises(ValueError):
        FileHandler.get_quotechar("txt")


def test_get_extension():
    assert FileHandler.get_extension("/path/to/file.txt") == "txt"


def test_load_and_save(file_handler):
    # Create a temporary CSV file
    temp_file = NamedTemporaryFile(suffix=".csv", delete=False)
    temp_file_path = temp_file.name
    temp_file.close()

    # Create a sample DataFrame
    data = {"col1": [1, 2, 3], "col2": ["a", "b", "c"]}
    df = pd.DataFrame(data)

    try:
        # Save the DataFrame to the temporary file
        df.to_csv(temp_file_path, index=False)

        # Load the DataFrame from the temporary file
        loaded_df = file_handler.load(temp_file_path)

        # Check if the loaded DataFrame is equal to the original DataFrame
        pd.testing.assert_frame_equal(df, loaded_df)

    finally:
        # Clean up the temporary file
        os.remove(temp_file_path)
