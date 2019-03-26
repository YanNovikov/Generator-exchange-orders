from configurations.dbconfigs import *
from RowInsertHat import *
proprties = DbConfigs()
class OrdersInsertRow:
    def __init__(self, order):
        self.order = order
        self.hat = RowInsertHat(proprties.tablename, self.order).getHat()
        self.inserts = self.getOrdersInserts()

    def getInsertRow(self, index):
        row = "("
        for item in self.order.__dict__.items():
            if item[0] == "status" or item[0] == "date":
                row += "'{}',".format(item[1][index])
            elif item[0] == "px" or item[0] == "vol":
                row += "{},".format(item[1])
            else:
                row += "'{}',".format(item[1])
        row = row[:-1]
        return self.hat + row + ")"

    def getOrdersInserts(self):
        inserts = []
        for i in range(0, len(self.order.status)):
            if self.order.status[i] is not None:
                insert = self.getInsertRow(i)
                inserts.append(insert)
        return inserts
