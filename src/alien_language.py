"""
    Not really a code kata but still some great problem to
    improve coding skills such as tdd and interface discovery.
    
    The problem has been presented by Google Code Jam and is
    available as an exercise:
    http://code.google.com/codejam/contest/90101/dashboard
"""

import re
import unittest

from mockito import mock, when, verify, unstub, any as any_value

class AlienLanguage (object):
    def __init__ (self, parser, dictionary):
        self.parser = parser
        self.dictionary = dictionary
        
    def determine_words (self, expression):
        potential_words = self.parser.find_potential_words(expression)
        
        return [word for word in potential_words if word in self.dictionary]
    
class AbstractAlienLanguageToken (object):
    def __init__ (self, value):
        self.value = value
    
    def get_possible_variations (self):
        raise TypeError('Not implemented')
    
    def __repr__ (self):
        return str(self)
    
    def __eq__ (self, other):
        return self.value == other.value and self.__class__ == other.__class__
    
class LiteralAlienLanguageToken (AbstractAlienLanguageToken):
    def get_possible_variations (self):
        return [self.value]
    
    def __str__ (self):
        return self.value

class AlternatingAlienLanguageToken (AbstractAlienLanguageToken):
    def get_possible_variations (self):
        return [character for character in self.value]

    def __str__ (self):
        return '[%s]' % self.value
    
class AlienLanguageTokenizer (object):
    TOKEN_PATTERN = re.compile(r'(\([a-z]+\))')
    
    def tokenize (self, expression):
        match = AlienLanguageTokenizer.TOKEN_PATTERN.split(expression)
        
        result = []
        for group in match:
            if not group:
                continue
            if group[0] == '(':
                result.append(AlternatingAlienLanguageToken(group[1:-1]))
            else:
                result.append(LiteralAlienLanguageToken(group))
        
        return result
    
class AlienLanguageParser (object):
    def __init__ (self, tokenizer):
        self.tokenizer = tokenizer
    
    def find_potential_words (self, expression):
        tokens = self.tokenizer.tokenize(expression)
        
        result = None
        for token in tokens:
            variations = token.get_possible_variations()
            if not result:
                result = variations
            else:
                result_multiplied = []
                for intermediate in result:
                    for variation in variations:
                        result_multiplied.append(intermediate + variation)
                result = result_multiplied
        return result


class AlienLanguageTokenizerTests (unittest.TestCase):
    def test_should_tokenize_literal (self):
        self.assertEquals([LiteralAlienLanguageToken('abc')], 
                          AlienLanguageTokenizer().tokenize('abc'))

    def test_should_tokenize_alternation (self):
        self.assertEquals([AlternatingAlienLanguageToken('abc')], 
                          AlienLanguageTokenizer().tokenize('(abc)'))

    def test_should_tokenize_complex_example (self):
        expression = '(ab)ac(ad)'
        expected = [
                    AlternatingAlienLanguageToken('ab'),
                    LiteralAlienLanguageToken('ac'),
                    AlternatingAlienLanguageToken('ad')
                    ]
        self.assertEquals(expected, 
                          AlienLanguageTokenizer().tokenize(expression))

class AlienLanguageParserAcceptanceTests (unittest.TestCase):
    def tearDown (self):
        unittest.TestCase.tearDown(self)
        unstub()
        
    def test_should_find_correct_words_for_expression (self):
        first_token = mock()
        when(first_token).get_possible_variations().thenReturn(['a', 'b'])

        second_token = mock()
        when(second_token).get_possible_variations().thenReturn(['a'])
        
        third_token = mock()
        when(third_token).get_possible_variations().thenReturn(['a', 'b'])
        
        tokens = [first_token, second_token, third_token]
        
        tokenizer_mock = mock()
        when(tokenizer_mock).tokenize(any_value()).thenReturn(tokens)
        
        parser = AlienLanguageParser(tokenizer_mock)
        potential_words = parser.find_potential_words('(ab)a(ab)')
        
        self.assertEquals(['aaa', 'aab', 'baa', 'bab'], potential_words)

        verify(tokenizer_mock).tokenize('(ab)a(ab)')
    
class AlienLanguageAcceptanceTests (unittest.TestCase):
    def tearDown (self):
        unittest.TestCase.tearDown(self)
        unstub()
        
    def test_should_determine_correct_words (self):
        expression = '(ab)(bc)(ca)'
        potential_words = 'abc aba acc aca bbc bba bcc bca'.split()
        language_words = 'abc bca dac dbc cba'.split()
        actual_words = 'abc bca'.split()
        
        parser_mock = mock()
        when(parser_mock).find_potential_words(any_value()).thenReturn(potential_words)
        
        language = AlienLanguage(parser_mock,
                                 language_words)
        words = language.determine_words(expression)

        self.assertEquals(actual_words, words)
        
        verify(parser_mock).find_potential_words(expression)
        
class AlienLanguageIntegrationTests (unittest.TestCase):
    def test_should_determine_corrent_words_when_alterations_are_given (self):
        expression = '(ab)(bc)(ca)'
        language_words = 'abc bca dac dbc cba'.split()
        expected_words = 'abc bca'.split()
        
        tokenizer = AlienLanguageTokenizer()
        parser = AlienLanguageParser(tokenizer)
        language = AlienLanguage(parser, language_words)
        actual_words = language.determine_words(expression)
        self.assertEquals(expected_words, actual_words)

    def test_should_determine_corrent_words_when_literal_is_given (self):
        expression = 'abc'
        language_words = 'abc bca dac dbc cba'.split()
        expected_words = 'abc'.split()
        
        tokenizer = AlienLanguageTokenizer()
        parser = AlienLanguageParser(tokenizer)
        language = AlienLanguage(parser, language_words)
        actual_words = language.determine_words(expression)
        self.assertEquals(expected_words, actual_words)


def handle_google_code_jam_file (file_name):
    lines = open(file_name, 'r').readlines()
    (l, d, n) = map(lambda (x): int(x), lines[0].split())
    dictionary = map(lambda (x): x.strip(), lines[1:d + 1])
    expressions = map(lambda (x): x.strip(), lines[d + 1:])

    language = AlienLanguage(AlienLanguageParser(AlienLanguageTokenizer()), 
                             dictionary)
    
    count = 1
    for expression in expressions:
        print "Case #%d: %d" % (count, 
                                len(language.determine_words(expression)))
        count += 1    
    
if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: %s inputfile" % sys.argv[0])
        sys.exit(1)
    
    handle_google_code_jam_file(sys.argv[1])    
