#!/usr/bin/env python

import unittest

import cdhistory


class TestHistory(unittest.TestCase):
    def setUp(self):
        self.paths = {
                "/foo/bar/baz": 3,
                "/a/b/c/d/e/f": 4,
                "ara": 2
                }

    def test_matches(self):
        history = cdhistory.History(self.paths)

        results = history.matches("ara")
        self.assertEqual(2, len(results))
        self.assertEqual("ara", results[0])
        self.assertEqual("/foo/bar/baz", results[1])

        results = history.matches("ara", limit=1)
        self.assertEqual(1, len(results))
        self.assertEqual("ara", results[0])
