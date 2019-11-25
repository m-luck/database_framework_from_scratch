from BasicDatabase import BasicDatabase
from typing import List

class HashStructureImplementation(BasicDatabase):

    # Store values in array. 
    # Hash into index of array.

    # OurProgram < OurTestLines

    def __init__(self):
        BasicDatabase.__init__(self)
        # Hash key to index to desired record. 
        self.indices = {}
        self.records = []
        self.indTracker = 0

    def insert(self,k,v):
        """
        Upserts (updates or inserts) value into key bucket.

        Args:
            k - key
            v - value
        Returns: 
            None
        Side Effects:
            self.indices
            self.records
        """

        if self.search(k) != None: # The key already exists in the record, so update 
            resInd = self.indices[int(k)]
            self.records[resInd] = int(v)
        else: # Append to records,
            self.indices[int(k)] = self.indTracker 
            self.records.append((int(k), int(v)))
            self.indTracker += 1
    
    def search(self, k):
        """
        Searches the structure for the key.

        Args:
            k - key
        Returns:
            Corresponding value of key if exists, None otherwise.
        Side Effects:
            None
        """
        try: 
            resInd = self.indices[int(k)]
            res = self.records[resInd]
        except: 
            res = None
        return res

    def delete(self, k):
        """
        Deletes the key and value pair matching the key. 

        Args:
            k - key
        Returns:
            The key just removed.
        Side Effects:
            self.indices
            self.records
        """

        try:
            resInd = self.indices[int(k)]
            self.indices[int(k)] = "deleted"
            self.records[resInd] = "deleted"
            success = True
        except:
            success = False
        return success


