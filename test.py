import unittest
import lm
import corpus


class TestTokenize(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(corpus.tokenize(''), [])

    def test_apple(self):
        self.assertEqual(corpus.tokenize('This is an apple.'), ['This', 'is', 'an', 'apple', '.'])


class TestDeTokenize(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(corpus.detokenize([]), '')

    def test_short(self):
        self.assertEqual(corpus.detokenize(['.']), '.')


class TestGetngrams(unittest.TestCase):
    def test_1(self):
        self.assertEqual(lm.get_ngrams(['apple'], 1), [['apple']])

    def test_2(self):
        self.assertEqual(lm.get_ngrams(['apple'], 2), [[None, 'apple'], ['apple', None]])


class TestLanguageModel(unittest.TestCase):
    def test_train(self):
        model = lm.LanguageModel(3)
        model.train([['This', 'is', 'an', 'apple', '.']])
        dic = {(None, None): {'This': 1}, (None, 'This'): {'is': 1},
               ('This', 'is'): {'an': 1}, ('is', 'an'): {'apple': 1},
               ('an', 'apple'): {'.': 1}, ('apple', '.'): {None: 1},
               ('.', None): {None: 1}}
        self.assertTrue(model.counts == dic)

    def test_generate(self):
        model = lm.LanguageModel(3)
        model.train([['This', 'is', 'an', 'apple', '.']])
        self.assertTrue(type(corpus.detokenize(model.generate())) == str)
