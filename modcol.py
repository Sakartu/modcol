#!/usr/bin/env python3
from argparse import ArgumentParser
import subprocess
import shlex
import sys
import re


def main():
    args = parse_args()
    if not args.files:
        args.files = [sys.stdin]
    else:
        args.files = map(open, args.files)

    for f in args.files:
        for line in f:
            handle_line(line, args)


def handle_line(line, args):
    columns = re.split(args.delimiter, line)
    proc = subprocess.Popen(shlex.split(args.command), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    (outmsg, errmsg) = proc.communicate(columns[args.column - 1] + '\n')
    if errmsg:
        sys.stderr.write(errmsg)
        sys.stderr.flush()
        sys.exit(1)
    columns[args.column - 1] = outmsg[:-1]  # remove newline
    sys.stdout.write(args.delimiter.join(columns))
    sys.stdout.flush()


def parse_args():
    parser = ArgumentParser(description='An extension to the default GNU toolchain, allowing you to modify columns of csv-like files individually.')
    parser.add_argument('-d', '--delimiter', default=',', help='The delimiter used to delimit columns, "," by default.')
    parser.add_argument('command', help='The command that will be run on the specified column.')
    parser.add_argument('column', type=int, help='The column that will be fed the command.')
    parser.add_argument('files', nargs='*', default=[], help='The delimiter used to delimit columns.')
    return parser.parse_args()


if __name__ == '__main__':
    main()
