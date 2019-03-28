import os
from abc import abstractmethod

def getFilesFromDir(dirname):
    return os.listdir(dirname)

def cleanFile(filename):
    try:
        with open(filename, "r+") as file:
            file.truncate()
            print ("File '{}' has been just cleaned.".format(file.name))
    except IOError, err:
        print (err.message)

class FileService:

    def __init__(self, filename, mode):
        self.file = None
        self.filename = filename
        self.openmode = mode
        self.isopened = None

    def open(self):
        try:
            self.file = open(self.filename, self.openmode)
            print "{} opened in mode {} - Success.".format(self.filename, self.openmode)
            self.isopened = True
            return True
        except IOError as err:
            print "Can not open file {}. Message: {}.".format(self.filename, str(err))
            return False

    def close(self):
        self.file.close()
        self.isopened = False

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

