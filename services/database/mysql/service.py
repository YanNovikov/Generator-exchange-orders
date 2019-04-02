from services.database.mysql.connection import *
from configurations.dbconfigs import *
from utils.timeit import *

class MySqlService:
    def __init__(self, nowopen=False):
        self.__prop = DbConfigs()
        self.conn = MySqlConnection(self.__prop.host, self.__prop.user, self.__prop.password, self.__prop.dbname, nowopen)
        self.cursor = None

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
        with open(datafilename, "r+") as file:
            try:
                for line in file.readlines():
                    insert = line
                    if line.__contains__("INSERT"):
                        self.ExecuteStatement(insert)
                        if commiteverytime:
                            self.commit()
                log.INFO("All rows from file have bean inserted into a table - Success.")
            except IOError, err:
                log.ERROR(str(err))
                log.ERROR("Order is not added to Table.\n")

    def ExecuteStatement(self, statement, values=None):
        self.cursor = self.conn.cursor()
        if values:
            return self.cursor.execute(statement, values)
        else:
            return self.cursor.execute(statement)

    def selectValues(self):
        self.ExecuteStatement(self.__prop.testselect)
        result = self.cursor.fetchall()
        if result:
            log.DEBUG("Select results are: ")
            for x in result:
                log.DEBUG(str(x))
        else:
            log.DEBUG("No rows found.")

    def cleanTable(self):
        try:
            self.ExecuteStatement("DELETE FROM {}".format(self.__prop.tablename))
            log.INFO("All records from table '{}' have been deleted.".format(self.__prop.tablename))
        except Exception as err:
            log.ERROR(err)

    def commit(self):
        try:
            self.conn.commit()
            log.INFO("Changes are successfully commited.")
        except mysql.connector.Error as err:
            log.ERROR(str(err))

