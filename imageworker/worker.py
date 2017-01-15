#!/usr/bin/python3.5
import os
import glob
import re
import MySQLdb
from imageworker import utils
from PIL import Image
from multiprocessing import Pool


class Worker:

    def __init__(self, source: str, destination: str, quality: int, fromDB, sizes=None):
        self.poolsize = 8
        self.sourceDir = source
        self.destinationDir = destination
        self.fromDB = fromDB
        if quality:
            self.quality = quality
        else:
            self.quality = 100
        if sizes:
            self.sizes = sizes
        else:
            self.sizes = [1280, 960, 760, 640, 480, 320, 240]

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

    def run(self):
        """
        Run resize in Multiprocessing
        """
        # It's easier to ask for forgiveness than for permission
        # self.isWritable(self.destinationDir)
        pool = Pool(processes=self.poolsize)
        if self.fromDB:
            images = self.getImagesFromDB()
        else:
            self.getImagesFromDir()

        for image in images:
            for size in self.sizes:
                try:
                    pool.apply_async(self.resize, (image, size))
                except OSError as e:
                    print(e)
        pool.close()
        pool.join()

    def isWritable(self, path: str) -> bool:
        """
        Check if directory is writable
        """
        if os.access(path, os.W_OK):
            return True
        else:
            print('ERROR: "' + path + '" is not writable!')
            raise

    def isReadable(self, file: str) -> bool:
        """
        Check if a file is readable
        """
        if os.access(file, os.R_OK):
            return True
        else:
            print('ERROR: "' + file + '" is not readable!')
            raise

    """
    Get the original images paths from dir
    """
    def getImagesFromDir(self) -> bool:
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
    Get the original images paths from dir
    """
    def getImagesFromDB(self):
        config = utils.getConfig()
        db = MySQLdb.connect(host=config['database_host'], user=config['database_user'], passwd=config['database_password'], db=config['database_name'])
        cur = db.cursor()

        cur.execute("SELECT local_key FROM media")

        originals = []
        for rows in cur.fetchall():
            for localKey in rows:
                prefix = localKey[:2]
                image = self.sourceDir+'/'+prefix+'/'+localKey
                try:
                    self.isReadable(image)
                    originals.append(image)
                except Exception as e:
                    print('IMAGE ' + image + ' exist in DB but not as a file')
        db.close()

        return originals

    """
    Resize the image and save it
    """
    def resize(self, imagePath, size):
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
            newPath = self.destinationDir+'/'+str(size)
            # Create directory with appropriate size
            if not os.path.exists(newPath):
                os.makedirs(newPath)

            newName = re.search('\/([A-Za-z0-9]*)\.jpg', imagePath).group(1)

            # Save the image
            newImageName = newPath+'/'+newName+'.jpg'
            im2.save(newImageName, format='JPEG', optimize=True, quality=self.quality)
            im2.close()
        except Exception as e:
            print('Error while resizing: '+e)
