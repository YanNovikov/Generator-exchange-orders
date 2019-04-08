from __future__ import unicode_literals
from abc import abstractmethod


class DbConnection:
    def __init__(self, host, user, password, dbname):
        self.conn = None
        self.host = host
        self.user = user
        self.password = password
        self.dbname = dbname
        self.isconnected = False

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def reconnect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    def __openConnection(self):
        pass

    def getConnectionString(self, dbconnect = False):
        connectionstring = "host:{}, user='{}'".format(self.host, self.user)
        if dbconnect is True:
            connectionstring += ", dbname='{}'".format(self.dbname)
        return connectionstring
