from __future__ import unicode_literals
import os
from abc import abstractmethod
from loger import *


class FileService:
    def __init__(self, filename, mode):
        self.log = Loger()
        self.file = None
        self.filename = filename
        self.openmode = mode
        self.isopened = False

    def open(self):
        try:
            if self.isopened:
                self.log.DEBUG("{} already opened in mode {}.".format(self.filename, self.openmode))
                return True
            else:
                self.file = open(self.filename, self.openmode)
                self.log.DEBUG("{} opened in mode {} - Success.".format(self.filename, self.openmode))
                self.isopened = True
                return True
        except IOError as err:
            self.log.ERROR("Can not open file {}. Message: {}.".format(self.filename, str(err)))
            return False

    def close(self):
        if self.isopened:
            self.file.close()
            self.isopened = False
            self.log.DEBUG("File {} is closed - Success.".format(self.filename))
        else:
            self.log.DEBUG("File {} is not opened.".format(self.filename))

    @abstractmethod
    def writeline(self, message):
        pass

    @abstractmethod
    def writelines(self, messages):
        pass

    @abstractmethod
    def readline(self):
        pass

    @abstractmethod
    def read(self):
        pass

def cleanFile(filename):
    try:
        with open(filename, "r+") as file:
            file.truncate()
            Loger().DEBUG("File '{}' has been just cleaned.".format(file.name))
    except IOError as err:
        print (str(err))

