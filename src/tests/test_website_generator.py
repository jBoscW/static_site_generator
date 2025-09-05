import unittest
import src.website_generator as wg


class TestWebsiteGenerator(unittest.TestCase):
    def test_extract_title(self):
        self.assertEqual(wg.extract_title("# Hello World"), "Hello World")
        self.assertEqual(wg.extract_title("# Multiple ### Hashes ###"), "Multiple ### Hashes ###" )
        self.assertEqual(wg.extract_title("   # Leading Spaces"), "Leading Spaces")
        self.assertEqual(wg.extract_title("# Trailing Spaces   "), "Trailing Spaces")
        # raise exception if more than one ##
        with self.assertRaises(Exception):
            wg.extract_title("## No Title Here")
        with self.assertRaises(Exception):
            wg.extract_title("Some random text")
        with self.assertRaises(Exception):
            wg.extract_title("")
        with self.assertRaises(Exception):
            wg.extract_title("   ")
        with self.assertRaises(Exception):
            wg.extract_title("# ")

if __name__ == '__main__':
    unittest.main()