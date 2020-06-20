import unittest

from crawler.pastebin_crawler.data_noarmalization import PasteDataNormalizer


class TestDataNormalizerAuthor(unittest.TestCase):
    def test_author_unknown(self):
        self.assertEqual(PasteDataNormalizer.normalize_author('guest'), '')
        self.assertEqual(PasteDataNormalizer.normalize_author('unknown'), '')
        self.assertEqual(PasteDataNormalizer.normalize_author('anonymous'), '')
        self.assertEqual(PasteDataNormalizer.normalize_author(''), '')
        self.assertNotEqual(PasteDataNormalizer.normalize_author('John'), '')

    def test_author_lowercase(self):
        author = 'John'
        self.assertEqual(PasteDataNormalizer.normalize_author(author),
                         author.lower())

    def test_content(self):
        self.assertEqual(PasteDataNormalizer.normalize_content('content/'),
                         'content')


if __name__ == '__main__':
    unittest.main()
