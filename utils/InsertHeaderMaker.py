from loger import Loger
log = Loger()


class InsertHeaderMaker:
    def __init__(self, tablename, object):
        self.tablename = tablename
        self.keysnvalues = object.__dict__
        self.columns = ""
        self.addColumns()

    def addColumns(self):
        for item in self.keysnvalues.items():
            if item[1] is None:
                log.DEBUG("{} is removed".format(item))
                del self.keysnvalues[item[0]]
        if len(self.keysnvalues.keys()) > 0:
            self.columns = "("
            self.columns += ','.join(self.keysnvalues.keys())
            self.columns += ")"
        else:
            log.WARNING("Insert object is empty. Nothing to be inserted.")

    def getHat(self):
        if self.columns:
            return "INSERT INTO {}{} VALUES".format(self.tablename, self.columns)
        else:
            return None
