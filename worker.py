#!/usr/bin/python3.5

import os, glob, re
from PIL import Image
from multiprocessing import Pool, Lock


class Worker:

    def __init__(self):
        self.poolsize = 8
        self.sourceDir = "/home/ph/Bureau/cdn_squarebreak"
        self.destinationPath = "/home/ph/Bureau/cdn2_squarebreak"
        self.quality = 80
        self.sizes = [
            250,
            1200,
            800,
            650,
            400,
            300,
        ]

    """
    Run resize in Multiprocessing
    """
    def main(self):
        pool = Pool(processes=self.poolsize)
        images = self.getImages()
        for size in self.sizes:
            for image in images:
                try:
                    pool.apply_async(self.resize, (image, size))
                except OSError as e:
                    print(e)
        pool.close()
        pool.join()

    """
    Get the original images paths
    """
    def getImages(self):
        originals = []
        images = glob.glob(self.sourceDir+'/**/*.jpg', recursive=True)
        for image in images:
            match = re.search('\/([A-Za-z0-9]*)\.jpg', image)
            if (match):
                originals.append(image)

        total = len(originals)*len(self.sizes)
        print ('Resizing ' + str(len(originals)) + ' images in '+str(len(self.sizes)) + ' dimensions')
        print ('TOTAL:  ' + str(total) + ' to create')
        return originals

    """
    Resize the image and save it
    """
    def resize(self, imagePath, size):
        try:
            imageLib = Image.open(imagePath).convert('RGB')
            # Bug https://github.com/python-pillow/Pillow/issues/1237
            image = imageLib.copy()
            imageLib.close()
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
            newPath = self.destinationPath+'/'+str(size)
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
