import unittest

from Arrable import Arrable
from QueryCommands import WherePredicates
import QueryCommands as q

class TestQueryCommands(unittest.TestCase):
    
    # def test_import_from_file(self):
    #     arr = Arrable().import_from_file("sales1")
    #     # print(arr.get_col_names())
    #     # print(arr.get_rows()[0])
        
    # def test_import_from_file_pk(self):
    #     arr = Arrable().import_from_file("sales1", pk="itemid")
    #     # print(arr.get_col_names())
    #     # print(arr.get_rows()[0])

    # def test_import_from_file_no_head(self):
    #     arr = Arrable().import_from_file("sales1", header=False)
    #     # print(arr.get_col_names())
    #     # print(arr.get_rows()[0])

    # def test_select_single(self):
    #     arr = Arrable().import_from_file("sales1")
    #     res = q.select(arr, "itemid", where="itemid=14")
    #     print(res.get_rows())

    # def test_select_multiple_comma(self):
    #     arr = Arrable().import_from_file("sales1")
    #     res = q.select(arr, "itemid", where="itemid=14,saleid=36")
    #     print(res.get_rows())

    # def test_select_multiple_word(self):
    #     arr = Arrable().import_from_file("sales1")
    #     res = q.select(arr, "itemid", where="(itemid=14) and (saleid=36)")
    #     print(res.get_rows())

    # def test_groupby(self):
    #     arr = Arrable().import_from_file("sales1")
    #     resList = q._groupby(arr, "customerid")
    #     print([len(res) for res in resList])

    # def test_project(self):
    #     arr = Arrable().import_from_file("test_input1")
    #     result = q.project(arr, "saleid", "itemid", "time")
    #     print(result.get_rows())

    def test_sum(self):
        arr = Arrable().import_from_file("test_input1")
        result = q.sum(arr, "qty")
        self.assertEqual(result.get_rows()[0], 147)

    # def test_avg(self):
    #     arr = Arrable().import_from_file("sales1")
    #     result = q.avg(arr, "qty")
    #     print(result)

    # def test_sumgroup(self):
    #     arr = Arrable().import_from_file("sales1")
    #     result = q.sumgroup(arr, "qty", "time")
    #     print(result.get_rows())

    # def test_avggroup(self):
    #     arr = Arrable().import_from_file("sales1")
    #     result = q.avggroup(arr, "qty", "time")
    #     print(result.get_rows())

    # def test_count(self):
    #     arr = Arrable().import_from_file("sales1")
    #     result = q.count(arr, "qty")
    #     print(result)

    # def test_countgroup(self):
    #     arr = Arrable().import_from_file("sales1")
    #     result = q.countgroup(arr, "qty", "time")
    #     print(result.get_rows())

    # def test_concat(self):
    #     arr1 = Arrable().import_from_file("sales1")
    #     arr2 = Arrable().import_from_file("sales1")
    #     result = q.concat(arr1, arr2)
    #     print("arr1 num rows = <", len(arr1.get_rows()), ">\n")
    #     print("arr2 num rows = <", len(arr2.get_rows()), ">\n")
    #     print("concat arr num rows = <", len(result.get_rows()), ">\n")
    #     print(result.get_rows())

if __name__ == "__main__":
    unittest.main()