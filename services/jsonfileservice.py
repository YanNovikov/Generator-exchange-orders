import json

from fileservice import *

class JsonFileService(FileService):
    def writeline(self, message):
        if self.isopened:
            self.file.write("{}\n".format(message))
            return True
        else:
            if self.open():
                self.writeline(message)
            else:
                print "Error found while writing to {}. Stopped on a string:\n{}\n.".format(self.filename, message)
                return False

    def writelines(self, messages):
        for msg in messages:
            if self.writeline(msg):
                pass
            else:
                return

    def read(self):
        if self.isopened:
            names = json.load(self.file)
            return names
        else:
            if self.open():
                self.read()
            else:
                print "Error found while reading from {}.\n.".format(self.filename)
                return False
