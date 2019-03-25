from configurations.dbconfigs import *
from configurations.messageconfigs import *
from models.OrdersObject import *

g = GeneratorConfigs()
g.initializeconfigs()
db = DbConfigs()
db.initializeconfigs()
msg = MessageConfigs()
msg.initializeconfigs()

print OrdersObject(1, "Red").__dict__
