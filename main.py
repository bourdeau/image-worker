import argparse
from imageworker.worker import Worker

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s',
        help='Source image directory',
        required=True,
        type=str,
    )
    parser.add_argument(
        '-d',
        help='Destination image directory',
        required=True,
        type=str
    )
    parser.add_argument(
        '-q',
        help='Image quality (0 to 100)',
        required=False,
        type=int,
        default=100
    )
    parser.add_argument(
        '-si',
        help='List of sizes',
        required=False,
        nargs='+',
        type=int,
        default=[1280, 960, 760, 640, 480, 320, 240]
    )

    args = parser.parse_args()

    Worker(args.s, args.d, args.q, args.si).main()
