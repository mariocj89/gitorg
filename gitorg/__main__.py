import sys
from . import cli


if __name__ == "__main__":
    exit(cli.run(sys.argv[1:]))
