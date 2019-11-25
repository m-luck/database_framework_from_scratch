# from BTrees.OOBTree import OOBTree


class BasicDatabase():

    def __init__(self):
        self.records = None

    def __call__(self):
        self.print()

    def print(self):
        if len(list(str(self.records))) > 256: 
            print(str(self.records)[0:256] + "...")
        else:
            print(str(self.records))

    # Override the methods below to prevent NotImplementedError    

    def insert(self):
        raise NotImplementedError 

    def search(self):
        raise NotImplementedError 

    def delete(self):
        raise NotImplementedError