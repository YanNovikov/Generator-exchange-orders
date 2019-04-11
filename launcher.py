from __future__ import unicode_literals
from models.Generator import *
from services.rabbitmq.service import *
from services.database.mysql.crud import *

def initialize(args):

    if len(args) == 3:
        Loger().setLogermode(args[2])
        Reporter().initialize()
        Configuration().__init__(args[1])
    else:
        log.WARNING("Not all arguments are set. Try python launcher.py [configs.json/.xml] [INFO/DEBUG]")

    GeneratorConfigs().initializeconfigs()
    DbConfigs().initializeconfigs()
    MessageConfigs().initializeconfigs()

def execute():
    database = MySqlService(True)
    createTable(database, database.conn.dbname, DbConfigs().createtablefile, DbConfigs().tablename)
    database.disconnect()

    executor = Generator()
    executor.generate()

    # dropDatabase(DbConfigs().dbname, DbConfigs())
    # createDatabase(DbConfigs().dbname, DbConfigs())


def finalize():
    Reporter().finalize(GeneratorConfigs())


if __name__ == "__main__":
    initialize(sys.argv)
    execute()
    finalize()
