################################################################################
import os

try: import ConfigParser as ConfigParser
except: import configparser as ConfigParser


################################################################################
class Config:
    ################################################################################
    def __init__(self, configFile):
        self.CONFIG = False
        self.__loadConfig(configFile)

    ################################################################################
    def __loadConfig(self, configFile):
        if os.path.isfile(configFile):
            self.CONFIG = ConfigParser.RawConfigParser()
            self.CONFIG.read(configFile)
            return self
        else:
            raise BaseException("Config file " + configFile + " does not exist !")

    ################################################################################
    def getValue(self, name, defaultValue=None, section="main"):
        typeValue = type(defaultValue)
        if self.CONFIG.has_option(section, name):
            if typeValue is bool:
                return self.CONFIG.getboolean(section, name)
            elif typeValue is float:
                return self.CONFIG.getfloat(section, name)
            elif typeValue is int:
                return self.CONFIG.getint(section, name)
            else:
                return self.CONFIG.get(section, name)
        else:
            return defaultValue
