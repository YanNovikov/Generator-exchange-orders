from models.OrdersPositions import *
from utils.randfunctions import *
log = Loger()

class OrdersObject:
    def __init__(self, num, zone):
        try:
            self.zone = zone
            self.id = OrderID(num).get()
            self.direction = Direction(self.id).get()
            self.currencypair = CurrencyPair(self.id).get()
            self.px = Px(self.id).get()
            self.vol = Vol(self.id).get()
            self.dates = Dates(self.id).get()
            self.statuses = self.getStatus()
        except Exception as err:
            log.ERROR("Error while creating an order with id: {}. Message: {}".format(self.id, err.message))

    def getStatus(self):
        if self.zone == "Red":
            return Statuses(getRedStatus, self.id).get()
        elif self.zone == "Blue":
            return Statuses(getBlueStatus, self.id).get()
        elif self.zone == "Green":
            return Statuses(getGreenStatus, self.id).get()
        else:
            log.ERROR("Wrong zone name has been put.")

