import os
import glob
import re
import MySQLdb
from shutil import copyfile
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
        Run resize in Multiprocessing
        """
        # It's easier to ask for forgiveness than for permission
        # self.__isWritable(self.destinationDir)
        pool = Pool(processes=self.poolsize)
        if self.fromDB:
            images = self.__getImagesFromDB()
        else:
            images = self.__getImagesFromDir()

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

    def __isReadable(self, file: str):
        """
        Check if a file is readable
        """
        if os.access(file, os.R_OK):
            return True
        else:
            print('ERROR: "' + file + '" is not readable!')
            raise

    def __getImagesFromDir(self):
        """
        Get the original images paths from dir
        """
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
                self.__isReadable(image)
                originals.append(image)

        total = len(originals)*len(self.sizes)
        print('Resizing ' + str(len(originals)) + ' images in '+str(len(self.sizes)) + ' dimensions')
        print('TOTAL:  ' + str(total) + ' images to create')

        return originals

    def __getImagesFromDB(self):
        """
        Get the original images paths from dir
        """
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
                    self.__isReadable(image)
                    originals.append(image)
                except Exception as e:
                    print('IMAGE ' + image + ' exist in DB but not as a file')
        db.close()

        return originals

    def resize(self, imagePath, size):
        """
        Resize the image and save it (must be public for Pool)
        """
        # Copy file first
        backupOriginalDir = self.destinationDir + '/originals'
        if not os.path.exists(backupOriginalDir):
            os.makedirs(backupOriginalDir)

        imageName = re.search('\/([A-Za-z0-9]*)\.jpg', imagePath).group(1)
        copyfile(imagePath, backupOriginalDir + '/' + imageName+'.jpg')

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

            # Save the image
            newImageName = newPath+'/'+imageName+'.jpg'
            im2.save(newImageName, format='JPEG', optimize=True, quality=self.quality)
            im2.close()
        except Exception as e:
            print('Error while resizing: '+e)
