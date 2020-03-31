""" Contains test cases for styles
"""
import styles 
import unittest

__author__ = "Akshay Kale"
__copyright__ = "GPL"
__credits__ = "Dilanga Abeyrathna"
__email__ = "akale@unomaha.edu"


class TestStyle(unittest.TestCase):
    def setUp(self):
        self.style = styles.Style()

    def get_entities(self):
        text = 'Ron went to hospital!'
        output  = ''
        self.assertEqual(self.style.get_entities(text), output)

    def test_get_elongated_words(self):
        text = "Hiiiiii! whats up???"
        output = ['Hiiiiii!', 'up???']
        self.assertEqual(self.style.get_elongated_words(text), output)

if __name__ == '__main__':
    unittest.main()

