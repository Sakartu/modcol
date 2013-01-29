#!/usr/bin/env python3
from argparse import ArgumentParser
import subprocess
import shlex
import csv
import sys


def main():
    args = parse_args()
    if not args.files:
        args.files = [sys.stdin]
    else:
        args.files = map(open, args.files)

    args.delimiter = bytes(args.delimiter, 'utf-8').decode('unicode_escape')
    args.columns = list(map(int, args.columns.split(',')))
    for f in args.files:
        reader = csv.reader(f, delimiter=args.delimiter)
        for line in reader:
            handle_line(line, args)


def handle_line(columns, args):
    for c in args.columns:
        proc = subprocess.Popen(shlex.split(args.command), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        (outmsg, errmsg) = proc.communicate(bytes(columns[c - 1] + '\n', 'utf-8'))
        if errmsg:
            sys.stderr.write(errmsg)
            sys.stderr.flush()
            sys.exit(1)
        columns[c - 1] = outmsg[:-1]  # remove newline
    sys.stdout.write(args.delimiter.join(columns) + '\n')
    sys.stdout.flush()


def parse_args():
    parser = ArgumentParser(description='An extension to the default GNU toolchain, allowing you to modify columns of csv-like input.')
    parser.add_argument('-d', '--delimiter', default=',', help='The delimiter used to delimit columns, "," by default.')
    parser.add_argument('command', help='The command that will be run on the specified column.')
    parser.add_argument('columns', help='The columns that will be fed the command, separated by a comma.')
    parser.add_argument('files', nargs='*', default=[], help='The input files to read. If no files are provided, read from stdin.')
    return parser.parse_args()


if __name__ == '__main__':
    main()
