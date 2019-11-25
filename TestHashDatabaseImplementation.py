import timeit
import unittest
from HashStructureImplementation import HashStructureImplementation


class TestHashStructureImplementation(unittest.TestCase):

    def _createImplementation(self):
        self.truth = {}
        self.db = HashStructureImplementation()
        with open("myindex.txt", "r") as f:
            for line in f:
                key, val = line.split("|")
                if key[0].isdigit():
                    self.truth[int(key)] = int(val)
                    self.db.insert(int(key), int(val))

    def test_search_exist(self):
        self._createImplementation()

        self.assertEqual(self.db.search(27528), (27528, 19730))

    def test_insert_already_exist(self):
        self._createImplementation()

        self.db.insert(27528, 42)
        self.assertEqual(self.db.search(27528), (27528, 42)) 

    def test_insert_not_exist(self):
        self._createImplementation()

        self.db.insert(-1, 42)
        self.assertEqual(self.db.search(-1), (-1, 42)) 

    def test_remove_exist(self):
        self._createImplementation()

        self.db.delete(27528)
        self.assertEqual(self.db.search(27528), (25728, "deleted"))

    def test_remove_not_exist(self):
        self._createImplementation()

        self.assertEqual(self.db.delete("not exist"), False)
        
if __name__ == "__main__":
    unittest.main()