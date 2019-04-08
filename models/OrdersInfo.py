from __future__ import unicode_literals
from configurations.dbconfigs import *
from utils.InsertHeaderMaker import *
from utils.randfunctions import *


class OrdersInfo:
    def __init__(self, order):
        self.order = order
        self.hat = InsertHeaderMaker(DbConfigs().tablename, self.order).getHat()
        self.inserts = self.getInserts()
        self.csvrows = self.getCSV()

    def getInserts(self):
        inserts = []
        for i in range(0, len(self.order.status)):
            if self.order.status[i] is not None:
                insert = self.getInsert(i)
                inserts.append(insert)
        return inserts

    def getCSV(self):
        rows = []
        for i in range(0, len(self.order.status)):
            if self.order.status[i] is not None:
                row = self.getOneCSV(i)
                rows.append(row)
        return rows

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

    def getOneCSV(self, index):
        row = ""
        if index == 2:
            row += "!!!"
            if self.order.status[index] == "Filled":
                self.order.fillprice = self.order.initprice
                self.order.fillvolume = self.order.initvolume
            elif self.order.status[index] == "Partial-filled":
                self.order.fillprice = round(getChangedValue(self.order.initprice, self.order.id), 5)
                self.order.fillvolume = round(getChangedValue(self.order.initvolume, self.order.id), 2)
        else:
            self.order.fillprice = 0
            self.order.fillvolume = 0
        for item in self.order.__dict__.items():
            if item[0] == "status" or item[0] == "orderdate":
                row += "{},".format(item[1][index])
            else:
                row += "{},".format(item[1])
        row = row[:-1]
        return row
