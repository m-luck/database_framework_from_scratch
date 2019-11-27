
from BTreeImplementation import BTreeImplementation

class Arrable:
    
    def __init__(self, data_path=None, header=True):
        self.db = BTreeImplementation
        self.column_names = []
        
        if data_path:
            with open(data_path, "r") as f:
                for line in f:
                    cols = line.split("|")
                    if not header: # It is a data row.

                        key = int(cols[0]) # The ID column, implicitly indexed.

                        # Turn the row into a dictionary of field name to field value for faster lookup on WHERE checks.
                        val = {map(lambda x: x[0]:float(x[1]) if x[1].isnumeric() else x[0]:x[1], *(zip(self.column_names, cols)))}

                        self.db.insert(key, val)

                    else: # If header is True, it is the first row, which should enumerate the column labels.
                        self.column_names = cols
                        header = False


    def get_rows(self):
        """
        Returns the array of rows (an array of arrays).
        """
        return self.db.records

    def get_col_names(self):
        """
        Returns array of col names.
        """
        
        return self.column_names
    
    
        
    
