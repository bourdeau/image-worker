import os
import re
from PIL import Image as PILImage


class Image:
    """Handle image processing."""

    def __init__(self, img_path: str):
        """Init."""
        self.img_path = img_path

    def resize(self, dest_dir: str, size: int, quality: int = 100) -> None:
        """Resize the image and save it (method must be public for Pool)."""
        img_name = re.search('\/([A-Za-z0-9-_]*)\.jpg', self.img_path).group(1)

        try:
            image = PILImage.open(self.img_path).convert('RGB')
            size_width, size_height = image.size
            ratio = size_width / size_height
            # Portrait or Landscape
            if ratio > 1:
                width = size
                height = int(width / ratio)
            else:
                height = size
                width = int(height * ratio)

            im2 = image.resize((width, height), PILImage.ANTIALIAS)
            image.close()
            newPath = dest_dir + '/' + str(size)
            # Create directory with appropriate size
            if not os.path.exists(newPath):
                os.makedirs(newPath)

            # Save the image
            newImageName = newPath + '/' + img_name + '.jpg'
            im2.save(newImageName, format='JPEG', optimize=True, quality=quality)
            im2.close()
        except Exception as e:
            print('Error while resizing: ' + e)
