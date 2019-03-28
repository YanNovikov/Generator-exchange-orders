from configurations.messageconfigs import *
from models.OrdersObject import *
from models.Generator import *
from services.dbservice import *

def initialize():
    g = GeneratorConfigs()
    db = DbConfigs()
    msg = MessageConfigs()
    log = Loger()


def execute():
    generator = Generator()
    generator.generate()

    dbservice = DbService()
    dbservice.dropDatabase()
    #dbservice.connectDb()
    #dbservice.insertFromFile()


if __name__ == "__main__":
    initialize()
    execute()
