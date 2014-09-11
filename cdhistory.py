#!/usr/bin/env python

import argparse
import collections
import os
import sys

HISTORY_FILE = os.path.realpath(os.path.expanduser('~/.cdhistory'))

def read_history(filename):
    history = collections.Counter()
    if os.path.exists(filename):
        with open(filename) as fp:
            for line in fp:
                if line:
                    count, path = line.split()
                    history[path] = int(count)

    return history

def write_history(filename, history):
    with open(filename, 'w') as fp:
        for path in history:
            fp.write('%d %s\n' % (history[path], path))

def add_to_history(path):
    history = read_history(HISTORY_FILE)
    history[os.path.realpath(path)] += 1
    write_history(HISTORY_FILE, history)

def is_valid_path(path):
    if path.startswith('..'):
        return False
    if path == '-':
        return False
    return True

def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--add', action='store_true')
    parser.add_argument('paths', nargs=argparse.REMAINDER)

    args = parser.parse_args(argv)

    if args.add:
        for path in args.paths:
            if is_valid_path(path):
                add_to_history(path)


if __name__ == "__main__":
    main()
