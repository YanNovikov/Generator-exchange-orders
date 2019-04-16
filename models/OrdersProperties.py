from __future__ import unicode_literals
from models.ObjectProperty import ObjectProperty
from utils.randfunctions import *
from configurations.generatorconfigs import *
from datetime import datetime

properties = GeneratorConfigs()


class OrderID(ObjectProperty):
    def __init__(self, num):
        ObjectProperty.__init__(self, num)

    def createvalue(self, num):
        part1 = getSinExp(num)
        part2 = getCosExp(num + 1)
        return int(("{}{}".format(math.trunc(part1 * 10000000), math.trunc(part2 * 10000000)))[:15])


class CurrencyPair(ObjectProperty):
     def __init__(self, num):
        ObjectProperty.__init__(self, num)

     def createvalue(self, num):
        return properties.currencypairs[math.trunc(math.fmod(num, len(properties.currencypairs)))]


class Tag(ObjectProperty):
    def __init__(self, num):
        ObjectProperty.__init__(self, num)

    def createvalue(self, num):
        return properties.tags[math.trunc(math.fmod(num, len(properties.tags)))]


class Direction(ObjectProperty):
    def __init__(self, num):
        ObjectProperty.__init__(self, num)

    def createvalue(self, num):
        return properties.dirrection[math.trunc(math.fmod(num, 2))]


class Px(ObjectProperty):
    def __init__(self, num):
        self.px = properties.pxseed
        ObjectProperty.__init__(self, num)

    def createvalue(self, num):
        return round(math.fmod(num, self.px) / 100 + properties.minpx, 5)


class Vol(ObjectProperty):
    def __init__(self, num):
        self.vol = properties.volseed
        ObjectProperty.__init__(self, num)

    def createvalue(self, num):
        return round(math.fmod(num, self.vol) / 10 + properties.minvol, 1)

class Description(ObjectProperty):
    def __init__(self, num):
        ObjectProperty.__init__(self, num)

    def createvalue(self, num):
        return properties.descriptions[math.trunc(math.fmod(num, len(properties.descriptions)))]

class Dates(ObjectProperty):
    def __init__(self, num):
        ObjectProperty.__init__(self, num)

    def createvalue(self, num):
        difference = math.fmod(num, properties.datediff)
        date = properties.startdate + difference
        dates = []
        firststep = math.fmod(num, 50)
        secondstep = math.fmod(num, 150)
        miliseconds1 = math.trunc(math.fmod(num, 1000))
        miliseconds2 = math.trunc(math.fmod(num * getSinExp(num), 1000))
        miliseconds3 = math.trunc(math.fmod(num * getCosExp(num), 1000))
        dates.append("{}.{}".format(datetime.fromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S'), miliseconds1))
        dates.append("{}.{}".format(datetime.fromtimestamp(date + firststep).strftime('%Y-%m-%d %H:%M:%S'), miliseconds2))
        dates.append("{}.{}".format(datetime.fromtimestamp(date + firststep + secondstep).strftime('%Y-%m-%d %H:%M:%S'), miliseconds3))
        return dates


class Statuses(ObjectProperty):
    def __init__(self, fun, num):
        self.fum = fun
        ObjectProperty.__init__(self, num)

    def createvalue(self, num):
        return self.fum(num)
