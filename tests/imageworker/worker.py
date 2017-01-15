from imageworker.worker import Worker
import unittest


class WorkerTest(unittest.TestCase):

    def test_directories(self):
        test = Worker('/idonotexisthopefully', '/donotexisteither', 80, False, [120])

if __name__ == '__main__':
    unittest.main()
