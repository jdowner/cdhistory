#!/usr/bin/env python

import argparse
import collections
import contextlib
import logging
import os
import sys

logger = logging.getLogger(__name__)


@contextlib.contextmanager
def open_history(filename):
    history = read_history(filename)
    yield history
    write_history(filename, history)


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

def main(argv=sys.argv[1:]):
    logging.basicConfig(format='%(asctime)-15s %(message)s')

    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--add', action='store_true')
    parser.add_argument('-l', '--list', action='store_true')
    parser.add_argument('-c', '--clear', action='store_true')
    parser.add_argument('-r', '--refresh', action='store_true')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-f', '--file',
            default=os.path.realpath(os.path.expanduser('~/.cdhistory')))
    parser.add_argument('paths', nargs=argparse.REMAINDER)

    args = parser.parse_args(argv)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if args.verbose else logging.INFO)

    if args.clear:
        if os.path.isfile(args.file):
            os.remove(args.file)

    if args.add:
        with open_history(args.file) as history:
            for path in args.paths:
                rpath = os.path.realpath(path)
                if os.path.exists(rpath):
                    history[rpath] += 1

    elif args.refresh:
        with open_history(args.file) as history:
            remove = [p for p in history if not os.path.exists(p)]
            for path in remove:
                del history[path]


    elif args.list:
        history = read_history(args.file)
        paths = sorted(history.keys(), key=lambda k: history[k])
        for path in paths:
            print(path)


if __name__ == "__main__":
    main()
