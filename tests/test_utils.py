import unittest
from src import utils


class TestUtils(unittest.TestCase):
    def test_find_if(self):
        collection = range(1, 10)
        assert utils.find_if(collection, lambda integer: integer % 2 == 0 and integer % 3 == 0) == 6

    def test_find_all_if(self):
        collection = range(10)
        assert utils.find_all_if(collection, lambda integer: integer % 3 == 0) == [0, 3, 6, 9]


if __name__ == '__main__':
    unittest.main()
