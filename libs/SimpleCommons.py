################################################################################
import base64
import inspect
import socket
import json
import os
import sys
from collections import OrderedDict
import IPython
import atexit
from . import SimpleConfig as sc
import re

################################################################################
# GLOBAL PARAMS
################################################################################

################################################################################
ROOT_FOLDER = os.path.dirname(os.path.realpath(__file__)) + "/.."
CONFIG = sc.Config(ROOT_FOLDER + "/resources/config.ini")
################################################################################
DEBUG = CONFIG.getValue("DEBUG", True)
SCRIPTS_DATA_FOLDER = CONFIG.getValue("SCRIPTS_DATA_FOLDER", ROOT_FOLDER + "/data")
RESOURCES_FOLDER = CONFIG.getValue("RESOURCES_FOLDER", ROOT_FOLDER + "/resources")
SCRIPTS_OUTPUT_FOLDER = CONFIG.getValue("SCRIPTS_PLOTS_FOLDER", ROOT_FOLDER + "/output")
################################################################################
TIMEZONE_NY = "America/New_York"
TIMEZONE_PARIS = "Europe/Paris"
TIMEZONE_US_EASTERN = "US/Eastern"
TIMEZONE_GMT = "GMT"
TIMEZONE_UTC = "utc"
TIMEZONE_DEFAULT = TIMEZONE_PARIS
################################################################################
SIZE_BYTE = 1
SIZE_INT = 4
SIZE_FLOAT = 4
SIZE_LONG = 8
SIZE_DOUBLE = 8
FORMAT_INT = ">i"
FORMAT_FLOAT = ">f"

################################################################################
LINE_BREAK = "\n"


################################################################################
def setInteractiveMode(interactiveMode):
    global INTERACTIVE_MODE
    INTERACTIVE_MODE = interactiveMode
    sp.init(INTERACTIVE_MODE)


################################################################################
def startInteractiveSession(exitAfer=False):
    if INTERACTIVE_MODE:
        frame = inspect.currentframe()
        locals().update(frame.f_back.f_locals)
        globals().update(frame.f_back.f_globals)
        sp.show(block=False)
        IPython.embed(display_banner=None)
        del frame
        if exitAfer: sys.exit()


################################################################################
def isInteractive():
    try:
        sys.ps1
        return True
    except:
        return False


################################################################################
# INIT
################################################################################
INTERACTIVE_MODE = isInteractive()
from . import SimpleCollections as scl
from . import SimplePlot as sp
from . import SimpleLogger as sl
from . import SimplePlot as sp
from . import SimpleFile as sf

################################################################################
if INTERACTIVE_MODE: sl.printBegining()
if INTERACTIVE_MODE: atexit.register(sl.printEnd)
setInteractiveMode(INTERACTIVE_MODE)
sp.setupPlots()
