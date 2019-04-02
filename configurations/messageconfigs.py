from configuration import *
from utils.singleton import singleton


@singleton
class MessageConfigs:
    def __init__(self):
        pass

    def initializeconfigs(self):
        try:
            configs = Configuration().configs
            self.queuename = configs["queuename"]
            log.INFO("Configurations for messaging loaded.")
        except KeyError as err:
            log.ERROR("Configuration does not fits arguments. {}".format(err))
            sys.exit(1)
