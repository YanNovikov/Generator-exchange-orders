from configuration import *
from utils.singleton import singleton
log = Loger()


@singleton
class MessageConfigs:
    def __init__(self):
        self.configs = Configuration().configs

    def initializeconfigs(self):
        try:
            self.queuename = self.configs["queuename"]
            log.INFO("Configurations loaded to MessageConfigs.")
        except KeyError as err:
            log.ERROR("Configuration does not fits arguments. {}".format(err))
            sys.exit(1)
