#!/usr/bin/env python

import argparse
import collections
import contextlib
import logging
import os
import sys

import fuzzywuzzy.fuzz as fuzz

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
    data = sorted([(history[p], p) for p in history], reverse=True)
    with open(filename, 'w') as fp:
        for count, path in data:
            fp.write('%d %s\n' % (count, path))


def rank_paths(history, path, threshold=40):
    # Match the path assuming that it is an absolute path
    abs_results = [(fuzz.ratio(k, path), k) for k in history]
    if logger.getEffectiveLevel() <= logging.DEBUG:
        abs_results.sort(reverse=True)
        for result in abs_results:
            logger.debug('{} {}'.format(*result))

    # Match the path assuming that it is relative to the current working
    # directory
    augmented = os.path.join(os.getcwd(), path)
    rel_results = [(fuzz.ratio(k, augmented), k) for k in history]

    # Combine the results
    results = abs_results + rel_results
    results.sort(reverse=True)

    # Filter out low scoring results and duplicates
    paths = []
    for score, path in results:
        if score > threshold and path not in paths:
            paths.append(path)

    return paths


def main(argv=sys.argv[1:]):
    logging.basicConfig(format='%(asctime)-15s %(message)s')

    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--add', action='store_true')
    parser.add_argument('-l', '--list', action='store_true')
    parser.add_argument('-c', '--clear', action='store_true')
    parser.add_argument('-r', '--refresh', action='store_true')
    parser.add_argument('-m', '--match', action='store_true')
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

    elif args.match:
        with open_history(args.file) as history:
            path = args.paths[0] if args.paths else os.getcwd()
            for result in rank_paths(history, path):
                print(result)

    elif args.list:
        history = read_history(args.file)
        paths = sorted(history.keys(), key=lambda p: history[p], reverse=True)
        for path in paths:
            print(path)


if __name__ == "__main__":
    main()
