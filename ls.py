import os
import sys


def list_dir(path="."):
    return os.listdir(path)


def main(args=None):
    args = args or sys.argv[1:]
    path = args[0] if args else "."
    for name in sorted(list_dir(path)):
        print(name)


if __name__ == "__main__":
    main()