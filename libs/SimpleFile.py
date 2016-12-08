################################################################################
import json
import zipfile
import re
import shutil
import threading
import pandas as pd
import requests as rq
import time
from numpy import *
import os
from zipfile import ZipFile
from os import listdir
from os.path import isfile
from . import SimpleLogger as sl
from . import SimpleString as ss
from . import SimpleTime as st
from . import SimpleCommons as sc
from collections import OrderedDict

# from pdfminer.converter import TextConverter
# from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
# from pdfminer.pdfpage import PDFPage
try: from StringIO import StringIO
except ImportError: from io import StringIO
try: from BytesIO import BytesIO
except ImportError: from io import BytesIO
from ftplib import FTP

################################################################################
CSV_SEP = ";"
CSV_SEP_SAFE = "---"
CSV_MULTIVALUE_SEP = "@@@"


################################################################################
def makeDir(path):
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


################################################################################
def makeDirPath(*args):
    return makeDir(makePath(*args))


################################################################################
def cleanFileName(fileName, title=False):
    if title: fileName = fileName.title()
    return re.sub('[^a-zA-Z0-9-_\.]', '', fileName)


################################################################################
def makePath(*args):
    args = [arg.rstrip("/") for arg in args]
    return '/'.join(str(x) for x in args)


################################################################################
def readCSV(filePath, csvSEP=CSV_SEP, hasHeaders=True, maxColumns=0, encoding="utf-8", debug=False):
    if debug: sl.debug("reading file", filePath)
    try:
        return pd.read_csv(filePath, sep=csvSEP, escapechar="\\", header=0 if hasHeaders else None, low_memory=False, usecols=arange(maxColumns) if maxColumns > 0 else None, encoding=encoding).fillna('').as_matrix()
    except:
        return []


################################################################################
def readCSVs(filePaths, csvSEP=CSV_SEP, pathPrefix="", hasHeaders=True, maxCols=0, encoding="utf-8"):
    if not filePaths: return False
    if pathPrefix: filePaths = [makePath(pathPrefix, filePath) for filePath in filePaths]
    filePath = filePaths.pop(0)
    datas = readCSV(filePath, csvSEP, hasHeaders, maxCols, debug=True, encoding=encoding)
    for filePath in filePaths:
        tmpDatas = readCSV(filePath, csvSEP, hasHeaders, maxCols, debug=True)
        if len(tmpDatas) > 0: datas = concatenate((datas, tmpDatas))
    return datas


################################################################################
def writeToCSV(data, filePath, csvSEP=CSV_SEP, append=False, debug=False):
    if debug: sl.debug("writing file", filePath)
    mode = "w"
    if append: mode = "a"
    csvFile = open(filePath, mode)
    for line in data:
        lineString = ""
        first = True
        for item in line:
            if not first:
                lineString += csvSEP
            else:
                first = False
            if ss.isNaN(item): item = ""
            lineString += ss.removeLineBreaks(str(item).replace(csvSEP, CSV_SEP_SAFE))
        csvFile.write(lineString + "\n")
    csvFile.close()


################################################################################
def appendToCSV(data, filePath, csvSEP=CSV_SEP):
    writeToCSV(data, filePath, csvSEP=csvSEP, append=True)


################################################################################
# fields = [(indexCSV, name, type),...]
def loadNPFromCSV(filePath, fields, csvSEP=CSV_SEP, headers=True, encoding="utf-8", replaceNans=True):
    dType = OrderedDict()
    for field in fields: dType[field[0]] = "unicode" if field[2][0] == "U" else field[2]
    dTypeFinal = [(field[1], field[2]) for field in fields]
    fieldsSortedByIndex = sort(array(fields, dtype=[("index", "i4"), ("name", "U50"), ("type", "U10")]), order="index")
    try:
        df = pd.read_csv(filePath, sep=csvSEP, header=0 if headers else None, escapechar="\\", low_memory=False, usecols=[field[0] for field in fields], names=[field["name"] for field in fieldsSortedByIndex], dtype=dType, encoding=encoding)
        if replaceNans: df = df.fillna('')
        sl.debug("file read", filePath)
        df = df[[field[1] for field in fields]]
        temp = df.to_records(index=False)
        temp.dtype.names = [field[1] for field in fields]
        return temp.view(type=ndarray).astype(dtype=dTypeFinal)
    except Exception as e:
        sl.warning("Error while reading file", filePath, e)
        return array([], dtype=dTypeFinal)


################################################################################
def loadNPFromCSVs(filePaths, fields, csvSEP=CSV_SEP, headers=True):
    if not filePaths: return False
    filePath = filePaths.pop(0)
    datas = loadNPFromCSV(filePath, fields, csvSEP, headers)
    sl.debug("file read", filePath)
    for filePath in filePaths:
        tmpDatas = loadNPFromCSV(filePath, fields, csvSEP, headers)
        if len(tmpDatas) > 0: datas = concatenate((datas, tmpDatas))
        sl.debug("file read", filePath)
    return datas


################################################################################
def exists(file):
    return os.path.exists(file)


################################################################################
def delete(fileOrFolder):
    if os.path.exists(fileOrFolder):
        if os.path.isfile(fileOrFolder):
            os.remove(fileOrFolder)
        else:
            shutil.rmtree(fileOrFolder)


################################################################################
def listDirectoryItems(folder, onlyFiles=False, omitHiddenFiles=True):
    def validItem(folder, file):
        if onlyFiles and not isfile(makePath(folder, file)): return False;
        if omitHiddenFiles and file.startswith("."): return False;
        return True

    return [makePath(folder, f) for f in listdir(folder) if validItem(folder, f)]


################################################################################
def listDirectoriesItems(folders, onlyFiles=False, omitHiddenFiles=True):
    items = []
    for folder in folders: items += listDirectoryItems(folder, onlyFiles, omitHiddenFiles)
    return items


################################################################################
def dumpNPArray(items, file, verbose=False):
    if items.dtype.names is None: final = items
    else:
        if len(items) > 0: final = vstack((array(items.dtype.names), items.tolist()))
        else: final = [array(items.dtype.names)]
    writeToCSV(final, file)
    if verbose:
        sl.debug("NP dump file saved", file)


################################################################################
def writeToFile(filePath, text):
    f = open(filePath, 'w')
    f.write(text)
    f.close()


################################################################################
def writeToBinaryFile(filePath, data):
    f = open(filePath, 'wb')
    f.write(data)
    f.close()


################################################################################
def loadJsonFile(filePath):
    try:
        loadedDatas = json.load(open(filePath))
        return loadedDatas
    except: sl.failure("The json file is absent or syntax is not valid", filePath)


################################################################################
def unzipFile(filePath, destinationPath):
    zipRef = zipfile.ZipFile(filePath, 'r')
    zipRef.extractall(destinationPath)
    zipRef.close()
    return destinationPath


################################################################################
def getFileSize(filePath):
    return os.path.getsize(filePath)


################################################################################
def readFile(filePath,encoding="utf8"):
    return open(filePath,encoding=encoding).read()
