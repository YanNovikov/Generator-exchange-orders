from __future__ import unicode_literals
from utils.singleton import singleton
from configurations.configuration import *

@singleton
class MessageConfigs:
    def __init__(self):
        pass

    def initializeconfigs(self):
        try:
            configs = Configuration().configs
            self.rmq_queue_original = configs["rmq_queue_original"]
            self.rmq_queue_protobuff = configs["rmq_queue_protobuff"]
            self.rmq_host = configs["rmq_host"]
            self.rmq_port = configs["rmq_port"]
            self.rmq_vhost = configs["rmq_vhost"]
            self.rmq_user = configs["rmq_user"]
            self.rmq_password = configs["rmq_password"]
            self.rmq_exchange_name = configs["rmq_exchange_name"]
            self.rmq_exchange_type = configs["rmq_exchange_type"]
            self.rmq_red_routing_key = configs["rmq_red_routing_key"]
            self.rmq_green_routing_key = configs["rmq_green_routing_key"]
            self.rmq_blue_routing_key = configs["rmq_blue_routing_key"]
            log.INFO("Configurations for messaging loaded.")
        except KeyError as err:
            log.ERROR("Configuration does not fits arguments. {}".format(str(err)))
            sys.exit(1)
