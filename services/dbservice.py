from dbconnection import *
from configurations.dbconfigs import *
from configurations.generatorconfigs import GeneratorConfigs
class DbService:
    def __init__(self):
        self.prop = DbConfigs()
        self.conn = DbConnection(self.prop.host, self.prop.user, self.prop.password, self.prop.dbname)
        self.connectDb()

    def connectDb(self):
        try:
            self.conn.connect()
        except EnvironmentError as err:
            self.createDatabase()

    def createDatabase(self):
        try:
            with open(self.prop.createdbfile, "r") as createfile:
                cmd = createfile.read()
                cnx = self.conn.getUserConnection()
                cursor = cnx.cursor()
                cursor.execute(cmd)
                cnx.close()
            log.INFO("Database created - Success.".format(self.prop.user, self.prop.dbname))
            self.conn.disconnect()
            self.checkTable()
        except mysql.connector.Error as err:
            log.ERROR("Error while creating database. Message: {}.".format(err.message))

    def createTable(self):
        try:
            with open(self.prop.createblefile, "r") as file:
                cmd = file.read()
                cursor = self.conn.cursor()
                cursor.execute(cmd)
                log.INFO("Table has been created.")
                self.checkTable()
        except mysql.connector.Error as err:
            log.ERROR(str(err))

    def checkTable(self):
        try:
            if self.showTable():
                self.removeRecords()
            self.selectValues()
            self.ExecuteStatement(self.prop.testinsert, self.prop.testvalues)
            log.DEBUG("Insert passed.")
            self.selectValues()
            self.ExecuteStatement(self.prop.testdelete)
            log.DEBUG("Delete passed.")
            self.selectValues()
            log.INFO("Test execute passed.")
        except mysql.connector.Error as err:
            log.WARNING("Table does not exist. {}".format(str(err)))
            self.createTable()

    def selectValues(self):
        cursor = self.conn.cursor()
        cursor.execute(self.prop.testselect)
        result = cursor.fetchall()
        if result:
            log.INFO("Select results are: ")
            for x in result:
                log.INFO(str(x))
        else:
            log.INFO("No rows found.")

    def showTable(self):
        cursor = self.conn.cursor()
        cursor.execute("SHOW TABLES")
        for x in cursor:
            if str(x).__contains__(self.prop.tablename):
                log.DEBUG("Table '{}' is found.".format(self.prop.tablename))
                return True

    def dropDatabase(self):
        cnx = self.conn.getUserConnection()
        cursor = cnx.cursor()
        log.DEBUG("Dropping database {}".format(self.prop.dbname))
        cursor.execute("DROP DATABASE {}".format(self.prop.dbname))
        cnx.close()

    def insertFromFile(self):
        g = GeneratorConfigs()
        with open(g.datafilename, "r+") as file:
            try:
                for line in file.readlines():
                    insert = line
                    if line.__contains__("INSERT"):
                        #print insert
                        line = line.split("VALUES")
                        print line
                        values = self.getParams(line[1])
                        insert = "{}VALUES {}".format(line[0], self.replaceValues(values))
                        print "{} {}".format(insert,values)
                        self.ExecuteStatement(insert, values)
            except IOError, err:
                log.ERROR(str(err))
                log.ERROR("Order is not added to Table.\n")

    def replaceValues(self, val):
        row = "("
        for i in range(0, len(val)-1):
            row += "%s,"
        return row + "%s)"

    def getParams(self, str):
        params = str.split(",")
        res = []
        for one in params:
            if one.__contains__("'"):
                res.append(one.split("'")[1])
            else:
                res.append(float(one))
        return res

    def ExecuteStatement(self, statement, values=None):
        cursor = self.conn.cursor()
        if values:
            cursor.execute(statement, values)
        else:
            cursor.execute(statement)

    def commit(self):
        pass

    def removeRecords(self):
        try:
            self.ExecuteStatement("DELETE FROM {}".format(self.prop.tablename))
            log.INFO("All records have been deleted.")
        except Exception as err:
            log.ERROR(err)




