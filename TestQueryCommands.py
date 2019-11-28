import unittest

from Arrable import Arrable
from QueryCommands import WherePredicates
import QueryCommands as q

class TestQueryCommands(unittest.TestCase):
    
    def test_import_from_file(self):
        arr = Arrable().import_from_file("sales1")
        # print(arr.get_col_names())
        # print(arr.get_rows()[0])
        
    def test_import_from_file_pk(self):
        arr = Arrable().import_from_file("sales1", pk="itemid")
        # print(arr.get_col_names())
        # print(arr.get_rows()[0])

    def test_import_from_file_no_head(self):
        arr = Arrable().import_from_file("sales1", header=False)
        # print(arr.get_col_names())
        # print(arr.get_rows()[0])

    def test_select_single(self):
        arr = Arrable().import_from_file("sales1")

        res = q.select(arr, "itemid", where="itemid=14")
        
        print(res.get_rows())

    def test_select_multiple(self):
        arr = Arrable().import_from_file("sales1")

        res = q.select(arr, "itemid", where="itemid=14,saleid=36")
        
        print(res.get_rows())

if __name__ == "__main__":
    unittest.main()