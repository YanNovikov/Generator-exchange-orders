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
        self.falsealarm = False
        self.established = False
        if nowopen is True:
            self.connect()

    def connect(self, trys=0):
        if trys < 3:
            # if self.falsealarm is True:
            #     log.DEBUG("Trying reconnect in 1 s")
            #     threading.Timer(1, self.connect, [trys + 1]).start()
            #     return
            try:
                self.conn.connect()
                self.cursor = self.conn.cursor()
                self.established = True
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_BAD_DB_ERROR:
                    log.WARNING("Database does not exist.")
                elif err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    log.ERROR("User name or password is incorrect.")
                else:
                    log.ERROR(str(err))
                    log.DEBUG("Trying reconnect in 1.5 s")
                    threading.Timer(2, self.connect, [trys + 1])
        else:
            log.ERROR("Connection cannot be established. Quiting...")
            self.established = False
            sys.exit(0)

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
                    Reporter().insertrowscount += 1
                if commitnow:
                    self.commit()
                log.DEBUG("Messages have bean inserted into a table - Success.")
            except IOError as err:
                log.ERROR(str(err))
        else:
            self.connect()


    def ExecuteStatement(self, statement, values=None):
        if self.conn.isconnected and self.established:
            self.cursor = self.conn.cursor()
            if values:
                return self.cursor.execute(statement, values)
            else:
                return self.cursor.execute(statement)
        else:
            return False

    def selectValues(self):
        selectwriter = TxtFileService(DbConfigs().selectresultfile, "a+")
        selectwriter.open()
        cleanFile(selectwriter.filename)
        if self.ExecuteStatement(self.__prop.testselect) is not False:
            result = self.cursor.fetchall()
            if result:
                log.DEBUG("Select results added to file '{}'.".format(selectwriter.filename))
                for x in result:
                    selectwriter.writeline(str(x))
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
                log.DEBUG("Changes are successfully commited.")
        except mysql.connector.Error as err:
            log.ERROR("Changes are not commited. {}".format(str(err)))

