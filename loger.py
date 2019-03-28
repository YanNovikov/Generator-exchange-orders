import datetime
from utils.singleton import singleton
from services.txtfileservice import *

@singleton
class Loger:
    def __init__(self, loggermode="INFODEBUG"):
        self.mode = loggermode
        self.filename = "logs/{}".format(datetime.datetime.now())
        self.file = TxtFileService(self.filename, "a+")

    def INFO(self, msg):
        if self.mode.__contains__("INFO"):
            self.writeMessage("INFO", msg)

    def DEBUG(self, msg):
        if self.mode.__contains__("DEBUG"):
            self.writeMessage("DEBUG", msg)

    def ERROR(self, msg):
        self.writeMessage("ERROR", msg)

    def CRITICAL(self, msg):
        self.writeMessage("CRITICAL", msg)

    def WARNING(self, msg):
        self.writeMessage("WARNING", msg)

    def writeMessage(self, tag, msg):
        print "[{}]: {}".format(tag, msg)
        try:
            self.file.writeline("[{}]: {}".format(tag, msg))
        except IOError as err:
            print "[ERROR]: Can not write to logfile. {}\n".format(str(err))

