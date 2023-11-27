import unittest
from main import *

class TestCase(unittest.TestCase):
    def test_tokenize_string(self):
        self.assertEqual(
            tokenize_string('test0 test1? test2!'), 
            ['test0', 'test1', 'test2'])

    def test_filter_words_by_terms(self):
        self.assertEqual(
            filter_words_by_terms(['a', 'b', 'c', 'd', 'e'], ['b', 'd', 'f']),
            ['b', 'd'])

    def test_count_occurences(self):
        self.assertEqual(
            count_occurences(['a', 'b', 'a', 'd', 'a'], ['a', 'd', 'f']),
            4)

    def test_count_chapter_words(self):
        self.assertEqual(
            count_chapter_words([['a', 'b', 'c'], ['d', 'e', 'f']]),
            6)

    def test_calculate_term_density(self):
        self.assertAlmostEqual(
            calculate_term_density(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'], ['c', 'e', 'z']),
            25.0)

    def test_group_lines_based_on_delimiting_line_pattern(self):
        text = '''
ch 0
asdas
asdas
ch 1
abc
ch 2
def
ghj
kl'''
        self.assertEqual(
            group_lines_based_on_delimiting_line_pattern(text.split('\n'), 'ch '),
            {
                1 : ['asdas', 'asdas'],
                2 : ['abc'],
                3 : ['def', 'ghj', 'kl']
            }
        )

    def test_chunk_collection(self):
        self.assertEqual(
            list(chunk_collection([1,1,1,2,2,2,3,3,3,4,4], 3)),
            [[1,1,1], [2,2,2], [3,3,3], [4,4]])

    def test_map_function(self):
        self.assertEqual(
            map_function(['a', 'b'], ['c', 'd'])([
                (1,['a', 'b', 'c', 'd']), 
                (2,['d', 'e', 'f', 'a'])]),
            [
                (1,[50, 50]), 
                (2,[25, 25])
            ])

    def test_shuffle_function(self):
        self.assertEqual(
            list(shuffle_function([[1,1,1], [2,2,2], [3,3,3], [4,4]])),
            [[1,1,1,2,2], [2,3,3,3,4], [4]])

    def test_reduce_function(self):
        self.assertEqual(
            reduce_function([(1,[30,20]),(2,[10,90])]),
            [
                'CHAPTER 1: war-related',
                'CHAPTER 2: peace-related'
            ])

if __name__ == '__main__':
    unittest.main()