import ast
import progressbar

from Arrable import Arrable
from typing import List
from collections import defaultdict

from BTreeImplementation import BTreeImplementation
from HashStructureImplementation import HashStructureImplementation


class WherePredicates():
    
    def __init__(self, predicate_strings):

        # AND / OR
        self.pred_strings, self.logic_operator = self._process_logic_operators(predicate_strings.strip()) 
        self.preds = self._process_predicate_list(self.pred_strings)

    def _process_logic_operators(self, preds: str):
        """
        Per specification, all selects will contain all conjunctive (AND) or all disjunctive (OR).
        This function finds that out with the whole WHERE string and returns a lambda with that type of check, or None if does not exist.
        """

        op = all
        res_list = []
        preds = ''.join(c for c in preds if c not in ")( ")
        self.to_print = preds

        if "or" in preds: # all ORs, per specification
            op = any
            res_list = preds.split("or") 

        elif "and" in preds: # all ANDs 
            op = all
            res_list = preds.split("and") 

        elif "," in preds: # all ANDs 
            op = all
            res_list = preds.split(",") 

        else:
            op = all
            res_list = [preds]
        
        return res_list, op

    def _process_predicate_list(self, predList: List):
        
        comp_pairs = []
        rel_ops = []
        for p in predList:
            if ">=" in p:
                a, b = p.split(">=")
                comp_pairs.append((a,b))
                rel_ops.append(lambda x, y: x >= y)
            elif "<=" in p:
                a, b = p.split("<=")
                comp_pairs.append((a,b))
                rel_ops.append(lambda x, y: x <= y)
            elif "==" in p:
                a, b = p.split("==")
                comp_pairs.append((a,b))
                rel_ops.append(lambda x, y: x == y)
            elif ">" in p:
                a, b = p.split(">")
                comp_pairs.append((a,b))
                rel_ops.append(lambda x, y: x > y)
            elif "<" in p:
                a, b = p.split("<")
                comp_pairs.append((a,b))
                rel_ops.append(lambda x, y: x < y)
            elif "!=" in p:
                a, b = p.split("!=")
                comp_pairs.append((a,b))
                rel_ops.append(lambda x, y: x != y)
            elif "=" in p:
                a, b = p.split("=")
                comp_pairs.append((a, b))
                rel_ops.append(lambda a, b: a == b)
                
        
        return list(zip(comp_pairs, rel_ops))
    
    def _check_arith_op(self, x, op_str):
        if op_str in x:
            field, const = x.split(op_str)
            return (True, field, const)
        return (False, None, None)

    def isMatch(self, row, cols):
        sub_res = []
        for pred in self.preds: 
            a, b = pred[0]
            lamb = pred[1]  # lamb applies in/equality function on two values/columns

            # Arithmetic
                
            if a in cols and not b.isnumeric() and ("\'" not in b and "\"" not in b) and b in cols: # It's two columns being compared intrarow
                lamb1, lamb2 = row[a] if not row[a].isnumeric() else float(row[a]), row[b] if not row[b].isnumeric() else float(row[b])  
            elif a in cols: # It's a column being compared to a value
                lamb1, lamb2 = row[a] if not row[a].isnumeric() else float(row[a]), b if not b.isnumeric() else float(b)
            elif b in cols: # It's a value being compared to a column
                lamb1, lamb2 = a if not a.isnumeric() else float(a), row[b] if not row[b].isnumeric() else float(row[b]) 
            else: 
                lamb1, lamb2 = a if not a.isnumeric() else float(a), b if not b.isnumeric() else float(b) # It's two values (rare, like True=False, maybe a SQL injection) 
            
            # Account for arithmetic
            # Will override current lambda inputs if arithmetic is found
            for op in "+-*/":

                has_arith = self._check_arith_op(a, op)
                if has_arith[0]:
                    field = has_arith[1]
                    const_num = float(has_arith[2])
                    lhs = float(row[field])
                    expr = f"{lhs} {op} {const_num}"
                    lamb1 = float(eval(expr))         

                has_arith = self._check_arith_op(b, op)
                if has_arith[0]:
                    field = has_arith[1]
                    const_num = float(has_arith[2])
                    lhs = float(row[field])
                    expr = f"{lhs} {op} {const_num}"
                    lamb2 = float(eval(expr))         

            sub_match = lamb(lamb1, lamb2)
            sub_res.append(sub_match)

            
        return self.logic_operator(sub_res)

    def print(self):
        print(self.to_print)

def select(fromTable: Arrable, cols: str, where: str):
    """
    e.g. 
        select(R, R.get_cols_names(), "(time > 50) or (qty < 30)")
        select(R, R.get_cols_names(), "qty = 5") 
        select(R, R.get_cols_names(), "itemid = 7")
    """

    orig_cols = fromTable.get_col_names()
    cols = cols.strip().split(",")
    where = WherePredicates(where)

    res = []
    for i, row in enumerate(fromTable.get_rows()):
        if where.isMatch(row, orig_cols):
            val = {entry:row[entry] for entry in cols}
            val["  "] = i
            res.append(val)

    newArr = Arrable().init_from_arrable(cols, res)

    return newArr

def join(tableA: Arrable, A_name: str, tableB: Arrable, B_name: str, where: str):
    """
    The where string expects a pre-parsed string where "Table.Column" has already become "Table_Column".
    e.g. 
        join(R, S, "R_price = S_cost and R_cost = S_price")
    """

    renamed_cols_tableA, renamed_cols_tableB = _get_converted_col_tables_for_join(tableA, A_name, tableB, B_name)
    joined_cols = renamed_cols_tableA.get_col_names() + renamed_cols_tableB.get_col_names() # Concat the lists

    where = where.replace(".","_")
    where = WherePredicates(where)

    res = []

    done = len(tableA.get_rows()) * len(tableB.get_rows())
    # print(done)
    
    prog = 0
    progress_bar = progressbar.ProgressBar(max_value=100).start()
    for Arow in renamed_cols_tableA.get_rows():
        intermediate_cartesian = []
        # print(prog/done)
        progress_bar.update((prog/done)*100)
        for Brow in renamed_cols_tableB.get_rows():
            # print(Arow)
            # print(Brow)
            joined_row = {**Arow, **Brow}
            intermediate_cartesian.append(joined_row)
            prog += 1
        for cart_row in intermediate_cartesian:
            if where.isMatch(cart_row, joined_cols):
                print('match')
                res.append(cart_row)
    
    progress_bar.finish()
    newArr = Arrable().init_from_arrable(joined_cols, res)

    return newArr

def _get_converted_col_tables_for_join(tableA: Arrable, A_name: str, tableB: Arrable, B_name: str):
    
    renamedArows = _rename_fields_in_table(tableA, A_name)
    renamedBrows = _rename_fields_in_table(tableB, B_name)
   
    colsA = list(map(lambda col: ''.join([A_name, "_", col]), tableA.get_col_names()))
    colsB = list(map(lambda col: ''.join([B_name, "_", col]), tableB.get_col_names()))
    
    newA = Arrable().init_from_arrable(colsA, renamedArows, tableA.pk)
    newB = Arrable().init_from_arrable(colsB, renamedBrows, tableB.pk)

    return newA, newB

def _rename_fields_in_table(table: Arrable, table_name):
    rows = []
    for row in table.get_rows():
        newRow = {}
        for col in table.get_col_names():
            new_col = ''.join([table_name, "_", col]) # Turn all "col"s to "A_col"
            newRow[new_col] = row[col]
        rows.append(newRow)
    return rows

def project(fromTable: Arrable, *args: str):
    """
    filters columns specified in params (*arg) 
    from the specified arrable (fromTable)
    returns: Arrable
    """
    columns = list(args)
    result = []
    for (j, row) in enumerate(fromTable.get_rows()):
        new_row = {col:row[col] for col in columns}
        result.append(new_row)

    newArrable = Arrable().init_from_arrable(columns, result)
    return newArrable

def sort(fromTable: Arrable, *args: str): # args can also be None for base case, returning the table itself (recursion)
    """
    Order in reverse order so that the earlier columns have higher priority
    """
    if not list(args):
        return fromTable
    orderedPreference = list(args)
    colToOrderOn = orderedPreference.pop()
    # print(colToOrderOn)
    sorted_table_rows = sorted(fromTable.get_rows(), key = lambda row: int(row[colToOrderOn]) if row[colToOrderOn].isnumeric() else row[colToOrderOn])
    # [print(row) for row in sorted_table_rows]
    # print("\n")
    newArr = Arrable().init_from_arrable(fromTable.get_col_names(), sorted_table_rows)
    return sort(newArr, *orderedPreference)

def _groupby(fromTable: Arrable, groupOn: str):
    """
    Returns an arrable per distinct column value as an intermediate step. 
    To be concatted.
    """

    res = defaultdict(list)
    
    for row in fromTable.get_rows():
        res[row[groupOn]].append(row)
    
    return list([groupArr for groupArr in res.values()])


def _some(table: Arrable, col_name: str):
    """
    function name due to unclear instructions in hw specification. will include other namings to hedge our bets.
    computes the sum of all values in a specified column
    does not check for proper data type - will add later
    returns int
    """
    result = 0
    for i, row in enumerate(table.get_rows()):
        result += int(row[col_name])
        
    return float(result)

def sum(table: Arrable, col_name: str):
    """
    sum calls some, returns some some sum
    """
    result = [_some(table, col_name)]
    return Arrable().init_from_arrable(["sum"], result)

    
def avg(table: Arrable, col_name: str):
    """
    computes average of all values in a specified column
    does not check for proper data type - will add later
    returns int
    """
    sum_elts = 0
    num_elts = 0
    for i, row in enumerate(table.get_rows()):
        num_elts += 1
        sum_elts += float(row[col_name])

    if num_elts==0:
        num_elts = 1  
    result = [sum_elts/num_elts]
    
    return Arrable().init_from_arrable(["avg"], result)
 
def moving_op(table: Arrable, col_name: str, sliding_window: int, op, op_name: str):
    newArr = Arrable().init_from_arrable([op_name], [])
    stubs = []

    for stub in range(0, sliding_window):
        slice = table.get_slice(0, stub+1)
        newArr = concat(newArr, op(slice, col_name))
    for i, row in enumerate(table.get_rows()):
        if i + sliding_window - 1 <= len(table.get_rows()) - 1: 
            slice = table.get_slice(i, i+sliding_window) # make this the slice
            # print(newArr.get_col_names())
            # print(op(slice, col_name).get_rows())
            newArr = concat(newArr, op(slice, col_name))
            
    return newArr

def movsum(table: Arrable, col_name: str, sliding_window: int):
    return moving_op(table, col_name, sliding_window, sum, "sum") 

def movavg(table: Arrable, col_name: str, sliding_window: int):
    return moving_op(table, col_name, sliding_window, avg, "avg")
    
def count(table: Arrable):
    """
    counts the number of rows containing a value in the specified column 'col_name'
    returns int
    """
    result = [len(table.get_rows())]
    col_name = ["count"]
    return Arrable().init_from_arrable(col_name, result)

def sumgroup(table: Arrable, to_add: str, groupOn: str):
    """
    groups 'Arrable' by 'groupOn' and compute the sum of column 'to_add' for each group
    returns arrable with two columns, 'groupOn' and new 'sumgroup' columns
    """
    group_col_name = "sumgroup"
    final_columns = table.get_col_names().append(group_col_name)
    all_groups = _groupby(table, groupOn)
    list_of_sums = [0] * len(all_groups)
    
    # generate list of sums, one for each group
    for index, group in enumerate(all_groups):
        for row in group:
            list_of_sums[index] += int(row[to_add])
    
    # append sumgroup as new column and then append row to new final arrable
    arrable_rows = []
    for i, group in enumerate(all_groups):
        group[0].update({group_col_name:str(list_of_sums[i])})
        arrable_rows.append(group[0])
    
    final_arrable = Arrable().init_from_arrable(final_columns, arrable_rows)
    result = project(final_arrable, group_col_name, groupOn)
    
    return result

def avggroup(table: Arrable, to_avg: str, groupOn: str):
    """
    groups 'Arrable' by 'groupOn' and compute the avg of column 'to_avg' for each group
    returns arrable with two columns, 'groupOn' and new 'avggroup' columns
    """
    group_col_name = "avggroup"
    final_columns = table.get_col_names().append(group_col_name)
    all_groups = _groupby(table, groupOn)
    list_of_avgs = [0] * len(all_groups)
    
    # generate list of avgs, one for each group
    row_count = 0
    for i, group in enumerate(all_groups):
        for row in group:
            list_of_avgs[i] += int(row[to_avg])
            row_count += 1
        list_of_avgs[i] = list_of_avgs[i]/row_count
        row_count = 0
        
    # append avggroup as new column and then append row to new final arrable
    arrable_rows = []
    for i, group in enumerate(all_groups):
        group[0].update({group_col_name:str(list_of_avgs[i])})
        arrable_rows.append(group[0])
    
    final_arrable = Arrable().init_from_arrable(final_columns, arrable_rows)
    result = project(final_arrable, group_col_name, groupOn)
    
    return result

def countgroup(table: Arrable, groupOn: str):
    """
    groups 'Arrable' by 'groupOn' and counts the number of rows containing a value for 'to_count' in each group
    returns arrable with two columns, 'groupOn' and new 'countgroup' columns
    """
    all_groups = _groupby(table, groupOn)
    list_of_counts = []
    for group in all_groups:
        list_of_counts.append(len(group))
     
    arrable_rows = []
    group_col_name = "countgroup"
    final_columns = table.get_col_names().append(group_col_name)
    for i, group in enumerate(all_groups):
        group[0].update({group_col_name:str(list_of_counts[i])})
        arrable_rows.append(group[0])
    
    final_arrable = Arrable().init_from_arrable(final_columns, arrable_rows)
    result = project(final_arrable, group_col_name, groupOn)
    
    return result

def concat(table1: Arrable, table2: Arrable):
    """
    concats two arrables
    returns arrable
    """
    if table1.get_col_names() != table2.get_col_names():
        print("Table schemas don't match.") 
        return
    col_names = table1.get_col_names()
    concated = table1.get_rows() + table2.get_rows()
    result = Arrable().init_from_arrable(col_names, concated)
    return result

def output_to_file(table):
    table.output_to_file()

def inputfromfile(file):
    Arrable().import_from_file(file)

def to_btree(table, ind):
    return Arrable(implem=BTreeImplementation, ind=ind).init_from_arrable(table.get_col_names(), table.get_rows())

def to_hash(table, ind):
    return Arrable(implem=HashStructureImplementation, ind=ind).init_from_arrable(table.get_col_names(), table.get_rows())