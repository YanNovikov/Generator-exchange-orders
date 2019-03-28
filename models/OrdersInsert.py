from configurations.dbconfigs import *
from InsertHeader import *
proprties = DbConfigs()
class OrdersInsert:
    def __init__(self, order):
        self.order = order
        self.hat = InsertHeader(proprties.tablename, self.order).getHat()
        self.inserts = self.getInserts()

    def getInsert(self, index):
        row = "("
        for item in self.order.__dict__.items():
            if item[0] == "status" or item[0] == "orderdate":
                row += "'{}',".format(item[1][index])
            elif item[0] == "price" or item[0] == "volume":
                row += "{},".format(item[1])
            else:
                row += "'{}',".format(item[1])
        row = row[:-1]
        return "{}{})".format(self.hat, row)

    def getInserts(self):
        inserts = []
        for i in range(0, len(self.order.status)):
            if self.order.status[i] is not None:
                insert = self.getInsert(i)
                inserts.append(insert)
        return inserts
