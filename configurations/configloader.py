import json
import xml
import sys
from loger import Loger
from services.jsonfileservice import *

log = Loger()
def loadConfigs():
    for name in getFilesFromDir("files"):
        if name.__contains__("configuration"):
            with open("files/{}".format(name), "r+") as file:
                if file.name.endswith(".json"):
                    return loadFromJSONFile()
                elif file.name.endswith(".xml"):
                    return loadFromXmlFile()
                else:
                    log.ERROR("There is no configuration file. Please add it or app wont start.")
                    sys.exit(1)


def loadFromXmlFile():
    log.INFO("Loading configs from configuration.xml.")

def loadFromJSONFile():
    log.INFO("Loading configs from configuration.json.")
    try:
        #jsonfile = JsonFileService("files/configuration.json", "r+")
        with open("files/configuration.json", "r+") as config:
            names = json.load(config)
            return names
    except IOError as err:
        log.INFO("Can't load configurations from file. {}".format(err.message))
        sys.exit(1)


