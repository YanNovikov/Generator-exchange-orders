from __future__ import unicode_literals
from models.OrdersObject import *
from models.OrdersInfo import *

class OrdersBatch:
    def __init__(self, size, index, zone):
        self.index = index
        self.zone = zone
        self.objects = self.getObjects(size)
        self.inserts = self.getInserts()
        self.csvrows = self.getCsvRows()
        self.protos = self.getProtoc()

    def getObjects(self, size):
        objects = []
        for i in range(self.index, self.index+size):
            objects.append(OrdersObject(i, self.zone))
        return objects

    def getCsvRows(self):
        csvrows = []
        for obj in self.objects:
            for csvrow in OrdersInfo(obj).csvrows:
                csvrows.append(csvrow)
        return csvrows

    def getInserts(self):
        inserts = []
        for obj in self.objects:
            for insert in OrdersInfo(obj).inserts:
                inserts.append(insert)
        return inserts

    def getProtoc(self):
        protoc = []
        for obj in self.objects:
            for proto in OrdersInfo(obj).protos:
                protoc.append(proto)
        return protoc
