from configurations.dbconfigs import *
from utils.InsertHeaderMaker import *


class OrdersInsert:
    def __init__(self, order):
        self.order = order
        self.hat = InsertHeaderMaker(DbConfigs().tablename, self.order).getHat()
        self.inserts = self.getInserts()

    def getInsert(self, index):
        values = " ("
        for item in self.order.__dict__.items():

            if item[0] == "status" or item[0] == "orderdate":
                values += "'{}',".format(item[1][index])

            elif item[0] == "price" or item[0] == "volume":
                    values += "{},".format(item[1])

            else:
                values += "'{}',".format(item[1])

        values = values[:-1]
        return "{}{})".format(self.hat, values)

    def getInserts(self):
        inserts = []
        for i in range(0, len(self.order.status)):
            if self.order.status[i] is not None:
                insert = self.getInsert(i)
                inserts.append(insert)
        return inserts
