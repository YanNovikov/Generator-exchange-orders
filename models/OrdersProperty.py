from abc import abstractmethod


class OrdersProperty:
    def __init__(self, num):
        self.value = self.createvalue(num)

    @abstractmethod
    def get(self):
        return self.value

    @abstractmethod
    def createvalue(self, num):
        pass
