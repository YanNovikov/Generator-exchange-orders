import pika
from configurations.messageconfigs import *

class RMQConnection:
    def __init__(self):
        self.prop = MessageConfigs()
        self.log = Loger()
        self.connection = None
        self.channel = None

    def connect(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
        channel = connection.channel()
        channel.queue_declare(queue=self.prop.queuename)
        return channel

    def sendMessages(self):
        pass

    def disconnect(self):
        pass