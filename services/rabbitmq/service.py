from services.rabbitmq.connection import *
from configurations.messageconfigs import *
from utils.timeit import *


class RMQService:
    def __init__(self):
        self.conn = RMQConnection()
        self.properties = MessageConfigs()

    def startSending(self):
        log.INFO("Start sending records to RabbitMQ.")



        try:
            self.__open_connection(host=self.properties.rmq_host, port=self.properties.rmq_port,
                                 virtual_host=self.properties.rmq_vhost, user=self.properties.rmq_user,
                                 password=self.properties.rmq_password)

            self.__delete_exchange(exchange_name=self.properties.rmq_exchange_name)
            self.__declare_exchange(exchange_name=self.properties.rmq_exchange_name,
                                 exchange_type=self.properties.rmq_exchange_type)
        except ValueError as err:
            log.ERROR("Occured while preparing exchange to send messages to Rmq. {}".format(str(err)))
            return False

        try:
            self.__declare_queue(queue_name="Red")
            self.__declare_queue(queue_name="Green")
            self.__declare_queue(queue_name="Blue")

            self.__queue_bind("Red", self.properties.rmq_exchange_name, self.properties.rmq_red_routing_key)
            self.__queue_bind("Green", self.properties.rmq_exchange_name, self.properties.rmq_green_routing_key)
            self.__queue_bind("Blue", self.properties.rmq_exchange_name, self.properties.rmq_blue_routing_key)

            self.__queue_purge("Red")
            self.__queue_purge("Green")
            self.__queue_purge("Blue")
        except Exception as err:
            log.ERROR("Occured while preparing queues to send messages to Rmq. {}".format(str(err)))
            return False
        return True

    def stopSending(self):
        log.INFO("Sending records to RabbitMQ stopped.")
        self.__close_connnection()

    @timeit
    def sendObjects(self, objects, key):
        if key == "Red":
            key = self.properties.rmq_red_routing_key
        elif key == "Green":
            key = self.properties.rmq_green_routing_key
        elif key == "Blue":
            key = self.properties.rmq_blue_routing_key

        for one in objects:
            self.__publish(self.properties.rmq_exchange_name, key, str(one))
        pass


    def __open_connection(self, user=pika.connection.Parameters.DEFAULT_USERNAME,
                    password=pika.connection.Parameters.DEFAULT_PASSWORD,
                    host=pika.connection.Parameters.DEFAULT_HOST,
                    port=pika.connection.Parameters.DEFAULT_PORT, *args, **kwargs):
        if 'vhost' in kwargs:
            vhost = kwargs['vhost']
        else:
            vhost = pika.connection.Parameters.DEFAULT_VIRTUAL_HOST

        log.DEBUG("Trying to connect to Rmq")
        self.conn.open(host=host, port=port, user=user, password=password, virtual_host=vhost)

        return self.conn.isconnected

    def __close_connnection(self):
        log.DEBUG("Closing RMQ connection")
        self.conn.close()

    def __publish(self, exchange_name, routing_key, body, properties=None, mandatory=False):
        self.conn.publish(exchange_name, routing_key, body, properties=properties, mandatory=mandatory)

    def __declare_exchange(self, exchange_name, exchange_type, passive=False, durable=True, auto_delete=False):
        log.DEBUG("Trying to create exchange '{}' type '{}'".format(exchange_name, exchange_type))
        return self.conn.declare_exchange(exchange_name, exchange_type, passive=passive, durable=durable, auto_delete=auto_delete)

    def __declare_queue(self, queue_name):
        log.DEBUG("Trying to declare queue '{}'".format(queue_name))
        return self.conn.declare_queue(queue_name=queue_name)

    def __delete_queue(self, queue_name, if_unused=False, if_empty=False):
        log.DEBUG("Deleting queue '{}'".format(queue_name))
        return self.conn.delete_queue(queue_name, if_unused=if_unused, if_empty=if_empty)

    def __delete_exchange(self, exchange_name=None, if_unused=False):

        log.DEBUG("Deleting exchange '{}'".format(exchange_name))
        return self.conn.delete_exchange(exchange_name=exchange_name, if_unused=if_unused)

    def __queue_bind(self, queue_name, exchange_name, routing_key=None):

        log.DEBUG("Binding queue '{}' to exchange '{}' with routing key  '{}'".format(queue_name, exchange_name,
                                                                                             routing_key))
        return self.conn.bind_queue(queue_name=queue_name, exchange_name=exchange_name, routing_key=routing_key)

    def __queue_unbind(self, queue_name, exchange_name, routing_key=None):
        log.DEBUG("Unbinding queue '{}' from exchange '{}' with routing key  '{}'".format(queue_name, exchange_name,
                                                                                       routing_key))
        return self.conn.unbind_queue(queue_name=queue_name, exchange_name=exchange_name, routing_key=routing_key)

    def __queue_purge(self, queue_name):
        log.DEBUG('Purging queue {}'.format(queue_name))
        return self.conn.purge_queue(queue_name)

    def __exchange_bind(self, destination, source, routing_key=''):
        log.DEBUG("Binding exchange: destination '{}', source '{}', routing_key '{}'".format(destination, source, routing_key))
        return self.conn.bind_exchange(destination=destination, source=source, routing_key=routing_key)

    def __exchange_unbind(self, destination, source, routing_key=''):
        log.DEBUG("Unbinding exchange: destination '{}', source '{}', routing_key '{}'".format(destination, source, routing_key))
        return self.conn.unbind_exchange(destination=destination, source=source, routing_key=routing_key)
