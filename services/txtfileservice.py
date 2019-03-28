from fileservice import *


class TxtFileService(FileService):
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
