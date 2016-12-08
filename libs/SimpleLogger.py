################################################################################
import os
import sys
import requests
from . import SimpleTime as st
from . import SimpleString as ss
from . import SimpleCommons as sc
from . import SimpleFile as sf
from collections import OrderedDict
from tabulate import tabulate

try: from var_dump import var_dump
except: pass

################################################################################
COLOR_BLUE = '\033[94m'
COLOR_GREEN = '\033[92m'
COLOR_ORANGE = '\033[93m'
COLOR_RED = '\033[91m'
COLOR_NEUTRAL = '\033[0m'
COLOR_BOLD = '\033[1m'
COLOR_UNDERLINE = '\033[4m'

################################################################################
global occurrencesLog
occurrencesLog = {}
global scriptStart
scriptStart = st.now()


################################################################################
def d(object, exitDebug=True):
    var_dump(object)  # no python3?
    if exitDebug: exit()


################################################################################
def makeMessageFromArgsArray(args):
    cleanedArgs = []
    for arg in args: cleanedArgs.append(ss.dumps(arg).strip('"'))
    return ' / '.join(cleanedArgs)


################################################################################
def printSeparator():
    try: rows, columns = os.popen('stty size', 'r').read().split()
    except: columns = 30
    for i in range(0, int(columns)): sys.stdout.write("-")
    print


################################################################################
def info(*args):
    printLineColored("[NFO] - " + st.formatTimestamp(st.now(), "YYYY/MM/DD HH:mm:ss") + " - " + makeMessageFromArgsArray(args), COLOR_BLUE)


################################################################################
def warning(*args):
    printLineColored("[WRN] - " + st.formatTimestamp(st.now(), "YYYY/MM/DD HH:mm:ss") + " - " + makeMessageFromArgsArray(args), COLOR_ORANGE)


################################################################################
def success(*args):
    printLineColored("[OK!] - " + st.formatTimestamp(st.now(), "YYYY/MM/DD HH:mm:ss") + " - " + makeMessageFromArgsArray(args), COLOR_GREEN)


################################################################################
def failure(*args):
    printLineColored("[KO!] - " + st.formatTimestamp(st.now(), "YYYY/MM/DD HH:mm:ss") + " - " + makeMessageFromArgsArray(args), COLOR_RED)
    sys.exit(0)


################################################################################
def debug(*args):
    if sc.DEBUG: printLine("[DBG] - " + st.formatTimestamp(st.now(), "YYYY/MM/DD HH:mm:ss") + " - " + makeMessageFromArgsArray(args))


################################################################################
def printLine(string):
    print(string)


################################################################################
def printLineColored(string, color):
    printLine(color + string + COLOR_NEUTRAL)


################################################################################
def printTitle(title):
    # rows, columns = os.popen('stty size', 'r').read().split()
    # f = Figlet(font=sc.MISCS_TITLE_FONT, width=rows)
    printSeparator()
    # print(f.renderText(title))
    printLineColored(title, COLOR_BLUE)
    printSeparator()


################################################################################
def printBanner(bannerFile):
    printSeparator()
    [print(line.replace("\n", "")) for line in open(bannerFile).readlines()]


################################################################################
def printEnd():
    global scriptStart
    printSeparator()
    success("Finished in", str(st.now() - scriptStart) + " s")
    printSeparator()


################################################################################
def printBegining(bannerFile=""):
    if sf.exists(bannerFile): printBanner(bannerFile)
    info("Starting")
    printSeparator()


################################################################################
def addOccurenceLog(*args):
    global occurrencesLog
    argsArray = []
    for item in args: argsArray.append(item)
    key = argsArray.pop(0)
    argsArray = [st.formatTimestamp(st.now(), "YYYY/MM/DD HH:mm:ss")] + argsArray
    if key in occurrencesLog: occurrencesLog[key].append(makeMessageFromArgsArray(argsArray))
    else: occurrencesLog[key] = [makeMessageFromArgsArray(argsArray)]


################################################################################
def printOccurencesLog(delete=True):
    global occurrencesLog
    for key in occurrencesLog:
        printSeparator()
        info("Occurence log category", key, len(occurrencesLog[key]), "items")
        for item in occurrencesLog[key]: printLine(item)
    if delete: occurrencesLog = {}
    printSeparator()
