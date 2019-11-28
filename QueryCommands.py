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
    for (j, row) in enumerate(arrable.get_rows()):
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
    
def join():
    pass