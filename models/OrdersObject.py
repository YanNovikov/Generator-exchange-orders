from __future__ import unicode_literals
from models.OrdersProperties import *
from utils.randfunctions import *
from models.OrdersInfo import *
log = Loger()


class OrdersObject:
    def __init__(self, num, zone):
        try:
            self.id = OrderID(num).get()
            self.direction = Direction(self.id).get()
            self.currencypair = CurrencyPair(self.id).get()
            self.initprice = Px(self.id).get()
            self.initvolume = Vol(self.id).get()
            self.fillprice = 0
            self.fillvolume = 0
            self.orderdate = Dates(self.id).get()
            self.status = self.getStatus(zone)
            self.tag = Tag(self.id).get()
            self.description = Description(self.id).get()
        except Exception as err:
            log.ERROR("Error while creating an order with id: {}. Message: {}".format(self.id, err.message))

    def getStatus(self, zone):
        if zone == "Red":
            return Statuses(getRedStatus, self.id).get()
        elif zone == "Blue":
            return Statuses(getBlueStatus, self.id).get()
        elif zone == "Green":
            return Statuses(getGreenStatus, self.id).get()
        else:
            log.ERROR("Wrong zone name has been put. It is now set to 'Red'.")
            return Statuses(getRedStatus, self.id).get()

    def getOrdersRow(self):
        return OrdersInfo(self)

    def __str__(self):
        return "('{}','{}','{}',{},{},{},{},'{}')".format(self.id,
                                                       self.direction,
                                                       self.currencypair,
                                                       self.initprice,
                                                       self.initvolume,
                                                       self.fillprice,
                                                       self.fillvolume,
                                                       self.tag)

