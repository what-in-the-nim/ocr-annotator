import os
import os.path as op
import pytest
import pandas as pd

from nimocr.model import ImageListModel

@pytest.fixture
def image_list_model():
    return ImageListModel()

def test_load_file(image_list_model):
    # Create a temporary CSV file
    temp_file = op.join(op.dirname(__file__), "temp_file.csv")

    # Create a sample DataFrame
    data = {'path': ['image1.jpg', 'image2.jpg'],
            'text': ['Text1', 'Text2']}
    df = pd.DataFrame(data)

    try:
        # Save the sample DataFrame to the temporary file
        df.to_csv(temp_file, index=False)

        # Load the CSV file using ImageListModel
        image_list_model.load_file(temp_file)

        # Check if the loaded DataFrame is equal to the original DataFrame
        pd.testing.assert_frame_equal(df, image_list_model.df)

    finally:
        # Clean up the temporary file
        if op.exists(temp_file):
            os.remove(temp_file)
