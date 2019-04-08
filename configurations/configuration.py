from __future__ import unicode_literals
from utils.singleton import singleton
from configurations.configloader import *


@singleton
class Configuration:
    def __init__(self, filename=None):
        if filename is None:
            self.configs = loadDefaults()
        else:
            try:
                self.configs = loadConfigs(filename)
            except IOError as err:
                log.ERROR("{}".format(str(err)))
                log.WARNING("'defaults.json' will be used instead of {}".format(filename))

    @abstractmethod
    def __initializeconfigs(self):
        pass