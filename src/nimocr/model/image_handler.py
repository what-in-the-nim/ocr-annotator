import os.path as op

from PIL import Image


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

        # Calculate the aspect ratio of the image
        aspect_ratio = width / height

        # Calculate the target size of the image based on the aspect ratio and the container size
        target_width = container_width
        target_height = int(target_width / aspect_ratio)

        # If the calculated height is greater than the container height, adjust the target size
        if target_height > container_height:
            target_height = container_height
            target_width = int(target_height * aspect_ratio)

        # Resize the image to the target size
        resized_image = image.resize((target_width, target_height))

        return resized_image
