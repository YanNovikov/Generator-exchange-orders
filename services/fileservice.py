import os
class FileService:
    def getFilesFromDir(self, dirname):
        return os.listdir(dirname)