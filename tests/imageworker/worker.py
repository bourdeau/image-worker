from imageworker.worker import Worker
import unittest


class WorkerTest(unittest.TestCase):

    def test_invalid_directories(self):
        test = Worker('/idonotexisthopefully', '/donotexisteither', -80, False, [120])
        self.assertRaises(Exception, test.main)

    def test_valid_directories(self):
        test = Worker('./tests/imageworker/images-dest', './tests/imageworker/images-source', 80, False, [120])
        try:
            test.main()
        except Exception as e:
            print(e)

    def test_invalid_quality(self):
        test = Worker('./tests/imageworker/images-dest', './tests/imageworker/images-source', -1, False, [120])
        self.assertRaises(Exception, test.main)
        test = Worker('./tests/imageworker/images-dest', './tests/imageworker/images-source', 101, False, [120])
        self.assertRaises(Exception, test.main)


if __name__ == '__main__':
    unittest.main()
