from __future__ import unicode_literals
from configurations.dbconfigs import *
from utils.insertheadermaker import *
from utils.randfunctions import *
import services.proto.orderinfo_pb2 as OrderInformation


class OrdersInfo:
    def __init__(self, order):
        self.order = order
        self.hat = InsertHeaderMaker(DbConfigs().tablename, self.order).getHat()
        self.inserts = self.getInserts()
        self.csvrows = self.getCSV()
        self.protos = self.getProto()

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


    def getProto(self):
        protos = []
        for i in range(0, len(self.order.status)):
            if self.order.status[i] is not None:
                proto = self.getOneProto(i)
                protos.append(proto)
        return protos

    def getInsert(self, index):
        values = " ("
        for item in self.order.__dict__.items():

            if item[0] == "status" or item[0] == "orderdate":
                values += "'{}',".format(item[1][index])

            elif item[0] == "initprice" or item[0] == "fillprice" or item[0] == "initvolume" or item[0] == "fillvolume":
                values += "{},".format(item[1])

            else:
                values += "'{}',".format(item[1])

        values = values[:-1]
        return "{}{})".format(self.hat, values)

    def getOneCSV(self, index):
        row = ""
        if index == 2:
            if self.order.status[index] == "Filled":
                self.order.fillprice = self.order.initprice
                self.order.fillvolume = self.order.initvolume
            elif self.order.status[index] == "Partial-filled":
                self.order.fillprice = round(getChangedValue(self.order.initprice, self.order.id), 5)
                self.order.fillvolume = round(getChangedValue(self.order.initvolume, self.order.id), 2)
        else:
            self.order.fillprice = 0
            self.order.fillvolume = 0
        self.order.primaryid = DbConfigs().getUniqueId()

        for item in self.order.__dict__.items():
            if item[0] == "status" or item[0] == "orderdate":
                row += "{},".format(item[1][index])
            else:
                row += "{},".format(item[1])
        row = row[:-1]
        return row

    def getOneProto(self, index):
        result = OrderInformation.OrderInfo()
        result.primaryid = DbConfigs().getUniqueId()
        result.id = self.order.id
        result.direction = self.order.direction
        result.currencypair = self.order.currencypair

        result.status = self.order.status[index]
        result.orderdate = self.order.orderdate[index]

        if index == 2:
            if self.order.status[index] == "Filled":
                self.order.fillprice = self.order.initprice
                self.order.fillvolume = self.order.initvolume
            elif self.order.status[index] == "Partial-filled":
                self.order.fillprice = round(getChangedValue(self.order.initprice, self.order.id), 5)
                self.order.fillvolume = round(getChangedValue(self.order.initvolume, self.order.id), 2)
        else:
            self.order.fillprice = 0
            self.order.fillvolume = 0

        result.initprice = float(self.order.initprice)
        result.initvolume = float(self.order.initvolume)
        result.fillprice = float(self.order.fillprice)
        result.fillvolume = float(self.order.fillvolume)

        result.tag = self.order.tag
        result.description = self.order.description

        return result.SerializeToString()


