import unittest

from Arrable import Arrable
from QueryCommands import WherePredicates
import QueryCommands as q

class TestQueryCommands(unittest.TestCase):
    
    def test_import_from_file(self):
        arr = Arrable().import_from_file("test_input1")
        self.assertEqual(['saleid', 'itemid', 'customerid', 'storeid', 'time', 'qty', 'pricerange'], arr.get_col_names())
        self.assertEqual(arr.get_rows()[0], {'  ': 0, 'saleid': '36', 'itemid': '14', 'customerid': '2', 'storeid': '38', 'time': '49', 'qty': '15', 'pricerange': 'moderate'})
        
    def test_import_from_file_pk(self):
        arr = Arrable().import_from_file("sales1", pk="itemid")

    def test_import_from_file_no_head(self):
        arr = Arrable().import_from_file("test_input1", header=False)
        self.assertEqual([0, 1, 2, 3, 4, 5, 6], arr.get_col_names())
        self.assertEqual({'  ': 1, 0: '36', 1: '14', 2: '2', 3: '38', 4: '49', 5: '15', 6: 'moderate'}, arr.get_rows()[1])

    def test_select_single(self):
        arr = Arrable().import_from_file("sales1")
        res = q.select(arr, "itemid", where="itemid=14")
        self.assertEqual([{'itemid': '14', '  ': 0}], res.get_rows())

    def test_select_multiple_comma(self):
        arr = Arrable().import_from_file("sales1")
        res = q.select(arr, "itemid", where="itemid=14,saleid=36")
        self.assertEqual([{'itemid': '14', '  ': 0}], res.get_rows())

    def test_select_multiple_word(self):
        arr = Arrable().import_from_file("test_input1")
        res = q.select(arr, "itemid", where="(itemid=14) and (saleid=36)")
        self.assertEqual([{'itemid': '14', '  ': 0}], res.get_rows())

    def test_groupby(self):
        arr = Arrable().import_from_file("test_input1")
        resList = q._groupby(arr, "customerid")
        self.assertEqual([len(res) for res in resList], [3, 1, 1, 1])

    def test_project(self):
        arr = Arrable().import_from_file("test_input1")
        result = q.project(arr, "saleid", "itemid", "time")
        self.assertEqual({'saleid': '36', 'itemid': '14', 'time': '49'}, result.get_rows()[0])

    def test_sum(self):
        arr = Arrable().import_from_file("test_input1")
        result = q.sum(arr, "qty")
        self.assertEqual(result.get_rows()[0], 147)

    def test_avg(self):
        arr = Arrable().import_from_file("test_input1")
        result = q.avg(arr, "qty")
        self.assertEqual(result.get_rows(), 24.5)

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