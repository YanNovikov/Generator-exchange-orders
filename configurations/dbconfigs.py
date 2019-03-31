from configuration import *
from utils.singleton import singleton
log = Loger()


@singleton
class DbConfigs:
    def __init__(self):
        pass

    def initializeconfigs(self):
        try:
            configs = Configuration().configs
            self.dbname = configs["dbname"]
            self.tablename = configs["tablename"]
            self.user = configs["user"]
            self.password = configs["password"]
            self.host = configs["host"]
            self.createtablefile = configs["createtablefile"]
            self.testselect = configs["testselect"]
            log.INFO("Configurations for database usage loaded.")
        except KeyError as err:
            log.ERROR("Configuration does not fits arguments. No {} field is there".format(err))
            sys.exit(1)
