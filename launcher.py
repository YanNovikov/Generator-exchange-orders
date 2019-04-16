from __future__ import unicode_literals

import getopt

from models.Generator import *
from services.rabbitmq.service import *
from services.database.mysql.crud import *


def initialize(args):
    try:
        Reporter().initialize()
        args.remove(args[0])
        optlist, args = getopt.getopt(args, 'fc', ['loggermode=', 'configs='])
        for opt, val in optlist:
            if opt == "-c":
                Logger().setLoggeroutput(opt)
            elif opt == "-f":
                Logger().setLoggeroutput(opt)
            elif opt == "--loggermode":
                Logger().setLoggermode(val)
            elif opt == "--configs":
                Configuration().__init__(val)
    except getopt.GetoptError as err:
        print(str(err))


    log.INFO("Initializing application...")

    GeneratorConfigs().initializeconfigs()
    DbConfigs().initializeconfigs()
    MessageConfigs().initializeconfigs()

    database = MySqlService(True)
    # dropTable(database, DbConfigs().tablename)
    createTable(database, database.conn.dbname, DbConfigs().createtablefile, DbConfigs().tablename)
    database.cleanTable()
    database.commit()
    database.disconnect()

    log.INFO("Initializing completed.")

def execute():
    executor = Generator()
    executor.generate()



    # dropDatabase(DbConfigs().dbname, DbConfigs())
    # createDatabase(DbConfigs().dbname, DbConfigs())


def finalize():
    fs = TxtFileService("files/sql/reportselect.sql", "r+")

    database = MySqlService(True)
    database.insertFromFile("files/buffer.txt")
    database.commit()
    cleanFile("files/buffer.txt")

    Reporter().selectresult = (selectValues(database, " ".join(fs.read())))
    database.disconnect()
    Reporter().finalize(GeneratorConfigs())

if __name__ == "__main__":
    initialize(sys.argv)
    execute()
    finalize()
