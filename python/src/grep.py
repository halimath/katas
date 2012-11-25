"""
    Another simple kata that focusses on
    - test driven development
    - baby steps
    
    Write a function (grep) that takes a string (the needle) and a list
    of lines (the haystack) and returns a list of all lines that contain
    the needle.
"""

import unittest

def grep (needle, *haystack):
    if not needle:
        raise ValueError("No needle given")
    
    return [line for line in haystack if needle in line.split()]

class GrepTest (unittest.TestCase):
    def test_shouldRaiseValueErrorWhenNoNeedleIsGiven (self):
        self.assertRaises(ValueError, grep, None)
    
    def test_shouldReturnEmptyListWhenNoHaystackLineIsGiven (self):
        self.assertEquals([], grep("foo"))

    def test_shouldReturnEmptyListWhenHaystackWithoutMatchIsGiven (self):
        self.assertEquals([], grep("foo", "bar"))

    def test_shouldReturnListContainingSingleLineWhenHaystackWithMatchingSingleLineIsGiven (self):
        self.assertEquals(["foo"], grep("foo", "foo"))

    def test_shouldReturnListContainingAllMatchingLinesWhenHaystackWithMatchingLinesIsGiven (self):
        self.assertEquals(["foo", "foo"], grep("foo", "foo", "foo"))

    def test_shouldReturnListContainingAllMatchingLinesWhenHaystackWithMatchingLinesAndNonMatchingLinesIsGiven (self):
        self.assertEquals(["foo", "foo"], grep("foo", "foo", "bar", "foo", "bar"))

    def test_shouldReturnListContainingAllMatchingLinesWhenHaystackWithPartiallyMatchingLinesAndNonMatchingLinesIsGiven (self):
        self.assertEquals(["my foo", "your foo"], grep("foo", "my foo", "my bar", "your foo", "your bar"))