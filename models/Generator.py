from configurations.generatorconfigs import *
from services.txtfileservice import *
from models.OrdersObject import *
from OrdersBatch import *

log = Loger()


class Generator:
    def __init__(self):
        self.properties = GeneratorConfigs()
        self.fileworker = TxtFileService(self.properties.datafilename, "a+")
        self.index = 0
    def generate(self):
        cleanFile(self.properties.datafilename)

        for index in range(0, self.properties.batchcount):
            self.getEveryBatch()
        self.getFinalBatch()

        log.INFO("Orders created: {}".format(self.index))

    def getEveryBatch(self):

        log.DEBUG("Red zone ==== {}".format(self.properties.redbatch))
        self.fileworker.writeline("--Red zone")
        orders = OrdersBatch(self.properties.redbatch, self.index, "Red")
        self.fileworker.writelines(orders.inserts)
        self.index += self.properties.redbatch

        log.DEBUG("Green zone ==== {}".format(self.properties.greenbatch))
        self.fileworker.writeline("--Green zone")
        orders = OrdersBatch(self.properties.greenbatch, self.index, "Green")
        self.fileworker.writelines(orders.inserts)
        self.index += self.properties.greenbatch

        log.DEBUG("Blue zone ==== {}".format(self.properties.bluebatch))
        self.fileworker.writeline("--Blue zone")
        orders = OrdersBatch(self.properties.bluebatch, self.index, "Blue")
        self.fileworker.writelines(orders.inserts)
        self.index += self.properties.bluebatch

        log.DEBUG("Batch created {} rows.".format(self.properties.redgreenblue))

    def getFinalBatch(self):
        log.DEBUG("Additional zone ==== {}".format(self.properties.lastbatch))
        self.fileworker.writeline("--Additional zone")
        pointer = 0
        while self.index < self.properties.orderscount:
                if pointer == 0:
                    zone = "Green"
                    pointer += 1
                elif pointer == 1:
                    zone = "Red"
                    pointer += 1
                elif pointer == 2:
                    zone = "Blue"
                    pointer = 0
                order = OrdersObject(self.index, zone)
                self.fileworker.writelines(OrdersInsert(order).inserts)
                self.index += 1



