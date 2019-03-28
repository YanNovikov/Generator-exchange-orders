import mysql.connector
from mysql.connector import errorcode
from loger import *
log = Loger()


class DbConnection:
    def __init__(self, host, user, password, dbname):
        self.__conn = None
        self.host = host
        self.user = user
        self.password = password
        self.dbname = dbname
        self.isconnected = False


    def connect(self):
        self.__conn = self.getSecureConnection()
        if self.__conn:
            self.isconnected = True
            return True

    def reconect(self):
        self.disconnect()
        self.connect()

    def disconnect(self):
        if self.isconnected:
            self.__conn.close()
        self.isconnected = False

    def getUserConnection(self):
        return mysql.connector.connect(host=self.host, user=self.user, password=self.password)

    def getDbConnection(self):
        return mysql.connector.connect(host=self.host, user=self.user, password=self.password, database=self.dbname)

    def checkDbConnection(self):
        try:
            cnx = self.getDbConnection()
            cnx.close()
            log.INFO("Connection to host='{}', user='{}', database='{}' is Success.".format(self.host, self.user, self.dbname))
            return True
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                log.WARNING("Database does not exist")
                raise EnvironmentError
            else:
                log.ERROR(str(err))

    def checkMySqlConnection(self):
        try:
            cnx = self.getUserConnection()
            cnx.close()
            log.INFO("Connection to host='{}', user='{}' is Success.".format(self.host, self.user))
            return True
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                log.ERROR("User name or password is incorrect.")
            else:
                log.ERROR(err)

    def getSecureConnection(self):
        if self.checkMySqlConnection():
            if self.checkDbConnection():
                cnx = self.getDbConnection()
                log.INFO("Connection to Db is set.")
                return cnx
            else:
                cnx = self.getUserConnection()
                log.INFO("Connection to server is set.")
                return cnx
        log.INFO("Connection is not set.")
        return None

    def cursor(self):
        if self.isconnected:
            return self.__conn.cursor()
        else:

