from configuration import *
from utils.singleton import singleton
log = Loger()


@singleton
class DbConfigs:
    def __init__(self):
        self.configs = Configuration().configs
        self.initializeconfigs()

    def initializeconfigs(self):
        try:
            self.dbname = self.configs["dbname"]
            self.tablename = self.configs["tablename"]
            self.user = self.configs["user"]
            self.password = self.configs["password"]
            self.host = self.configs["host"]
            self.createdbfile = self.configs["createdbfile"]
            self.createblefile = self.configs["createtablefile"]
            self.testinsert = self.configs["testinsert"]
            self.testdelete = self.configs["testdelete"]
            self.testselect = self.configs["testselect"]
            self.testvalues = self.configs["testvalues"]
            log.INFO("Configurations loaded to DbConfigs.")
        except KeyError as err:
            log.ERROR("Configuration does not fits arguments. {}".format(err))
            sys.exit(1)
