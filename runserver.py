#!/usr/bin/env python

from sys import argv, exit, stderr
from regserver import app
import argparse


def main(argv):
    DATABASE_NAME = "reg.sqlite"

    # Create parser that has a description of the program and port positional argument
    parser = argparse.ArgumentParser(
        description='The registrar application', allow_abbrev=False)
    parser.add_argument(
        "port", type=int, help="the port at which the server should listen", nargs=1)
    # args = parser.parse_args()

    # grab the port and run the app, unless the port is already in use
    port = int(argv[1])
    try:
        app.run(host='0.0.0.0', port=port, debug=True)
    except Exception:
        print(f"{argv[0]}: Address already in use", file=stderr)
        exit(1)

if __name__ == '__main__':
    main(argv)
