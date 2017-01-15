import os, sys
import unittest
import shutil
from imageworker.worker import Worker


class WorkerTest(unittest.TestCase):

    def test_invalid_directories(self):
        test = Worker('/idonotexisthopefully', '/donotexisteither', -80, False, [100])
        self.assertRaises(Exception, test.main)

    def test_invalid_quality(self):
        test = Worker('./tests/imageworker/images-source', './tests/imageworker/images-dest', -1, False, [300])
        self.assertRaises(Exception, test.main)
        test = Worker('./tests/imageworker/images-source', './tests/imageworker/images-dest', 101, False, [400])
        self.assertRaises(Exception, test.main)

    def test_invalid_dimensions(self):
        test = Worker('./tests/imageworker/images-source', './tests/imageworker/images-dest', 80, False, 'adazd')
        self.assertRaises(Exception, test.main)
        test = Worker('./tests/imageworker/images-source', './tests/imageworker/images-dest', 80, False, [7894949])
        self.assertRaises(Exception, test.main)

    def test_invalid_resizing(self):
        test = Worker('./tests/imageworker/images-source', './tests/imageworker/images-dest', 80, False, [600])
        test.main()
        if not os.path.isfile('./tests/imageworker/images-dest/originals/rabbit.jpg'):
            raise Exception('Copying original file failed!')
        if not os.path.isfile('./tests/imageworker/images-dest/600/rabbit.jpg'):
            raise Exception('Copying original file failed!')

        for the_file in os.listdir('./tests/imageworker/images-dest'):
            shutil.rmtree('./tests/imageworker/images-dest/' + the_file)

if __name__ == '__main__':
    unittest.main()
