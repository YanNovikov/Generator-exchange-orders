from abc import abstractmethod
from configloader import *
from utils.singleton import singleton


@singleton
class Configuration:
    @abstractmethod
    def __init__(self):
        self.configs = loadConfigs()
    @abstractmethod
    def initializeconfigs(self):
        pass