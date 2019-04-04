from configurations.messageconfigs import *
from services.database.mysql.crud import *
from models.Generator import *
from services.database.mysql.service import *
from services.rabbitmq.service import *

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
    executor = Generator()
    executor.generate()

    database = MySqlService(nowopen=True)  # opens connection right here
    # dropTable(database, DbConfigs().tablename)
    createTable(database, database.conn.dbname, DbConfigs().createtablefile, DbConfigs().tablename)
    database.cleanTable()
    database.insertFromFile(GeneratorConfigs().datafilename, commiteverytime=False)  # if True commits after every insert
    database.commit()
    # database.selectValues()


def finalize():
    Reporter().finalize(GeneratorConfigs())


if __name__ == "__main__":
    initialize(sys.argv)
    execute()
    finalize()
