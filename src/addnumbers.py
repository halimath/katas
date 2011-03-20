"""
    A simple kata that focusses on
    - test driven development
    - baby steps
    
    Create a function that takes a string as input. The string should
    contain several numbers and separators. The function will parse
    the string and add the numbers together returning the sum.
"""

import unittest

def calculateSum (input):
    if not input:
        return 0
    return reduce(lambda sum, value: sum + int(value), 
                  input.split('+'), 0)

class CalculateSumTest (unittest.TestCase):
    def test_shouldReturnZeroWhenNoneIsGiven (self):
        self.assertEquals(0, calculateSum(None))

    def test_shouldReturnZeroWhenZeroIsGiven (self):
        self.assertEquals(0, calculateSum("0"))

    def test_shouldReturnOneWhenOneIsGiven (self):
        self.assertEquals(1, calculateSum("1"))

    def test_shouldReturnTwoWhenTwoIsGiven (self):
        self.assertEquals(2, calculateSum("2"))

    def test_shouldReturnTwoWhenOnePlusOneIsGiven (self):
        self.assertEquals(2, calculateSum("1+1"))

    def test_shouldReturnThreeWhenOnePlusOnePlusOneIsGiven (self):
        self.assertEquals(3, calculateSum("1+1+1"))

    def test_shouldReturnThreeWhenOnePlusOnePlusOneWithWhitespaceIsGiven (self):
        self.assertEquals(3, calculateSum("1 + 1 + 1"))
    