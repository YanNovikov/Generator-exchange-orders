from configurations.messageconfigs import *
from models.OrdersObject import *
from models.Generator import *


def initialize():
    g = GeneratorConfigs()
    db = DbConfigs()
    msg = MessageConfigs()
    log = Loger()


def execute():
    generator = Generator()
    generator.generate()


if __name__ == "__main__":
    initialize()
    execute()
