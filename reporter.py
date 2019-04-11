from __future__ import unicode_literals
import operator
from services.file.txtfileservice import *
from datetime import datetime
import math
import threading

@singleton
class Reporter:
    def __init__(self):
        self.log = Loger()
        self.fileworker = TxtFileService("files/reports/{}".format(datetime.now()), "a+")
        self.checkpointno = 1
        self.insertrowscount = 0
        self.consumedmsgcount = 0
        self.sendmsgcount = 0
        self.generatedorderscount = 0
        self.writentofilerowscount = 0
        self.redzonecount = 0
        self.redzoneinserts = 0
        self.greenzonecount = 0
        self.greenzoneinserts = 0
        self.bluezonecount = 0
        self.bluezoneinserts = 0
        self.final = False

    def initialize(self):
        self.startedat = datetime.utcnow()
        self.fileworker.open()
        self.__reports = {}
        self.checkpoint()

    def addReport(self, methodname, tc):
        try:
            if methodname in self.__reports.keys():
                self.__reports[methodname].append(round(tc, 3))
            else:
                self.__reports[methodname] = []
                self.__reports[methodname].append(round(tc, 3))
            self.log.DEBUG("[Reporter]: method='{}' {}".format(methodname, round(tc, 3)))

        except KeyError as err:
            self.log.ERROR("Wrong method name is used. {}".format(str(err)))

        except AttributeError as err:
            self.initialize()
            self.log.WARNING("Maybe you forgot to start reporter. it is on now. {}".format(str(err)))
            self.addReport(methodname, tc)

    def finalize(self, prop):
        self.final = True
        self.stopedat = datetime.utcnow()
        total = self.stopedat - self.startedat

        parameters = ["Orders to be generated: {}".format(prop.orderscount),
                      "Red part: {}%".format(math.trunc(prop.redpart * 100)),
                      "Green part: {}%".format(math.trunc(prop.greenpart * 100)),
                      "Blue part: {}%".format(math.trunc(prop.bluepart * 100)),
                      "Started at {}".format(self.startedat.strftime('%d.%m.%Y %H:%M:%S.%f')[:-3]),
                      "Finished at {}".format(self.stopedat.strftime('%d.%m.%Y %H:%M:%S.%f')[:-3]),
                      "Total time is {} s".format(total.microseconds / 100000),
                      "\n.:Method:.  =>  .:Time:.\n"]

        self.fileworker.writelines(parameters)

        data = sorted(self.__reports.items(), key=operator.itemgetter(1))
        for row in data:
            key = row[0]
            values = row[1]
            if len(values) > 1:
                report = "'{}' => \n\tMax: {} ms\n\tAverage: {} ms\n\tMin: {} ms\n\tSummary: {} ms"
                report = report.format(key, max(values), round(math.fsum(values) / len(values), 3), min(values),
                                       round(math.fsum(values), 3))
            else:
                report = "'{}' => {} ms".format(key, values)

            self.fileworker.writeline(report)

        parameters = ["\nGenerated objects count: {}".format(self.generatedorderscount),
                      "Rows in csv written to file: {}".format(self.writentofilerowscount),
                      "Send messages count: {}".format(self.sendmsgcount),
                      "Consumed messages count: {}".format(self.consumedmsgcount),
                      "Rows inserted: {}".format(self.insertrowscount)]

        self.fileworker.writelines(parameters)

        self.log.INFO("Report is made in file {}.".format(self.fileworker.filename))

    def checkpoint(self):
        if self.checkpointno < 5 and self.final is False:
            stopedat = datetime.utcnow()
            total = stopedat - self.startedat

            self.fileworker.writeline("\nCheckpoint number: {}\n".format(self.checkpointno))
            parameters = ["After start: {} s".format(total.microseconds / 100000),
                          "Red zone: objects = {}, inserts = {}".format(self.redzonecount, self.redzoneinserts),
                          "Green zone: objects = {}, inserts = {}".format(self.greenzonecount, self.greenzoneinserts),
                          "Blue zone: objects = {}, inserts = {}".format(self.bluezonecount, self.bluezoneinserts),
                          "Generated objects count: {}".format(self.generatedorderscount),
                          "Rows in csv written to file: {}".format(self.writentofilerowscount),
                          "Send messages count: {}".format(self.sendmsgcount),
                          "Consumed messages count: {}".format(self.consumedmsgcount),
                          "Rows inserted: {}\n".format(self.insertrowscount)]

            self.fileworker.writelines(parameters)
            self.checkpointno += 1

            threading.Timer(2, self.checkpoint).start()
