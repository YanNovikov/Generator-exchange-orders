from OrdersProperties import OrdersProperty
from utils.randfunctions import *
from configurations.generatorconfigs import *
from datetime import datetime

properties = GeneratorConfigs()


class OrderID(OrdersProperty):
    def __init__(self, num):
        OrdersProperty.__init__(self, num)

    def createvalue(self, num):
        part1 = getSinExp(num)
        part2 = getCosExp(num + 1)
        return int(("{}{}".format(math.trunc(part1 * 100000000), math.trunc(part2 * 10000000)))[:15])


class CurrencyPair(OrdersProperty):
     def __init__(self, num):
        OrdersProperty.__init__(self, num)

     def createvalue(self, num):
        return properties.currencypairs[math.trunc(math.fmod(num, len(properties.currencypairs)))]


class Tag(OrdersProperty):
    def __init__(self, num):
        OrdersProperty.__init__(self, num)

    def createvalue(self, num):
        return properties.tags[math.trunc(math.fmod(num, len(properties.tags)))]



class Direction(OrdersProperty):
    def __init__(self, num):
        OrdersProperty.__init__(self, num)

    def createvalue(self, num):
        return properties.dirrection[math.trunc(math.fmod(num, 2))]


class Px(OrdersProperty):
    def __init__(self, num):
        self.px = (properties.maxpx - properties.minpx + 1) * 100
        OrdersProperty.__init__(self, num)

    def createvalue(self, num):
        return math.fmod(num, self.px) / 100 + properties.minpx


class Vol(OrdersProperty):
    def __init__(self, num):
        self.vol = properties.maxvol - properties.minvol + 1
        OrdersProperty.__init__(self, num)

    def createvalue(self, num):
        return math.fmod(num, self.vol) + properties.minvol


class Dates(OrdersProperty):
    def __init__(self, num):
        OrdersProperty.__init__(self, num)

    def createvalue(self, num):
        difference = math.fmod(num, properties.datediff)
        date = properties.startdate + difference
        dates = []
        firststep = math.fmod(num, 50)
        secondstep = math.fmod(num, 150)
        miliseconds1 = math.trunc(math.fmod(num, 1000))
        miliseconds2 = math.trunc(math.fmod(num * getSinExp(num), 1000))
        miliseconds3 = math.trunc(math.fmod(num * getCosExp(num), 1000))
        dates.append("{}.{}".format(datetime.fromtimestamp(date).strftime('%d.%m.%Y %H:%M:%S'), miliseconds1))
        dates.append("{}.{}".format(datetime.fromtimestamp(date + firststep).strftime('%d.%m.%Y %H:%M:%S'), miliseconds2))
        dates.append("{}.{}".format(datetime.fromtimestamp(date + firststep + secondstep).strftime('%d.%m.%Y %H:%M:%S'), miliseconds3))
        return dates

class Statuses(OrdersProperty):
    def __init__(self, fun, num):
        self.fum = fun
        OrdersProperty.__init__(self, num)

    def createvalue(self, num):
        return self.fum(num)