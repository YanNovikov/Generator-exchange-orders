from __future__ import unicode_literals
from configurations.generatorconfigs import *


class ObjectProperty:
    def __init__(self, num):
        self.properties = GeneratorConfigs()
        self.value = self.createvalue(num)

    @abstractmethod
    def get(self):
        return self.value

    @abstractmethod
    def createvalue(self, num):
        pass
