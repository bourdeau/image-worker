
import glob
import os
import re
from PIL import Image
from multiprocessing import Pool


class Worker:

    def __init__(self):
        self.poolsize = 2
        self.cdnPath = "/home/ph/Bureau/cdn_squarebreak"
        self.cdnNewPath = "/home/ph/Bureau/PYTHON_cdn_squarebreak"
        self.quality = 80
        self.sizes = [
            1200,
            800,
            650,
            400,
            300,
            250,
        ]

    """
    Run resize in Multiprocessing
    """
    def main(self):
        images = self.getImages()
        for image in images:
            pool = Pool(self.poolsize)
            for size in self.sizes:
                pool.apply_async(self.resize, (image, size))
        pool.close()
        pool.join()

    """
    Get the original images paths
    """
    def getImages(self):
        originals = []
        images = glob.glob(self.cdnPath+'/**/*.jpg', recursive=True)
        for image in images:
            match = re.search('\/([A-Za-z0-9]*)\.jpg', image)
            if (match):
                originals.append(image)

        return originals

    """
    Resize the image and save it
    """
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
        newPath = self.cdnNewPath+'/'+str(size)
        # Create directory with appropriate size
        if not os.path.exists(newPath):
            os.makedirs(newPath)

        newName = re.search('\/([A-Za-z0-9]*)\.jpg', imagePath).group(1)

        # Save the image
        im2.save(newPath+'/'+newName+'.jpg', optimize=True, quality=self.quality)

if __name__ == "__main__":
    test = Worker()
    test.main()
