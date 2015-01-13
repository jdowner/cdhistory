#!/usr/bin/env python

import argparse
import collections
import contextlib
import heapq
import logging
import os
import re
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
                    count, path = line.split(None, 1)
                    history[path] = int(count)

    return history


def validate_history(history):
    remove = []
    for path in history:
        if not os.path.exists(path):
            remove.append(path)

    for path in remove:
        del history[path]


def write_history(filename, history):
    data = sorted([(history[p], p) for p in history], reverse=True)
    with open(filename, 'w') as fp:
        for count, path in data:
            fp.write('%d %s\n' % (count, path))


def rank_paths(history, test, limit=10):
    pattern = re.compile('(?=(' + '.*?'.join(re.escape(c) for c in test) + '))')

    def score(match, path):
        length = match.end(1) - match.start(1)
        if length == 0:
            return (0, 0)

        lscore = 1.0 / length
        fscore = history[path]
        return (lscore, fscore)

    results = []
    for path in history:
        matches = [score(m, path) for m in pattern.finditer(path)]
        if matches:
            results.append((max(matches), path))
            logger.debug('score {}: {}'.format(*results[-1]))

    return [path for _, path in heapq.nlargest(limit, results)]


def main(argv=sys.argv[1:]):
    logging.basicConfig(format='%(asctime)-15s %(message)s')

    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--add', action='store_true')
    parser.add_argument('-l', '--list', action='store_true')
    parser.add_argument('-c', '--clear', action='store_true')
    parser.add_argument('-r', '--refresh', action='store_true')
    parser.add_argument('-m', '--match', action='store_true')
    parser.add_argument('-n', '--max-results', type=int, default=10)
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

    elif args.refresh:
        with open_history(args.file) as history:
            validate_history(history)

    if args.add:
        with open_history(args.file) as history:
            for path in args.paths:
                rpath = os.path.realpath(path)
                if os.path.exists(rpath):
                    history[rpath] += 1

    elif args.match:
        with open_history(args.file) as history:
            path = args.paths[0] if args.paths else os.getcwd()
            for result in rank_paths(history, path, limit=args.max_results):
                print(result)

    elif args.list:
        history = read_history(args.file)
        paths = sorted(history.keys(), key=lambda p: history[p], reverse=True)
        for path in paths:
            print(path)


if __name__ == "__main__":
    main()
