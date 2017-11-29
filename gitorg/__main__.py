import sys
from . import cli

def main():
    exit(cli.run(sys.argv[1:]))

if __name__ == "__main__":
    main()
