import logging
import os.path as op
import math

from PIL import Image

logger = logging.getLogger(__name__)


class ImageHandler:
    @staticmethod
    def open(path: str) -> Image.Image:
        """Return the current image."""
        if not op.exists(path):
            return FileNotFoundError(f"File not found: {path}, Please browse directory to solve this.")

        image = Image.open(path)
        rgb_image = image.convert("RGB")
        return rgb_image

    @staticmethod
    def rotate(image: Image.Image, degree: int = 90) -> Image.Image:
        """Rotate the current image."""
        rotated_image = image.rotate(degree, expand=True)
        return rotated_image

    @staticmethod
    def resize(image: Image.Image, size: tuple[int, int]) -> Image.Image:
        """Resize the current image."""
        resized_image = image.resize(size)
        return resized_image

    @staticmethod
    def scale(image: Image.Image, scale: float) -> Image.Image:
        """Scale the current image."""
        width, height = image.size
        # Calculate the new width and height
        new_width = int(width * scale)
        new_height = int(height * scale)
        # Resize the image
        resized_image = image.resize((new_width, new_height))
        return resized_image

    @staticmethod
    def fit(image: Image.Image, size: tuple[int, int]) -> Image.Image:
        """Fit the current image to target size with aspect ratio."""
        width, height = image.size
        container_width, container_height = size
        logger.info(f"Image size: {width}x{height}")
        logger.info(f"Container size: {container_width}x{container_height}")

        # Calculate the aspect ratio of the image and container
        aspect_ratio = width / height
        container_ratio = container_width / container_height

        # Decide which dimension to scale to fit the container without distortion
        if aspect_ratio > container_ratio:
            # Scale the width to fit the container
            target_width = container_width
            target_height = math.floor(target_width / aspect_ratio)
        else:
            # Scale the height to fit the container
            target_height = container_height
            target_width = math.floor(target_height * aspect_ratio)

        # Resize the image to the target size
        logger.info(f"Target size: {target_width}x{target_height}")
        resized_image = image.resize((target_width, target_height))

        return resized_image
