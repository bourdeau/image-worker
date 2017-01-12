
import glob, sys
import os
import re
from PIL import Image


class Worker:

    def __init__(self):
        self.CDN_PATH = "/home/ph/Bureau/cdn_squarebreak"
        self.CDN_NEW_PATH = "/home/ph/Bureau/PYTHON_cdn_squarebreak"
        self.QUALITY = 80
        self.sizes = [
            1200,
            800,
            650,
            400,
            300,
            250,
        ]

    def main(self):
        images = self.getImages()
        for image in images:
            for size in self.sizes:
                self.resize(image, size)

    def getImages(self):
        originals = []
        images = glob.glob(self.CDN_PATH+'/**/*.jpg', recursive=True)
        for image in images:
            match = re.search('\/([A-Za-z0-9]*)\.jpg', image)
            if (match):
                originals.append(image)

        return originals

    def resize(self, imagePath, size):
        image = Image.open(imagePath).convert('RGB')
        originalWidth, originalHeight = image.size
        ratio = originalWidth / originalHeight
        # Portrait or Landscape
        if ratio > 1:
            width = size
            height = int(width / ratio)
        else:
            height = size
            width = int(height * ratio)

        im2 = image.resize((width, height), Image.ANTIALIAS)
        newPath = self.CDN_NEW_PATH+'/'+str(size)
        # Create directory with appropriate size
        if not os.path.exists(newPath):
            os.makedirs(newPath)

        newName = re.search('\/([A-Za-z0-9]*)\.jpg', imagePath).group(1)

        # Save the image
        im2.save(newPath+'/'+newName+'.jpg', optimize=True, quality=self.QUALITY)

if __name__ == "__main__":
    test = Worker()
    test.main()
