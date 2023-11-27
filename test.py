import unittest
from main import *

class TestCase(unittest.TestCase):
    def test_tokenize_string(self):
        text = "test0 test1? test2!"
        tokens = tokenize_string(text)
        self.assertEqual(tokens, ["test0", "test1", "test2"])

if __name__ == '__main__':
    unittest.main()