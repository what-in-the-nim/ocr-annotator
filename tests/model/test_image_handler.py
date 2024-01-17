import pytest
from PIL import Image

from nimocr.model import ImageHandler  # Replace 'your_module' with the actual module name

@pytest.fixture
def image_handler():
    return ImageHandler()

def test_open_nonexistent_file(image_handler):
    # Provide a path to a nonexistent image file
    nonexistent_image_path = "path/to/nonexistent/image.jpg"
    
    # Check if FileNotFoundError is raised
    result = image_handler.open(nonexistent_image_path)
    assert isinstance(result, FileNotFoundError)

def test_rotate(image_handler):
    # Create a sample image
    image = Image.new("RGB", (100, 100), "white")

    # Perform a rotation
    rotated_image = image_handler.rotate(image, degree=90)

    # Check if the rotated image has the expected size
    assert rotated_image.size == (100, 100)

def test_resize(image_handler):
    # Create a sample image
    image = Image.new("RGB", (100, 100), "white")

    # Perform a resize
    resized_image = image_handler.resize(image, size=(50, 50))

    # Check if the resized image has the expected size
    assert resized_image.size == (50, 50)

def test_scale(image_handler):
    # Create a sample image
    image = Image.new("RGB", (100, 100), "white")

    # Perform a scaling
    scaled_image = image_handler.scale(image, scale=0.5)

    # Check if the scaled image has the expected size
    assert scaled_image.size == (50, 50)

def test_fit(image_handler):
    # Create a sample image
    image = Image.new("RGB", (100, 100), "white")

    # Perform a fit operation
    fitted_image = image_handler.fit(image, size=(50, 50))

    # Check if the fitted image has the expected size
    assert fitted_image.size == (50, 50)
