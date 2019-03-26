


class OrdersBatch:
    def __init__(self, size, index):
        self.objects = self.getObjects(size)
        self.inserts = self.getInserts(self.objects)

    def getObjects(self, size):
        pass

    def getInserts(self, objects):
        pass