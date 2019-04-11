from __future__ import unicode_literals
from services.file.txtfileservice import *
from services.rabbitmq.service import *
import services.proto.orderinfo_pb2 as OrderInfo
from models.OrdersBatch import *
from utils.timeit import *


class Generator:
    def __init__(self):
        self.properties = GeneratorConfigs()
        self.fileworker = TxtFileService(self.properties.datafilename, "a+")
        self.rmqpublisher = RMQService()
        self.rmqconsumer = RMQService()
        self.dbselector = MySqlService(True)
        self.index = 1

    @timeit
    def generate(self):
        cleanFile(self.properties.datafilename)

        log.DEBUG("Red zone ==== {}".format(self.properties.redbatch))
        log.DEBUG("Green zone ==== {}".format(self.properties.greenbatch))
        log.DEBUG("Blue zone ==== {}".format(self.properties.bluebatch))

        self.fileworker.open()
        self.rmqpublisher.startSending()

        for index in range(0, self.properties.batchcount):
            log.DEBUG("Batch {}.".format(index))
            self.__getEveryBatch()
        if self.properties.lastbatch > 0:
            self.__getFinalBatch()

        log.INFO("Orders created: {}.".format(self.index - 1))
        log.INFO("All rows successfully added to file {}.".format(self.properties.datafilename))

        self.fileworker.close()
        self.rmqpublisher.stopSending()
        self.rmqconsumer.startConsuming()

        self.dbselector.selectValues()

    @timeit
    def __getEveryBatch(self):

        self.fileworker.writeline("--Red zone")
        orders = self.__getRedZone(self.properties.redbatch)
        self.__writeCSV(orders)
        self.rmqpublisher.sendObjects(orders.protos, "Red")

        self.fileworker.writeline("--Green zone")
        orders = self.__getGreenZone(self.properties.greenbatch)
        self.__writeCSV(orders)
        self.rmqpublisher.sendObjects(orders.protos, "Green")

        self.fileworker.writeline("--Blue zone")
        orders = self.__getBlueZone(self.properties.bluebatch)
        self.__writeCSV(orders)
        self.rmqpublisher.sendObjects(orders.protos, "Blue")

        log.DEBUG("Batch created {} objects.".format(self.properties.redgreenblue))

    @timeit
    def __getFinalBatch(self):
        log.DEBUG("Additional zone ==== {}".format(self.properties.lastbatch))
        self.fileworker.writeline("--Additional zone")
        flag = 0
        while self.index <= self.properties.orderscount:
                if flag == 0:
                    zone = "Green"
                    flag += 1
                elif flag == 1:
                    zone = "Red"
                    flag += 1
                elif flag == 2:
                    zone = "Blue"
                    flag = 0
                order = OrdersObject(self.index, zone)
                self.fileworker.writelines(OrdersInfo(order).csvrows)
                self.rmqpublisher.sendObjects(OrdersInfo(order).protos, zone)
                self.index += 1

    @timeit
    def __getRedZone(self, batch):
        orders = OrdersBatch(batch, self.index, "Red")
        Reporter().redzonecount += len(orders.objects)
        Reporter().redzoneinserts += len(orders.inserts)
        self.index += batch
        return orders

    @timeit
    def __getGreenZone(self, batch):
        orders = OrdersBatch(batch, self.index, "Green")
        Reporter().greenzonecount += len(orders.objects)
        Reporter().greenzoneinserts += len(orders.inserts)
        self.index += batch
        return orders

    @timeit
    def __getBlueZone(self, batch):
        orders = OrdersBatch(batch, self.index, "Blue")
        Reporter().bluezonecount += len(orders.objects)
        Reporter().bluezoneinserts += len(orders.inserts)
        self.index += batch
        return orders

    @timeit
    def __writeCSV(self, orders):
        self.fileworker.writelines(orders.csvrows)

    @timeit
    def __writeInserts(self, orders):
        self.fileworker.writelines(orders.inserts)

