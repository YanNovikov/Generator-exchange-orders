import datetime
from utils.singleton import singleton


@singleton
class Loger:
    def __init__(self, loggermode="INFODEBUGWARNING"):
        self.mode = loggermode
        self.filename = "logs/{}".format(datetime.datetime.now())
        self.writeMessage("INFO", "Logger started in default mode.")

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
        if self.mode.__contains__("WARNING"):
            self.writeMessage("WARNING", msg)

    def writeMessage(self, tag, msg):
        print "[{}]: {}".format(tag, msg)
        try:
            with open(self.filename, "a+") as file:
                file.write("[{}]: {}\n".format(tag, msg))
        except IOError as err:
            print "[ERROR]: Can not write to logfile. {}\n".format(str(err))
            
    def setLogermode(self, mode):
        self.mode = mode
        self.writeMessage("INFO", "Logger mode is now set in {}.".format(mode))
