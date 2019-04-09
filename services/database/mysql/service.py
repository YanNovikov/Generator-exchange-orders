from __future__ import unicode_literals
from services.database.mysql.connection import *
from mysql.connector import errorcode
from configurations.dbconfigs import *
from utils.timeit import *
from utils.InsertHeaderMaker import *

class MySqlService:
    def __init__(self, nowopen=False):
        self.__prop = DbConfigs()
        self.conn = MySqlConnection(self.__prop.host, self.__prop.user, self.__prop.password, self.__prop.dbname)
        self.cursor = None
        if nowopen is True:
            self.connect()

    def connect(self):
        try:
            self.conn.connect()
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                log.WARNING("Database does not exist.")
            elif err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                log.ERROR("User name or password is incorrect.")
            else:
                log.ERROR(str(err))
    @timeit
    def insertFromFile(self, datafilename, commiteverytime=False):
        if self.conn.isconnected:
            with open(datafilename, "r+") as file:
                try:
                    for line in file.readlines():
                        insert = line
                        if line.__contains__("INSERT"):
                            self.ExecuteStatement(insert)
                            if commiteverytime:
                                self.commit()
                    log.INFO("All rows from file have bean inserted into a table - Success.")
                except IOError as err:
                    log.ERROR(str(err))
                    log.ERROR("Order is not added to Table.\n")

    @timeit
    def insertConsumedObjects(self, objects, commitnow=True):
        if self.conn.isconnected:
            try:
                for order in objects:
                    hat = InsertHeaderMaker(self.__prop.tablename, order)
                    values = " ("
                    for item in order.__dict__.items():
                        if item[0] == "primaryid" or item[0] == "initprice" or item[0] == "fillprice" or item[0] == "initvolume" or item[0] == "fillvolume":
                            values += "{},".format(item[1])
                        else:
                            values += "'{}',".format(item[1])
                    values = values[:-1]
                    self.ExecuteStatement("{}{})".format(hat.getHat(), values))
                if commitnow:
                    self.commit()
                log.DEBUG("Messages have bean inserted into a table - Success.")
            except IOError as err:
                log.ERROR(str(err))
                log.ERROR("Order is not added to Table.\n")

    def ExecuteStatement(self, statement, values=None):
        if self.conn.isconnected:
            self.cursor = self.conn.cursor()
            if values:
                return self.cursor.execute(statement, values)
            else:
                return self.cursor.execute(statement)
        else:
            return False

    def selectValues(self):
        if self.ExecuteStatement(self.__prop.testselect) is not False:
            result = self.cursor.fetchall()
            if result:
                log.DEBUG("Select results are: ")
                for x in result:
                    log.DEBUG(str(x))
            else:
                log.DEBUG("No rows found.")

    def cleanTable(self):
        try:
            if self.ExecuteStatement("DELETE FROM {}".format(self.__prop.tablename)) is not False:
                log.INFO("All records from table '{}' have been deleted.".format(self.__prop.tablename))
        except Exception as err:
            log.ERROR(err)

    def commit(self):
        try:
            if self.conn.commit() is not False:
                log.INFO("Changes are successfully commited.")
        except mysql.connector.Error as err:
            log.ERROR("Changes are not commited. {}".format(str(err)))

