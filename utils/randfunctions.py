import math
from configurations.generatorconfigs import GeneratorConfigs
g = GeneratorConfigs()

def getSinExp(value):
    return math.exp(math.sin(value))

def getCosExp(value):
    return math.exp(math.cos(value))

def getToProviderStatus(id):
    if math.fmod(id, 2) == 0:
        return g.status[1]
    else:
        return None

def getResultStatus(id):
    return g.status[math.trunc(math.fmod(id, 3) + 2)]

def getNewStatus():
    return g.status[0]

def getRedStatus(stat):
    return [None, getToProviderStatus(stat), getResultStatus(stat)]

def getGreenStatus(stat):
    return [getNewStatus(), getToProviderStatus(2), getResultStatus(stat)]

def getBlueStatus(stat):
    return [getNewStatus(), getToProviderStatus(stat), None]