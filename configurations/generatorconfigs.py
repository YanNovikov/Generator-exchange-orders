from configuration import *
from utils.singleton import singleton
from utils.randfunctions import *
import time
from datetime import datetime
log = Loger()


@singleton
class GeneratorConfigs:
    def __init__(self):
        self.configs = Configuration().configs
        self.initializeconfigs()

    def initializeconfigs(self):
        try:
            self.datafilename = self.configs["datafilename"]
            self.batchcount = self.configs["batchcount"]
            self.orderscount = self.configs["orderscount"]
            self.redpart = self.configs["redpart"]
            self.greenpart = self.configs["greenpart"]
            self.bluepart = self.configs["bluepart"]
            self.startdate = time.mktime(datetime.strptime(self.configs["startdate"], "%d.%m.%Y %H:%M:%S").timetuple())
            self.finishdate = time.mktime(datetime.strptime(self.configs["finishdate"], "%d.%m.%Y %H:%M:%S").timetuple())
            self.status = self.configs["status"]
            self.currencypairs = self.configs["currencypairs"]
            self.tags = self.configs["tags"]
            self.dirrection = self.configs["dirrection"]
            self.maxpx = self.configs["maxpx"]
            self.minpx = self.configs["minpx"]
            self.maxvol = self.configs["maxvol"]
            self.minvol = self.configs["minvol"]
            self.datediff = self.finishdate - self.startdate
            self.batch = self.getCorrectBatch(self.orderscount, self.batchcount)
            self.redbatch = self.getOneBatch(self.batch, self.redpart)
            self.bluebatch = self.getOneBatch(self.batch, self.bluepart)
            self.greenbatch = self.getOneBatch(self.batch, self.greenpart)
            self.lastbatch = self.getLastBatch(self.orderscount, self.batchcount)
            self.redgreenblue = self.redbatch + self.bluebatch + self.greenbatch
            log.INFO("Configurations loaded to GeneratorConfigs.")
        except KeyError as err:
            log.ERROR("Configuration does not fits arguments. {}".format(err))
            sys.exit(1)

    def getCorrectBatch(self, ocount, bcount):
        return math.trunc(ocount / bcount)

    def getLastBatch(self, ocount, bcount):
        return ocount - self.getCorrectBatch(ocount, bcount) * bcount

    def getOneBatch(self, batch, part):
        return math.trunc(batch * part)
