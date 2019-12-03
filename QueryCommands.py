from Arrable import Arrable
from typing import List
from collections import defaultdict

class WherePredicates():
    
    def __init__(self, predicate_strings):

        # AND / OR
        self.pred_strings, self.logic_operator = self._process_logic_operators(predicate_strings.lower().strip()) 
        self.preds = self._process_predicate_list(self.pred_strings)

    def _process_logic_operators(self, preds: str):
        """
        Per specification, all selects will contain all conjunctive (AND) or all disjunctive (OR).
        This function finds that out with the whole WHERE string and returns a lambda with that type of check, or None if does not exist.
        """

        op = all
        res_list = []

        if "or" in preds: # all ORs, per specification
            op = any
            res_list = preds.strip(")(").split("or") 

        elif "and" in preds: # all ANDs 
            op = all
            res_list = preds.strip(")(").split("and") 

        elif "," in preds: # all ANDs 
            op = all
            res_list = preds.strip(")(").split(",") 

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
            elif "=" in p:
                a, b = p.split("=")
                comp_pairs.append((a, b))
                rel_ops.append(lambda a, b: a == b)
                
        
        return list(zip(comp_pairs, rel_ops))
    
    def isMatch(self, row, cols):
        sub_res = []
        for pred in self.preds: 
            a, b = pred[0]
            lamb = pred[1]
            if a in cols and not b.isnumeric() and "\'" not in b and "\"" not in b and b in cols: # It's two columns being compared intrarow
                sub_match = lamb(row[a], row[b])
            elif a in cols: # It's a column being compared to a value
                sub_match = lamb(row[a], b)
            else: 
                sub_match = lamb(a, b) # It's two values (rare, like True=False, maybe a SQL injection) 
            sub_res.append(sub_match)

            
        return self.logic_operator(sub_res)

def select(fromTable: Arrable, cols: str, where: str):
    """
    e.g. 
        select(R, "(time > 50) or (qty < 30)")
        select(R, "qty = 5") 
        select(R, "itemid = 7")
    """

    orig_cols = fromTable.get_col_names()
    cols = cols.strip().split(",")
    where = WherePredicates(where)

    res = []
    for i, row in enumerate(fromTable.get_rows()):
        if where.isMatch(row, orig_cols):
            val = {entry:row[entry] for entry in cols}
            val["-1*"] = i
            res.append(val)

    newArr = Arrable().init_from_arrable(cols, res)

    return newArr

def project(fromTable: Arrable, *arg: str):
    """
    filters columns specified in params (*arg) 
    from the specified arrable (fromTable)
    returns: Arrable
    """
    columns = list(arg)
    result = []
    for (j, row) in enumerate(fromTable.get_rows()):
        new_row = {col:row[col] for col in columns}
        result.append(new_row)

    newArrable = Arrable().init_from_arrable(columns, result)
    return newArrable

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
        
    return result

def sum(table: Arrable, col_name: str):
    """
    sum calls some, returns some some sum (int)
    """
    result = _some(table, col_name)
    
    return result

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
        sum_elts += int(row[col_name])
        
    result = sum_elts/num_elts
    
    return result

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
    group_col_name = "sumgroup"
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
    
def join():
    pass