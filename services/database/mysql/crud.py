from __future__ import unicode_literals

import sys

from loger import *
import threading
import mysql.connector
from services.file.txtfileservice import *
log = Logger()


def createTable(conn, dbname, createtablefile, tablename):
    if conn.conn.isconnected:
        log.TRACE("Trying to create table '{}'.".format(tablename))
        if not showTable(conn, tablename):
            try:
                with open(createtablefile, "r") as file:
                    cmd = file.read()
                    conn.ExecuteStatement("USE {}".format(dbname))
                    conn.ExecuteStatement(cmd)
                    conn.commit()
                    log.INFO("Table '{}' has been created.".format(tablename))
            except mysql.connector.Error as err:
                log.ERROR("Occured while creating table. {}".format(str(err)))
        else:
            log.INFO("Table '{}' exists.".format(tablename))
    else:
        log.FATAL("Initializing database is not passed...")
        sys.exit(0)

def dropTable(conn, tablename):
    if showTable(conn, tablename):
        try:
            conn.ExecuteStatement("DROP TABLE {}".format(tablename))
            log.INFO("Table '{}' is dropped.".format(tablename))
        except mysql.connector.Error as err:
            log.ERROR("While dropping table. {}".format(str(err)))
            raise err

def cleanTable(conn, tablename):
    try:
        if showTable(conn, tablename):
            removeRecords(conn, tablename)
    except mysql.connector.Error as err:
        log.ERROR("Table does not exist. {}".format(str(err)))
        raise err

def showTable(conn, tablename):
    if conn.conn.isconnected:
        conn.ExecuteStatement("SHOW TABLES")
        for x in conn.cursor:
            if str(x).__contains__(tablename):
                return True
    else:
        return False

def selectValues(conn, query):
    if conn.ExecuteStatement(query) is not False:
        result = conn.cursor.fetchall()
        if result:
            return result
        else:
            log.DEBUG("No rows found.")

def createDatabase(dbname, params):
    conn = mysql.connector.connect(host=params.host, user=params.user, password=params.password)
    log.DEBUG("Creating database {}".format(dbname))
    ExecuteStatement(conn, "CREATE DATABASE {}".format(dbname))

def dropDatabase(dbname, params):
    conn = mysql.connector.connect(host=params.host, user=params.user, password=params.password)
    log.DEBUG("Dropping database {}".format(dbname))
    ExecuteStatement(conn, "DROP SCHEMA {}".format(dbname))

def ExecuteStatement(conn, statement, values=None):
    cursor = conn.cursor()
    if values:
        cursor.execute(statement, values)
    else:
        cursor.execute(statement)
    return cursor


def commit(conn, trys=0):
    if trys < 3:
        try:
            conn.commit()
            return True
        except mysql.connector.Error as err:
            log.ERROR("Message: {}".format(str(err)))
            threading.Timer(1000, conn.commit, [conn, trys+1])
    else:
        log.CRITICAL("Can not commit changes.")
        return False


def removeRecords(conn, tablename):
    try:
        ExecuteStatement(conn, "DELETE FROM {}".format(tablename))
        log.INFO("All records have been deleted.")
    except Exception as err:
        log.ERROR(err)


