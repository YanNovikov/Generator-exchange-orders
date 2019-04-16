from __future__ import unicode_literals
from models.OrdersProperties import *
from models.OrdersInfo import *
log = Logger()


class OrdersObject:
    def __init__(self, num=0, zone="", createnow=True):
        if createnow is True:
            try:
                self.primaryid = 0
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
                log.ERROR("Error while creating an order with id: {}. Message: {}".format(self.id, str(err)))

    def setFromObject(self, one):
        try:
            self.primaryid = one.primaryid
            self.id = one.id
            self.direction = one.direction
            self.currencypair = one.currencypair
            self.initprice = round(one.initprice, 5)
            self.initvolume = round(one.initvolume, 2)
            self.fillprice = round(one.fillprice, 5)
            self.fillvolume = round(one.fillvolume, 2)
            self.orderdate = one.orderdate
            self.status = one.status
            self.tag = one.tag
            self.description = one.description
        except Exception as err:
            log.ERROR("Error while creating Order from object. Message: {}".format(str(err)))

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

    def __str__(self):
        return "('{}','{}','{}',{},{},{},{},'{}')".format(self.id,
                                                       self.direction,
                                                       self.currencypair,
                                                       self.initprice,
                                                       self.initvolume,
                                                       self.fillprice,
                                                       self.fillvolume,
                                                       self.tag)

