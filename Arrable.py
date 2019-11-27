
from BTreeImplementation import BTreeImplementation
from HashStructureImplementation import HashStructureImplementation
from typing import List

class Arrable:
    
    def __init__(self, implem=BTreeImplementation):
        self.db = BTreeImplementation()
        self.column_names = []
        self.pk = None

    def import_from_file(self, data_path, header=True, pk=None):
        
        if pk: self.pk = pk

        with open(data_path, "r") as f:

            rowNum = 0

            for i, line in enumerate(f):

                cols = line.split("|") 

                if (i==0 and not header):
                    self.column_names = [ i for i in range(0,len(cols)) ]
                    if not self.pk: 
                        self.column_names = ["-1*"] + self.column_names 
                        
                elif (i==0 and header):
                    if not self.pk: 
                        self.column_names = ["-1*"] + cols 
                    else:
                        self.column_names = cols
                
                if (i>0 and header) or (i>=0 and not header):
                    if not self.pk:
                        cols = [rowNum] + cols
                        
                    # Turn the row into a dictionary of field name to field value for faster lookup on WHERE checks.
                    val = { key:val for key, val in zip(self.column_names, cols) }

                    key = val[self.pk] if self.pk else rowNum # The ID column, implicitly indexed with primary key, else implicit ID if not provided.

                    self.db.insert(key, val)
                    rowNum += 1
        
        return self

    def init_from_arrable(self, col_names: List, rows: List, pk=None):

        self.column_names = col_names
        
        rowNum = 0
        for row in rows:

            key = row[pk] if pk else rowNum # The ID column, implicitly indexed with primary key, else implicit ID if not provided.

            val = row

            self.db.insert(key, val)
            rowNum += 1
        
        return self



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
    
    def result(self):
        pass
    
    def print(self):
        pass
    
    
        
    
