import os
import re
import glob
from multiprocessing import Pool
from imageworker.image import Image


class Worker:
    """Worker."""

    def __init__(self, source: str, destination: str, quality=100, sizes=[1280, 960]):
        self.pool_size = 8
        self.source_dir = source
        self.dest_dir = destination
        self.quality = quality
        self.sizes = sizes

        if not os.path.isdir(self.source_dir):
            raise Exception('Directory "' + self.source_dir + '" doesn\'t exist!')
        if not os.path.isdir(self.dest_dir):
            raise Exception('Directory "' + self.dest_dir + '" doesn\'t exist!')

    def main(self):
        """Run."""
        print('SOURCE: ' + self.source_dir)
        print('DESTINATION : ' + self.dest_dir)
        print('#####################################')

        pool = Pool(processes=self.pool_size)

        images = self.__getImagesFromDir()

        total = len(images) * len(self.sizes)
        print('Resizing ' + str(len(images)) + ' images in ' + str(len(self.sizes)) + ' dimensions')
        print('TOTAL:  ' + str(total) + ' images to create')

        for image in images:
            for size in self.sizes:
                try:
                    newImage = Image(image)
                    pool.apply_async(newImage.resize, (self.dest_dir, size, self.quality))
                except OSError as e:
                    print(e)
        pool.close()
        pool.join()

    def __getImagesFromDir(self):
        """Get the original images paths from dir."""
        originals = []

        images = glob.glob(self.source_dir + '/**/*.jpg', recursive=True)

        for image in images:
            match = re.search('\/(.*)\.jpg', image)
            if (match):
                originals.append(image)

        return originals
