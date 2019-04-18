from __future__ import unicode_literals
from services.database.mysql.connection import *
from mysql.connector import errorcode
from configurations.dbconfigs import *
from utils.timeit import *
from utils.insertheadermaker import *

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
            return True
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                log.WARNING("Database does not exist.")
            elif err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                log.ERROR("User name or password is incorrect.")
            else:
                log.ERROR("Connection failed. {}".format(str(err)))
            return False

    def reconnect(self, attempts=0):
        if attempts < 2:
            log.DEBUG("Trying reconnect in 1 s...")
            if self.connect() is False:
                time.sleep(1)
                self.reconnect(attempts=attempts+1)
            else:
                return True
        return False

    @timeit
    def insertFromFile(self, datafilename, commiteverytime=False):
        if os.stat(datafilename).st_size != 0:
            self.connect()
            file = TxtFileService(datafilename, "r+")
            try:
                for line in file.read():
                    if self.ExecuteStatement(line):
                        Reporter().insertrowscount += 1
                        if commiteverytime:
                            self.commit()
                log.DEBUG("All rows from file have bean inserted into a table - Success.")
                cleanFile(datafilename)
                self.commit()
            except IOError as err:
                log.ERROR(str(err))
                log.ERROR("Order is not added to Table.\n")

    @timeit
    def insertConsumedObjects(self, objects, commitnow=True):
        try:
            # time.sleep(1)
            inserted = 0
            for order in objects:
                hat = InsertHeaderMaker(self.__prop.tablename, order)
                values = " ("
                for item in order.__dict__.items():
                    if item[0] == "primaryid" or item[0] == "initprice" or item[0] == "fillprice" or item[0] == "initvolume" or item[0] == "fillvolume":
                        values += "{},".format(item[1])
                    else:
                        values += "'{}',".format(item[1])
                values = values[:-1]
                if self.ExecuteStatement("{}{})".format(hat.getHat(), values)) is not False:
                    inserted += 1
                else:
                    with open("files/buffer.txt", "a+") as file:
                        file.write(("{}{})\n".format(hat.getHat(), values)))

            if inserted < len(objects):
                if not self.reconnect():
                    log.DEBUG("Reconnect failed...")
                else:
                    log.DEBUG("Successfully reconnected...")
            if inserted > 1:
                if commitnow:
                    log.DEBUG("Inserted {} rows.".format(inserted))
                    self.commit()
                    Reporter().insertrowscount += inserted
            log.TRACE("{} Messages have bean inserted into a table - Success.".format(inserted))
        except IOError as err:
            log.ERROR(str(err))

    def ExecuteStatement(self, statement, values=None):
        try:
            if self.conn.isconnected:
                self.cursor = self.conn.cursor()
                if values:
                    return self.cursor.execute(statement, values)
                else:
                    return self.cursor.execute(statement)
            else:
                return False
        except mysql.connector.Error as err:
            log.ERROR("In execute {}".format(str(err)))
            self.conn.isconnected = False
            return False


    def selectValues(self):
        selectwriter = TxtFileService(DbConfigs().selectresultfile, "a+")
        cleanFile(selectwriter.filename)
        if self.ExecuteStatement(self.__prop.testselect) is not False:
            result = self.cursor.fetchall()
            if result:
                log.INFO("Select results added to file '{}'.".format(selectwriter.filename))
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

    def disconnect(self):
        self.conn.disconnect()

    def commit(self):
        try:
            if self.conn.commit() is not False:
                log.DEBUG("Changes are successfully commited.")
                return True
        except mysql.connector.Error as err:
            log.ERROR("Changes are not commited. {}".format(str(err)))
            return False



