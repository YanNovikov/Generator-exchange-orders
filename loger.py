import datetime
from utils.singleton import singleton


@singleton
class Loger:
    def __init__(self, loggermode="INFODEBUG"):
        self.mode = loggermode
        self.filename = "logs/{}".format(datetime.datetime.now())

    def INFO(self, msg):
        if self.mode.__contains__("INFO"):
            with open(self.filename, "a+") as file:
                file.writelines("[INFO]: {}\n".format(msg))
            print "[INFO]: " + msg

    def DEBUG(self, msg):
        if self.mode.__contains__("DEBUG"):
            with open(self.filename, "a+") as file:
                file.writelines("[DEBUG]: {}\n".format(msg))
            print "[DEBUG]: " + msg

    def ERROR(self, msg):
        print "[ERROR]: " + msg
        with open(self.filename, "a+") as file:
            file.writelines("[ERROR]: {}\n".format(msg))

    def CRITICAL(self, msg):
        print "[CRITICAL]: " + msg
        with open(self.filename, "a+") as file:
            file.writelines("[CRITICAL]: {}\n".format(msg))

    def WARNING(self, msg):
        print "[WARNING]: " + msg
        with open(self.filename, "a+") as file:
            file.writelines("[WARNING]: {}\n".format(msg))