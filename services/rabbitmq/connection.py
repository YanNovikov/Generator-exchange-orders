import pika
from configurations.messageconfigs import *
from loger import *
log = Loger()


class RMQConnection:
    def __init__(self):
        self.params = pika.connection.Parameters
        self.connection = None
        self.channel = None
        self.isconnected = False

    def open(self, user=pika.connection.Parameters.DEFAULT_USERNAME,
             password=pika.connection.Parameters.DEFAULT_PASSWORD,
             host=pika.connection.Parameters.DEFAULT_PORT,
             port=pika.connection.Parameters.DEFAULT_PORT,
             virtual_host=pika.connection.Parameters.DEFAULT_VIRTUAL_HOST):
        if not self.isconnected:
            try:
                credentials = pika.PlainCredentials(username=user, password=password)
                params = pika.ConnectionParameters(host=host, port=port, virtual_host=virtual_host, credentials=credentials)

                self.connection = pika.BlockingConnection(params)
                self.channel = self.connection.channel()
                log.INFO("Successfully connected to Rmq server.")
                self.isconnected = True
            except pika.exceptions.AMQPConnectionError as err:
                log.ERROR("Occured while connection to RMQ. {}".format(str(err)))
                return False
        else:
            log.INFO("Already connected to Rmq.")
        return True

    def close(self):
        try:
            if self.isconnected:
                self.connection.close()
                log.INFO("Connection to Rmq server closed successfully")
                self.isconnected = False
        except pika.exceptions.AMQPError as err:
            log.ERROR("While closing connection to Rmq. {}".format(str(err)))

    def publish(self, exchange_name, routing_key, body, properties=None, mandatory=False):
        try:
            self.channel.basic_publish(exchange=exchange_name, routing_key=routing_key,
                                       body=body, properties=properties,
                                       mandatory=mandatory)
            log.DEBUG("Published to {}:{} message = {}".format(exchange_name, routing_key, body))
        except pika.exceptions.AMQPError as err:
            log.ERROR("Can not publish to Rmq server. {}".format(str(err)))

    def declare_exchange(self, exchange_name, exchange_type, passive=False, durable=True, auto_delete=False):
        try:
            self.channel.exchange_declare(exchange=exchange_name,
                                                 exchange_type=exchange_type,
                                                 passive=passive,
                                                 durable=durable,
                                                 auto_delete=auto_delete)
            log.DEBUG("Exchange is created - Success.")
        except pika.exceptions.AMQPError as err:
            log.ERROR("Can not create exchange. {}".format(str(err)))

    def declare_queue(self, queue_name):
        try:
            self.channel.queue_declare(queue=queue_name)
            log.DEBUG("Queue is declared - Success.")
        except pika.exceptions.AMQPError as err:
            log.ERROR("Can not create queue. {}".format(str(err)))

    def delete_queue(self, queue_name, if_unused=False, if_empty=False):
        try:
            return self.channel.queue_delete(queue_name, if_unused=if_unused, if_empty=if_empty)
        except pika.exceptions.AMQPError as err:
            log.ERROR("Can not delete queue. {}".format(str(err)))

    def delete_exchange(self, exchange_name=None, if_unused=False):
        try:
            return self.channel.exchange_delete(exchange=exchange_name, if_unused=if_unused)
        except pika.exceptions.AMQPError as err:
            log.ERROR("Can not delete exchange. {}".format(str(err)))

    def bind_queue(self, queue_name, exchange_name, routing_key=None):
        try:
            return self.channel.queue_bind(queue_name, exchange_name, routing_key=routing_key)
        except pika.exceptions.AMQPError as err:
            log.ERROR("Can not bind queue. {}".format(str(err)))

    def unbind_queue(self, queue_name, exchange_name, routing_key=None):
        try:
            return self.channel.queue_unbind(queue_name, exchange_name, routing_key=routing_key)
        except pika.exceptions.AMQPError as err:
            log.ERROR("Can not unbind queue. {}".format(str(err)))

    def bind_exchange(self, destination, source, routing_key=''):
        try:
            return self.channel.exchange_bind(destination=destination, source=source,
                                              routing_key=routing_key)
        except pika.exceptions.AMQPError as err:
            log.ERROR("Can not bind exchange. {}".format(str(err)))

    def unbind_exchange(self, destination, source, routing_key=''):
        try:
            return self.channel.exchange_unbind(destination=destination, source=source,
                                                routing_key=routing_key)
        except pika.exceptions.AMQPError as err:
            log.ERROR("Can not unbind exchange. {}".format(str(err)))

    def purge_queue(self, queue_name):
        try:
            return self.channel.queue_purge(queue_name)
        except pika.exceptions.AMQPError as err:
            log.ERROR("Can not purge queue. {}".format(str(err)))