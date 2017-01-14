#!/usr/bin/python3.5
import sys

from worker import Worker

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('You must provide 2 arguments')
        raise
    worker = Worker(sys.argv[1], sys.argv[2])
    worker.main()
