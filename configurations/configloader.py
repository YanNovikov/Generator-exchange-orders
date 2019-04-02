import sys
from services.file.jsonfileservice import *

log = Loger()


def loadConfigs(filename):
    try:
        with open("files/{}".format(filename), "r+") as file:
            if file.name.endswith(".json"):
                return loadFromJSONFile(file)
            elif file.name.endswith(".xml"):
                return loadFromXmlFile(file)
    except IOError as err:
        raise err

def loadDefaults():
    try:
        return loadConfigs("defaults.json")
    except IOError as err:
        log.ERROR("Error occured while opening defaults configuration file. Message: {}.".format(str(err)))
        sys.exit(1)


def loadFromXmlFile(file):
    log.INFO("Loading configs from {}.".format(file.name))


def loadFromJSONFile(file):
    log.INFO("Loading configs from {}.".format(file.name))
    fileservice = JsonFileService(file.name, "r+")
    names = fileservice.read()
    fileservice.close()
    return names


