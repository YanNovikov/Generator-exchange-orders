from __future__ import unicode_literals
import operator
from services.file.txtfileservice import *
from datetime import datetime
import math

@singleton
class Reporter:
    def __init__(self):
        self.log = Loger()
        self.fileworker = TxtFileService("files/reports/{}".format(datetime.now()), "a+")

    def initialize(self):
        self.startedat = datetime.utcnow()
        self.fileworker.open()
        self.__reports = {}

    def addReport(self, methodname, tc):
        try:
            if methodname in self.__reports.keys():
                self.__reports[methodname].append(round(tc, 3))
            else:
                self.__reports[methodname] = []
                self.__reports[methodname].append(round(tc, 2))
            self.log.DEBUG("[Reporter]: method='{}' {}".format(methodname, round(tc, 2)))

        except KeyError as err:
            self.log.ERROR("Wrong method name is used. {}".format(str(err)))

        except AttributeError as err:
            self.initialize()
            self.log.WARNING("Maybe you forgot to start reporter. it is on now. {}".format(str(err)))
            self.addReport(methodname, tc)

    def finalize(self, prop):
        self.stopedat = datetime.utcnow()
        total = self.stopedat - self.startedat

        parameters = ["Orders to be generated: {}".format(prop.orderscount),
                      "Red part: {}%".format(math.trunc(prop.redpart * 100)),
                      "Green part: {}%".format(math.trunc(prop.greenpart * 100)),
                      "Blue part: {}%".format(math.trunc(prop.bluepart * 100)),
                      "Started at {}".format(self.startedat.strftime('%d.%m.%Y %H:%M:%S.%f')[:-3]),
                      "Finished at {}".format(self.stopedat.strftime('%d.%m.%Y %H:%M:%S.%f')[:-3]),
                      "Total time is {} ms".format(total.microseconds / 1000),
                      "\n.:Method:.  =>  .:Time:.\n"]

        self.fileworker.writelines(parameters)

        data = sorted(self.__reports.items(), key=operator.itemgetter(1))
        for row in data:
            key = row[0]
            values = row[1]
            if len(values) > 1:
                report = "'{}' => \n\tMax: {} ms\n\tAverage: {} ms\n\tMin: {} ms\n\tSummary: {} ms".format(key,
                                                                                                        max(values),
                                                                                                        math.fsum(values)/len(values),
                                                                                                        min(values),
                                                                                                        math.fsum(values))
            else:
                report = "'{}' => {} ms".format(key, values)

            self.fileworker.writeline(report)

        self.log.INFO("Report is made in file {}.".format(self.fileworker.filename))
