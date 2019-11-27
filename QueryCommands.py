from Arrable import Arrable
from typing import List

class WherePredicates():
    
    def __init__(self, col_names, rows, predicate_strings):

        # AND / OR
        self.pred_strings, self.logic_operator = self._process_logic_operators(predicate_strings.lower().strip()) 
        self.preds = self._process_predicate_list(self.pred_strings)

    def _process_logic_operators(self, preds: str):
        """
        Per specification, all selects will contain all conjunctive (AND) or all disjunctive (OR).
        This function finds that out with the whole WHERE string and returns a lambda with that type of check, or None if does not exist.
        """

        op = None
        res_list = []

        if "or" in self.preds: # all ORs, per specification
            op = (lambda x, y: x or y)
            res_list = preds.strip(")(").split("or") 

        elif "and" in self.preds: # all ANDs 
            op = (lambda x, y: x and y)
            res_list = preds.strip(")(").split("and") 

        elif "," in self.preds: # all ANDs 
            op = (lambda x, y: x and y)
            res_list = preds.strip(")(").split(",") 
        
        return res_list, op

    def _process_predicate_list(self, predList: List):
        
        comp_pairs = []
        rel_ops = []
        for p in self.preds:
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
                comp_pairs.append((a,b))
                rel_ops.append(lambda x, y: x == y)
        
        return zip(comp_pairs, rel_ops)
    
    def check(self, row):
        sub_res = []
        for pred in preds: 
            a, b = pred[0]
            lamb = pred[1]
            sub_res.append(lamb(a, b))
        
        if self.logic_operator == :
            return any
            
        

def select(fromTable: Arrable, where: str):
    """
    e.g. 
        select(R, (time > 50) or (qty < 30))
        select(R, qty = 5) 
        select(R, itemid = 7)
    res = []
    return res
    """
    res = []
    for row in Arrable.get_rows():
        if 


def join():
    pass