from configurations.dbconfigs import *
from configurations.messageconfigs import *
from models.OrdersObject import *

g = GeneratorConfigs()
g.initializeconfigs()
db = DbConfigs()
db.initializeconfigs()
msg = MessageConfigs()
msg.initializeconfigs()

o = OrdersObject(1, "Green")
print o.__dict__
print o.getOrdersRow().inserts
