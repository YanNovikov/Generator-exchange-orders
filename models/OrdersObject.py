from models.OrdersPositions import *
from utils.randfunctions import *
from OrdersInsert import *
log = Loger()

class OrdersObject:
    def __init__(self, num, zone):
        try:
            self.id = OrderID(num).get()
            self.direction = Direction(self.id).get()
            self.currencypair = CurrencyPair(self.id).get()
            self.px = Px(self.id).get()
            self.vol = Vol(self.id).get()
            self.date = Dates(self.id).get()
            self.status = self.getStatus(zone)
            self.tag = Tag(self.id).get()
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
        return OrdersInsert(self)

