import os
import unittest
import shutil
from imageworker.worker import Worker


class WorkerTest(unittest.TestCase):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    sourceDir = dir_path + '/images-source'
    destDir = dir_path + '/images-dest'

    def test_invalid_directories(self):
        with self.assertRaises(Exception):
            Worker('/idonotexisthopefully', '/donotexisteither', -80, [100])

    def test_resized_image_exist(self):
        test = Worker(self.sourceDir, self.destDir, 80, [600])
        test.main()

        if not os.path.isfile(self.destDir + '/600/rabbit.jpg'):
            raise Exception('Copying resized image failed!')

        for the_file in os.listdir(self.destDir):
            if os.path.isdir(self.destDir + '/' + the_file):
                shutil.rmtree(self.destDir + '/' + the_file)

if __name__ == '__main__':
    unittest.main()
