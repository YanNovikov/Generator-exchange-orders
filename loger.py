from __future__ import unicode_literals
import datetime
import os

from utils.singleton import singleton

# 1 TRACE
# 2 DEBUG
# 3 INFO
# 4 WARNING
# 5 ERROR
# 6 CRITICAL
# 7 FATAL

# output = '-c' - console
# output = '-f' - file
# output = '-cf' - console and file

@singleton
class Logger:
    def __init__(self):
        self.mode = 3
        self.output = "-cf"
        self.filename = "files/logs/{}".format(datetime.datetime.now().ctime())
        self.__LOGGER("Started with default settings.")

    def TRACE(self, msg):
        if self.mode < 2:
            self.writeMessage("TRACE", msg)

    def DEBUG(self, msg):
        if self.mode < 3:
            self.writeMessage("DEBUG", msg)

    def INFO(self, msg):
        if self.mode < 4:
            self.writeMessage("INFO", msg)

    def WARNING(self, msg):
        if self.mode < 5:
            self.writeMessage("WARNING", msg)

    def ERROR(self, msg):
        if self.mode < 6:
            self.writeMessage("ERROR", msg)

    def CRITICAL(self, msg):
        if self.mode < 7:
            self.writeMessage("CRITICAL", msg)

    def FATAL(self, msg):
        self.writeMessage("FATAL", msg)

    def __LOGGER(self, msg):
        self.writeMessage("LOGGER", msg)

    def writeMessage(self, tag, msg):
        if self.output.__contains__('c'):
            print("[{}]: {}".format(tag, msg))
        if self.output.__contains__('f'):
            try:
                with open(self.filename, "a+") as file:
                    file.write("[{}]: {}\n".format(tag, msg))
            except IOError as err:
                print("[ERROR]: Can not write to logfile. {}".format(str(err)))

    def setLoggeroutput(self, output):
        if output == "-c":
            self.writeMessage("LOGGER", "Logger output goes to console now.")
            if os.path.exists(self.filename):
                os.remove(self.filename)
        elif output == "-f":
            self.writeMessage("LOGGER", "Logger output goes to file {}.".format(self.filename))

        self.output = output
            
    def setLoggermode(self, mode="info"):
        modenames = {
            'trace': 1,
            'debug': 2,
            'info': 3,
            'warning': 4,
            'error': 5,
            'critical': 6,
            'fatal': 7
        }
        if mode.lower() in modenames.keys():
            self.mode = modenames[mode.lower()]
            self.writeMessage("LOGGER", "Logger mode is now set to {}.".format(mode))
        else:
            self.mode = modenames['info']
            self.writeMessage("WARNING", "Wrong logger mode is send. Continue working in default.")
