import mysql.connector
from mysql.connector import errorcode
from services.database.dbconnection import *
from loger import *
log = Loger()

# Please catch Exceptions and Errors outside


class MySqlConnection(DbConnection):
    def __init__(self, host, user, password, dbname, nowopen=False):
        DbConnection.__init__(self, host, user, password, dbname)
        self.__curs = None
        if nowopen is True:
            self.connect()

    def cursor(self, buffered=None, raw=None, prepared=None, cursor_class=None, dictionary=None, named_tuple=None):
        if self.isconnected:
            if self.__curs is None:
                log.DEBUG("Setting cursor for '{}'.".format(self.dbname))
                self.__curs = self.__conn.cursor(buffered, raw, prepared, cursor_class, dictionary, named_tuple)
                return self.__curs
            else:
                return self.__curs
        else:
            try:
                print 1
                self.connect()
            except mysql.connector.Error as err:
                log.ERROR("Can not get cursor because connection is unset.")
                raise err
            self.cursor(buffered, raw, prepared, cursor_class, dictionary, named_tuple)

    def connect(self):
        if self.isconnected is True:
            log.INFO("Connection to database '{}' is Success.".format(self.dbname))
        else:
            log.DEBUG("Trying to open new connection.")
            try:
                self.__conn = self.__createConnection()
            except mysql.connector.Error as err:
                log.ERROR("Unable to connect to {}".format(self.getConnectionString(dbconnect=True)))
                raise err
            self.isconnected = True
            self.connect()

    def commit(self):
        self.__conn.commit()

    def reconnect(self):
        self.disconnect()
        self.connect()

    def disconnect(self):
        if self.isconnected is True:
            self.__conn.close()
            self.isconnected = False
            log.INFO("Disconnected - Success.")
            return True
        log.INFO("Already disconnected.")

    def __openConnection(self):
        return mysql.connector.connect(host=self.host, user=self.user, password=self.password, database=self.dbname)



    def __createConnection(self):
        try:
            cnx = self.__openConnection()
            log.DEBUG("Connection to {} is Success.".format(self.getConnectionString(dbconnect=True)))
            return cnx
        except mysql.connector.Error as err:
            raise err
