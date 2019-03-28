
from OrdersObject import *
from OrdersInsert import *

class OrdersBatch:
    def __init__(self, size, index, zone):
        self.index = index
        self.zone = zone
        self.objects = self.getObjects(size)
        self.inserts = self.getInserts()

    def getObjects(self, size):
        objects = []
        for i in range(self.index, self.index+size):
            objects.append(OrdersObject(i, self.zone))
        return objects

    def getInserts(self):
        inserts = []
        for obj in self.objects:
            for insert in OrdersInsert(obj).inserts:
                inserts.append(insert)
        return inserts
