#!/usr/bin/python3.5
import argparse
from worker import Worker

if __name__ == "__main__":
    # Arguments parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", help="Source image directory", required=True, type=str)
    parser.add_argument("-d", help="Destination image directory", required=True, type=str)
    parser.add_argument("-q", help="Image quality (0 to 100)", required=False, type=int)
    parser.add_argument('-si', nargs='+', help='<Required> List of sizes', required=False, type=int)

    args = parser.parse_args()

    # Main instance
    worker = Worker(args.s, args.d, args.q, args.si)
    worker.main()
