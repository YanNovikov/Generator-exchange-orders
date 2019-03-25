import json
import xml
import sys
from loger import Loger
from services.fileservice import *

log = Loger()
def loadConfigs():
    fileservice = FileService()
    for name in fileservice.getFilesFromDir("files"):
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
    with open("files/configuration.json", "r+") as config:
        names = json.load(config)
    return names

