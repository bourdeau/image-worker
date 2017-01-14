#!/usr/bin/python3.5

import os, glob, re
from PIL import Image
from multiprocessing import Pool


class Worker:

    def __init__(self, source, destination):
        self.poolsize = 8
        self.sourceDir = source
        self.destinationDir = destination
        self.quality = 80
        self.sizes = [
            1280,
            960,
            760,
            640,
            480,
            320,
            240,
        ]

    """
    Main
    """
    def main(self):
        if not os.path.isdir(self.sourceDir):
            print('Directory "' + self.sourceDir + '" doesn\'t exist!')
            raise
        if not os.path.isdir(self.destinationDir):
            print('Directory "' + self.destinationDir + '" doesn\'t exist!')
            raise

        print('SOURCE: ' + self.sourceDir)
        print('DESTINATION : ' + self.destinationDir)
        print('#####################################')
        self.run()

    """
    Run resize in Multiprocessing
    """
    def run(self):
        # It's easier to ask for forgiveness than for permission
        # self.isWritable(self.destinationDir)
        pool = Pool(processes=self.poolsize)
        images = self.getImages()
        for image in images:
            for size in self.sizes:
                try:
                    pool.apply_async(self.resize, (image, size))
                except OSError as e:
                    print(e)
        pool.close()
        pool.join()

    """
    Check if directory is writable
    """
    def isWritable(self, path):
        if os.access(path, os.W_OK):
            return True
        else:
            print('ERROR: "' + path + '" is not writable!')
            raise

    """
    Check if a file is readable
    """
    def isReadable(self, file):
        if os.access(file, os.R_OK):
            return True
        else:
            print('ERROR: "' + file + '" is not readable!')
            raise

    """
    Get the original images paths
    """
    def getImages(self):
        originals = []
        try:
            images = glob.glob(self.sourceDir+'/**/*.jpg', recursive=True)
        except IOError as e:
            print(e)
            raise

        for image in images:
            match = re.search('\/([A-Za-z0-9]*)\.jpg', image)
            if (match):
                # Glob should raise an exception if the image is not readle but
                # I rather take an extra security
                self.isReadable(image)
                originals.append(image)

        total = len(originals)*len(self.sizes)
        print('Resizing ' + str(len(originals)) + ' images in '+str(len(self.sizes)) + ' dimensions')
        print('TOTAL:  ' + str(total) + ' images to create')
        return originals

    """
    Resize the image and save it
    """
    def resize(self, imagePath, size):
        try:
            image = Image.open(imagePath).convert('RGB')
            # Bug https://github.com/python-pillow/Pillow/issues/1237
            # image = imageLib.copy()
            # imageLib.close()
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
            newPath = self.destinationDir+'/'+str(size)
            # Create directory with appropriate size
            if not os.path.exists(newPath):
                os.makedirs(newPath)

            newName = re.search('\/([A-Za-z0-9]*)\.jpg', imagePath).group(1)

            # Save the image
            newImageName = newPath+'/'+newName+'.jpg'
            im2.save(newImageName, optimize=True, quality=self.quality)
            im2.close()
        except Exception as e:
            print('Error while resizing: '+e)
