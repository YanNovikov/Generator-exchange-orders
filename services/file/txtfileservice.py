from services.file.fileservice import *


class TxtFileService(FileService):
    def writeline(self, message):
        try:
            if self.isopened:
                self.file.write("{}\n".format(message))
                return True
            else:
                if self.open():
                    self.writeline(message)
        except IOError as err:
            self.log.ERROR(
                "Error found while writing to {}. Stopped on a string:\n{}\n. {}\n".format(self.filename, message,
                                                                                           str(err)))
            return False

    def writelines(self, messages):
        for msg in messages:
            if self.writeline(msg):
                pass
            else:
                return

    def read(self):
        try:
            if self.isopened:
                data = self.file.readlines()
                self.log.DEBUG("Read from {} - Success".format(self.filename))
                return data
            else:
                if self.open():
                    return self.read()
        except IOError as err:
            self.log.ERROR("Error found while reading from {}.\n {}\n".format(self.filename, str(err)))
            return None

