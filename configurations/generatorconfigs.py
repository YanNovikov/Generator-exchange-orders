from __future__ import unicode_literals
from configurations.configuration import *
from utils.singleton import singleton
import time
import math
from datetime import datetime
log = Loger()


@singleton
class GeneratorConfigs:
    def __init__(self):
        pass

    def initializeconfigs(self):
        try:
            configs = Configuration().configs
            self.datafilename = configs["datafilename"]
            self.batchcount = configs["batchcount"]
            self.orderscount = configs["orderscount"]
            self.redpart = configs["redpart"]
            self.greenpart = configs["greenpart"]
            self.bluepart = configs["bluepart"]
            self.startdate = time.mktime(datetime.strptime(configs["startdate"], "%d.%m.%Y %H:%M:%S").timetuple())
            self.finishdate = time.mktime(datetime.strptime(configs["finishdate"], "%d.%m.%Y %H:%M:%S").timetuple())
            self.status = configs["status"]
            self.currencypairs = configs["currencypairs"]
            self.tags = configs["tags"]
            self.dirrection = configs["dirrection"]
            self.descriptions = configs["descriptions"]
            self.maxpx = configs["maxpx"]
            self.minpx = configs["minpx"]
            self.maxvol = configs["maxvol"]
            self.minvol = configs["minvol"]
            self.pxseed = (self.maxpx - self.minpx + 1) * 100
            self.volseed = (self.maxvol - self.minvol + 1) * 10
            self.datediff = self.finishdate - self.startdate
            self.batch = self.getCorrectBatch(self.orderscount, self.batchcount)
            self.redbatch = self.getOneBatch(self.batch, self.redpart)
            self.bluebatch = self.getOneBatch(self.batch, self.bluepart)
            self.greenbatch = self.getOneBatch(self.batch, self.greenpart)
            self.redgreenblue = self.redbatch + self.bluebatch + self.greenbatch
            self.lastbatch = self.getLastBatch(self.orderscount, self.redgreenblue * self.batchcount)
            log.INFO("Configurations for generating loaded.")
        except KeyError as err:
            log.ERROR("Configuration does not fits arguments. {}".format(err))
            sys.exit(1)

    def getCorrectBatch(self, ocount, bcount):
        return math.trunc(ocount / bcount)

    def getLastBatch(self, ocount, bcount):
        return ocount - bcount

    def getOneBatch(self, batch, part):
        return math.trunc(batch * part)
