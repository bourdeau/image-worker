
import os, glob, re
from PIL import Image
from multiprocessing import Pool, Lock

lock = Lock()


class Worker:

    GREEN = '\033[92m'
    ASK = '\033[93m'
    END = '\033[0m'

    def __init__(self):
        self.multiprocessing = True
        self.poolsize = 1
        self.totalImageProcessed = 0
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

    def main(self):
        images = self.getImages()
        if self.multiprocessing:
            self.multiplex(images)
        else:
            for image in images:
                for size in self.sizes:
                    self.resize(image, size)

    """
    Run resize in Multiprocessing
    """
    def multiplex(self, images):
        nb = 0
        for image in images:
            pool = Pool(processes=self.poolsize)
            for size in self.sizes:
                try:
                    print(self.ASK+'Ask process to resize #'+str(nb)+self.END)
                    pool.apply_async(self.resize, (image, size, nb))
                    nb += 1
                except OSError as e:
                    with lock:
                        print(e)
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
    def resize(self, imagePath, size, nb):
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
        newPath = self.cdnNewPath+'/'+str(size)
        # Create directory with appropriate size
        if not os.path.exists(newPath):
            os.makedirs(newPath)

        newName = re.search('\/([A-Za-z0-9]*)\.jpg', imagePath).group(1)

        # Save the image
        newImageName = newPath+'/'+newName+'.jpg'
        im2.save(newImageName, optimize=True, quality=self.quality)
        print(self.GREEN+'Process ~> #'+str(nb)+' resized ('+imagePath+')'+self.END)

if __name__ == "__main__":
    test = Worker()
    test.main()
