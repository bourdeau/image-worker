import os
import glob
import re
from shutil import copyfile
from PIL import Image
from multiprocessing import Pool


class Worker:

    def __init__(self, source: str, destination: str, quality: int, sizes=None):
        self.poolsize = 8
        self.sourceDir = source
        self.destinationDir = destination
        if quality:
            self.quality = quality
        else:
            self.quality = 100
        if sizes:
            self.sizes = sizes
        else:
            self.sizes = [1280, 960, 760, 640, 480, 320, 240]

    def main(self):
        self.__checkArguments()
        print('SOURCE: ' + self.sourceDir)
        print('DESTINATION : ' + self.destinationDir)
        print('#####################################')
        self.__run()

    def __checkArguments(self):
        if not os.path.isdir(self.sourceDir):
            raise Exception('Directory "' + self.sourceDir + '" doesn\'t exist!')
        if not os.path.isdir(self.destinationDir):
            raise Exception('Directory "' + self.destinationDir + '" doesn\'t exist!')
        if self.quality < 0 or self.quality > 100:
            raise ValueError('Quality must be between 0 and 100')
        for size in self.sizes:
            if size < 0 or size > 5000:
                raise ValueError('Size must be between 0 and 5000')

    def __run(self):
        """
        Main
        """
        pool = Pool(processes=self.poolsize)

        images = self.__getImagesFromDir()

        total = len(images) * len(self.sizes)
        print('Resizing ' + str(len(images)) + ' images in ' + str(len(self.sizes)) + ' dimensions')
        print('TOTAL:  ' + str(total) + ' images to create')

        for image in images:
            for size in self.sizes:
                try:
                    pool.apply_async(self.resize, (image, size))
                except OSError as e:
                    print(e)
        pool.close()
        pool.join()

    def __isWritable(self, path: str):
        """
        Check if directory is writable
        """
        if os.access(path, os.W_OK):
            return True
        else:
            print('ERROR: "' + path + '" is not writable!')
            raise

    def __getImagesFromDir(self):
        """
        Get the original images paths from dir
        """
        originals = []
        try:
            images = glob.glob(self.sourceDir + '/**/*.jpg', recursive=True)
        except IOError as e:
            print(e)
            raise

        for image in images:
            match = re.search('\/(.*)\.jpg', image)
            if (match):
                originals.append(image)

        return originals

    def resize(self, imagePath, size):
        """
        Resize the image and save it (must be public for Pool)
        """
        imageName = re.search('\/([A-Za-z0-9-_]*)\.jpg', imagePath).group(1)

        try:
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
            image.close()
            newPath = self.destinationDir + '/' + str(size)
            # Create directory with appropriate size
            if not os.path.exists(newPath):
                os.makedirs(newPath)

            # Save the image
            newImageName = newPath + '/' + imageName + '.jpg'
            im2.save(newImageName, format='JPEG', optimize=True, quality=self.quality)
            im2.close()
        except Exception as e:
            print('Error while resizing: ' + e)
