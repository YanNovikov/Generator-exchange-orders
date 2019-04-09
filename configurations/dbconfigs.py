from __future__ import unicode_literals
from configurations.configuration import *
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
            self.uniqueid = 0
            log.INFO("Configurations for database usage loaded.")
        except KeyError as err:
            log.ERROR("Configuration does not fits arguments. No {} field is there".format(str(err)))
            sys.exit(1)

    def getUniqueId(self):
        self.uniqueid += 1
        return self.uniqueid
