import unittest

from Arrable import Arrable
from QueryCommands import WherePredicates
import QueryCommands as q
import CommandTextParser as p

class TestQueryCommands(unittest.TestCase):
    
    def test_import_from_file(self):
        arr = Arrable().import_from_file("test_input1")
        self.assertEqual(['saleid', 'itemid', 'customerid', 'storeid', 'time', 'qty', 'pricerange', 'join'], arr.get_col_names())
        self.assertEqual(arr.get_rows()[0], {'  ': 0, 'saleid': '36', 'itemid': '14', 'join': 'hey', 'customerid': '2', 'storeid': '38', 'time': '49', 'qty': '15', 'pricerange': 'moderate'})
        
    def test_import_from_file_pk(self):
        arr = Arrable().import_from_file("sales1", pk="itemid")

    def test_import_from_file_no_head(self):
        arr = Arrable().import_from_file("test_input1", header=False)
        self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7], arr.get_col_names())
        self.assertEqual({0: '36', 1: '14', 2: '2', 3: '38', 4: '49', 5: '15', 6: 'moderate', '  ': 1, 7: 'hey'}, arr.get_rows()[1])

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

    def test_select_math(self):
        arr = Arrable().import_from_file("test_input1")
        res = q.select(arr, "itemid,customerid", where="(itemid/7<3) and (customerid*2<5)")
        self.assertEqual([{'  ': 0, 'customerid': '2', 'itemid': '14'}], res.get_rows())

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
        self.assertEqual(result.get_rows(), [24.5])

    def test_sumgroup(self):
        arr = Arrable().import_from_file("test_input1")
        result = q.sumgroup(arr, "qty", "time")
        self.assertEqual(result.get_rows(), [{'sumgroup': '15', 'time': '49'}, {'sumgroup': '31', 'time': '46'}, {'sumgroup': '14', 'time': '81'}, {'sumgroup': '86', 'time': '67'}, {'sumgroup': '1', 'time': '35'}])

    def test_avggroup(self):
        arr = Arrable().import_from_file("test_input1")
        result = q.avggroup(arr, "qty", "time")
        self.assertEqual(result.get_rows(), [{'avggroup': '15.0', 'time': '49'}, {'avggroup': '31.0', 'time': '46'}, {'avggroup': '14.0', 'time': '81'}, {'avggroup': '43.0', 'time': '67'}, {'avggroup': '1.0', 'time': '35'}])

    def test_count(self):
        arr = Arrable().import_from_file("sales1")
        result = q.count(arr)
        print(result)

    def test_countgroup(self):
        arr = Arrable().import_from_file("sales1")
        result = q.countgroup(arr, "time")
        print(result.get_rows())

    def test_concat(self):
        arr1 = Arrable().import_from_file("test_input1")
        arr2 = Arrable().import_from_file("test_input1_to_concat")
        result = q.concat(arr1, arr2)
        # print("arr1 num rows = <", len(arr1.get_rows()), ">\n")
        # print("arr2 num rows = <", len(arr2.get_rows()), ">\n")
        # print("concat arr num rows = <", len(result.get_rows()), ">\n")
        self.assertEqual(len(result.get_rows()), 9)

    def test_join(self):
        a = Arrable().import_from_file("test_input1")
        b = Arrable().import_from_file("test_input2")
        res = q.join(a, "a", b, "b", "a_join = b_j_oin")
        self.assertEqual(res.get_rows(), [{'a_saleid': '36', 'a_itemid': '14', 'a_customerid': '2', 'a_storeid': '38', 'a_time': '49', 'a_qty': '15', 'a_pricerange': 'moderate', 'a_join': 'hey', 'b_saleid': '3506', 'b_I': '13517', 'b_C': '16566', 'b_S': '45', 'b_T': '73', 'b_Q': '19', 'b_P': 'expensive', 'b_j_oin': 'hey'}])
        # for row in res.get_rows():
        #     print(row["a_join"], row["b_j_oin"])

    # def test_join_large(self): # Works
    #     a = Arrable().import_from_file("sales1")
    #     b = Arrable().import_from_file("sales2")
    #     res = q.join(a, "a", b, "b", "a_pricerange = b_P")
    #     print(res.get_rows())

    def test_mov_sum(self):
        arr = Arrable().import_from_file("sales1")
        res = q.moving_sum(arr, "qty", 2)
        rows = res.get_rows()
        self.assertEqual(rows[0], 15)
        self.assertEqual(rows[1], 46)
        self.assertEqual(rows[-1], 24)
        

    def test_mov_avg(self):
        arr = Arrable().import_from_file("sales1")
        res = q.moving_avg(arr, "qty", 2)
        rows = res.get_rows()
        self.assertEqual(rows[0], 15)
        self.assertEqual(rows[1], 23)
        self.assertEqual(rows[-1], 12)

    def test_sort_by_columns_single(self):
        arr = Arrable().import_from_file("test_input1")
        res = q.sort(arr, "qty")
        # [print(row) for row in res.get_rows()]
        
    def test_sort_by_columns_multiple(self):
        arr = Arrable().import_from_file("test_input1")
        res = q.sort(arr, "saleid", "qty", "pricerange")
        # print(res.get_rows(), [{'  ': 0, 'saleid': '36', 'itemid': '14', 'customerid': '2', 'storeid': '38', 'time': '49', 'qty': '15', 'pricerange': 'moderate', 'join': 'hey'}, {'  ': 1, 'saleid': '784', 'itemid': '90', 'customerid': '182', 'storeid': '97', 'time': '46', 'qty': '31', 'pricerange': 'moderate', 'join': '1'}, {'  ': 5, 'saleid': '951', 'itemid': '102', 'customerid': '116', 'storeid': '45', 'time': '35', 'qty': '1', 'pricerange': 'outrageous', 'join': 'wop'}, {'  ': 2, 'saleid': '801', 'itemid': '117', 'customerid': '2', 'storeid': '43', 'time': '81', 'qty': '14', 'pricerange': 'outrageous', 'join': 'g'}, {'  ': 3, 'saleid': '905', 'itemid': '79', 'customerid': '119', 'storeid': '81', 'time': '67', 'qty': '44', 'pricerange': 'outrageous', 'join': 'n'}, {'  ': 4, 'saleid': '227', 'itemid': '68', 'customerid': '2', 'storeid': '66', 'time': '67', 'qty': '42', 'pricerange': 'supercheap', 'join': 'lol'}])
        self.assertEqual(res.get_rows(),[{'  ': 0, 'saleid': '36', 'itemid': '14', 'customerid': '2', 'storeid': '38', 'time': '49', 'qty': '15', 'pricerange': 'moderate', 'join': 'hey'}, {'  ': 1, 'saleid': '784', 'itemid': '90', 'customerid': '182', 'storeid': '97', 'time': '46', 'qty': '31', 'pricerange': 'moderate', 'join': '1'}, {'  ': 5, 'saleid': '951', 'itemid': '102', 'customerid': '116', 'storeid': '45', 'time': '35', 'qty': '1', 'pricerange': 'outrageous', 'join': 'wop'}, {'  ': 2, 'saleid': '801', 'itemid': '117', 'customerid': '2', 'storeid': '43', 'time': '81', 'qty': '14', 'pricerange': 'outrageous', 'join': 'g'}, {'  ': 3, 'saleid': '905', 'itemid': '79', 'customerid': '119', 'storeid': '81', 'time': '67', 'qty': '44', 'pricerange': 'outrageous', 'join': 'n'}, {'  ': 4, 'saleid': '227', 'itemid': '68', 'customerid': '2', 'storeid': '66', 'time': '67', 'qty': '42', 'pricerange': 'supercheap', 'join': 'lol'}] )

    def test_parse_command_file(self):
        res = p.parse("test_commands1")
        self.assertEqual(res, [['R', 'inputfromfile(sales1)'], ['R1', 'select(R, (time > 50) or (qty < 30))'], ['R2', 'project(R1, saleid, qty, pricerange)'], ['R3', 'avg(R1, qty)'], ['R4', 'sumgroup(R1, time, qty)'], ['R5', 'sumgroup(R1, qty, time, pricerange)'], ['R6', 'avggroup(R1, qty, pricerange)'], ['S', 'inputfromfile(sales2)'], ['T', 'join(R, S, R.customerid = S.C)'], ['T1', 'join(R1, S, (R1.qty > S.Q) and (R1.saleid = S.saleid))'], ['T2', 'sort(T1, S_C)'], ['T2prime', 'sort(T1, R1_time, S_C)'], ['T3', 'movavg(T2prime, R1_qty, 3)'], ['T4', 'movsum(T2prime, R1_qty, 5)'], ['Q1', 'select(R, qty = 5)'], ['Btree(R, qty)'], ['Q2', 'select(R, qty = 5)'], ['Q3', 'select(R, itemid = 7)'], ['Hash(R,itemid)'], ['Q4', 'select(R, itemid = 7)'], ['Q5', 'concat(Q4, Q2)'], ['outputtofile(Q5, Q5)'], ['outputtofile(T, T)']])

    def test_interpret_select(self):
        res = p.interpret("select(T, (t=4) or (9 > 4))")
        self.assertEqual(res, "select(obj_dict['T'], ','.join(obj_dict['T'].get_col_names()), '(t=4) or (9 > 4)')")

    def test_interpret_join(self):
        res = p.interpret("join(R, S, R.customerid = S.C)")
        self.assertEqual(res, "join(obj_dict['R'], 'R', obj_dict['S'], 'S', ' R.customerid = S.C')")

    def test_to_hash(self):
        res = p.interpret("Hash(R,itemid)")
        self.assertEqual(res, "to_hash(obj_dict['R'], 'itemid')")

if __name__ == "__main__":
    unittest.main()