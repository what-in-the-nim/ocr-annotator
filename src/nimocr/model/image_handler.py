from PIL import Image

class ImageHandler:
    @staticmethod
    def open(path: str) -> Image.Image:
        """Return the current image."""
        try:
            image = Image.open(path)
            rgb_image = image.convert("RGB")
            return rgb_image
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {path}, Please browse directory to solve this.")
        
    def rotate(image: Image.Image, degree: int = 90) -> Image.Image:
        """Rotate the current image."""
        rotated_image = image.rotate(degree, expand=True)
        return rotated_image