################################################################################
from collections import OrderedDict
from copy import deepcopy
from tabulate import tabulate
from numpy import *
from . import SimpleTime as st
from . import SimplePlot as sp
from . import SimpleString as ss
from . import SimpleFile as sf


################################################################################
def makeUniqueNP(items, keyFunction, keepFirst=True):
    finalItems = zeros(len(items), dtype=items.dtype)
    finalItemsDict = {}
    indexValid = 0
    for index in arange(len(items)):
        itemKey = keyFunction(items[index])
        if keepFirst:
            if not itemKey in finalItemsDict:
                finalItemsDict[itemKey], finalItems[indexValid] = 1, items[index]
                indexValid += 1
        else:
            finalItemsDict[itemKey], finalItems[indexValid] = 1, items[index]
            indexValid += 1
    return resize(finalItems, indexValid)


################################################################################
def makeUnique(items, keyFunction, keepFirst=True):
    finalItems = OrderedDict()
    for item in items:
        itemKey = keyFunction(item)
        if keepFirst:
            if not itemKey in finalItems: finalItems[itemKey] = item
        else: finalItems[itemKey] = item
    return list(finalItems.values())  # python3


################################################################################
def isList(items):
    return isinstance(items, list)


################################################################################
def getValueFromDict(dictionnary, key, defaultValue):
    if key in dictionnary:
        return dictionnary[key]
    else:
        return defaultValue


################################################################################
def compare(lefts, rights, leftKeyFunction, rightKeyFunction):
    leftsDict = {}
    for left in lefts:
        keyOrKeys = leftKeyFunction(left)
        if not isinstance(keyOrKeys, list): keyOrKeys = [keyOrKeys]
        for key in keyOrKeys: leftsDict[key] = left

    rightsDict = {}
    for right in rights:
        keyOrKeys = rightKeyFunction(right)
        if not isinstance(keyOrKeys, list): keyOrKeys = [keyOrKeys]
        for key in keyOrKeys: rightsDict[key] = right

    intersections = []
    for key in leftsDict.keys():
        if key in rightsDict:
            intersections.append(leftsDict[key])

    unionsDict = {}
    for key in rightsDict.keys(): unionsDict[key] = rightsDict[key]
    for key in leftsDict.keys(): unionsDict[key] = leftsDict[key]
    unions = unionsDict.values()

    onlyLefts = []
    for key in leftsDict.keys():
        if not key in rightsDict:
            onlyLefts.append(leftsDict[key])

    onlyRights = []
    for key in rightsDict.keys():
        if not key in leftsDict:
            onlyRights.append(rightsDict[key])

    return list(intersections), list(unions), list(onlyLefts), list(onlyRights)


################################################################################
# scl.superCompare(ptBZ, ptSI, keyFunc, "bz", "si")
# scl.superCompare(ptBZ, ptSI, keyFunc, "bz", "si", outputFolder=PLOTS_FOLDER)
# scl.superCompare(ptBZ, ptSI, keyFunc, "bz", "si", "day", 20130304,20130330,0,PLOTS_FOLDER)
def superCompare(lefts, rights, keyFunction, leftName="lefts", rightName="rights", dayField="day", dayFrom=False, dayTo=False, smoothFactor=30, outputFolder=False, makeUnique=True):
    if not isinstance(lefts, ndarray) or not isinstance(rights, ndarray): raise Exception("lefts and rights must be np arrays")
    if lefts.dtype != rights.dtype: raise Exception("lefts and rights must be of same dtype")

    if dayField and dayFrom: lefts, rights = lefts[lefts[dayField] >= dayFrom], rights[rights[dayField] >= dayFrom]
    if dayField and dayTo: lefts, rights = lefts[lefts[dayField] <= dayTo], rights[rights[dayField] <= dayTo]

    if makeUnique: lefts, rights = makeUniqueNP(lefts, keyFunction), makeUniqueNP(rights, keyFunction)

    intersections, unions, onlyLefts, onlyRights = compare(lefts, rights, keyFunction, keyFunction)
    datas = []
    datas.append(["# " + leftName, len(lefts), ss.percentFormat(len(lefts) / len(unions), 1) + "% of union"])
    datas.append(["# " + rightName, len(rights), ss.percentFormat(len(rights) / len(unions), 1) + "% of union"])
    datas.append(["# only in " + leftName, len(onlyLefts), ss.percentFormat(len(onlyLefts) / len(lefts), 1) + "% of all " + leftName])
    datas.append(["# only in " + rightName, len(onlyRights), ss.percentFormat(len(onlyRights) / len(rights), 1) + "% of all " + rightName])
    datas.append(["# union", len(unions), ""])
    datas.append(["# intersection", len(intersections), ss.percentFormat(len(intersections) / len(unions), 1) + "% of union"])
    summary = tabulate(datas)
    print(summary)

    if not dayField: return

    unions, intersections, onlyLefts, onlyRights = array(unions, dtype=lefts.dtype), array(intersections, dtype=lefts.dtype), array(onlyLefts, dtype=lefts.dtype), array(onlyRights, dtype=lefts.dtype)
    sortedDays = sort(unions[dayField])
    if not dayFrom: dayFrom = sortedDays[0]
    if not dayTo: dayTo = sortedDays[-1]
    days, daysIndexes, dateTimes, naiveDateTimes = st.getDaysList(dayFrom, dayTo)

    figure, plot = sp.figureAndPlot()
    countsByDaysLefts, smoothedCountsByDaysLefts = zeros(len(dateTimes)), zeros(len(dateTimes))
    countsByDaysRights, smoothedCountsByDaysRights = zeros(len(dateTimes)), zeros(len(dateTimes))
    countsByDaysUnions, smoothedCountsByDaysUnions = zeros(len(dateTimes)), zeros(len(dateTimes))
    countsByDaysIntersections, smoothedCountsByDaysIntersections = zeros(len(dateTimes)), zeros(len(dateTimes))
    for item in lefts: countsByDaysLefts[daysIndexes[item[dayField]]] += 1
    for item in rights: countsByDaysRights[daysIndexes[item[dayField]]] += 1
    for item in intersections: countsByDaysIntersections[daysIndexes[item[dayField]]] += 1
    for item in unions: countsByDaysUnions[daysIndexes[item[dayField]]] += 1
    if smoothFactor > 1:
        for i in range(smoothFactor, len(smoothedCountsByDaysLefts) - 1): smoothedCountsByDaysLefts[i] = mean(countsByDaysLefts[i - smoothFactor:i])
        for i in range(smoothFactor, len(smoothedCountsByDaysRights) - 1): smoothedCountsByDaysRights[i] = mean(countsByDaysRights[i - smoothFactor:i])
        for i in range(smoothFactor, len(smoothedCountsByDaysUnions) - 1): smoothedCountsByDaysUnions[i] = mean(countsByDaysUnions[i - smoothFactor:i])
        for i in range(smoothFactor, len(smoothedCountsByDaysIntersections) - 1): smoothedCountsByDaysIntersections[i] = mean(countsByDaysIntersections[i - smoothFactor:i])
    else:
        smoothedCountsByDaysLefts = countsByDaysLefts
        smoothedCountsByDaysRights = countsByDaysRights
        smoothedCountsByDaysUnions = countsByDaysUnions
        smoothedCountsByDaysIntersections = countsByDaysIntersections
    plot.plot()
    plot.plot(dateTimes, smoothedCountsByDaysLefts, label="~ # " + leftName)
    plot.plot(dateTimes, smoothedCountsByDaysRights, label="~ # " + rightName)
    plot.plot(dateTimes, smoothedCountsByDaysUnions, label="~ # unions")
    plot.plot(dateTimes, smoothedCountsByDaysIntersections, label="~ # intersections")
    sp.show()

    if outputFolder:
        sf.makeDir(outputFolder)
        sp.setNameAndSave(figure, plot, "Datas comparaison", "pdf", outputFolder, False, "comp")
        sf.writeToFile(sf.makePath(outputFolder, "comp-summary.txt"), summary)
        sf.dumpNPArray(unions, sf.makePath(outputFolder, "comp-unions.csv"), verbose=True)
        sf.dumpNPArray(intersections, sf.makePath(outputFolder, "comp-intersections.csv"), verbose=True)
        sf.dumpNPArray(lefts, sf.makePath(outputFolder, "comp-" + sf.cleanFileName(leftName) + ".csv"), verbose=True)
        sf.dumpNPArray(rights, sf.makePath(outputFolder, "comp-" + sf.cleanFileName(rightName) + ".csv"), verbose=True)
        sf.dumpNPArray(onlyLefts, sf.makePath(outputFolder, "comp-only-" + sf.cleanFileName(leftName) + ".csv"), verbose=True)
        sf.dumpNPArray(onlyRights, sf.makePath(outputFolder, "comp-only-" + sf.cleanFileName(rightName) + ".csv"), verbose=True)


################################################################################
def groupItemsByKey(items, keyFunction):
    itemsDict = OrderedDict()
    itemsWithIndexesDict = OrderedDict()
    for index in range(len(items)):
        item = items[index]
        itemKey = keyFunction(item)
        if not itemKey in itemsDict: itemsDict[itemKey] = []
        if not itemKey in itemsWithIndexesDict: itemsWithIndexesDict[itemKey] = []
        itemsDict[itemKey].append(item)
        itemsWithIndexesDict[itemKey].append({"item": item, "index": index})
    return itemsDict, itemsWithIndexesDict


################################################################################
def getNonOverlappingItems(items, otherItems, overlappingFunction, overlappingFunctionForOthers=False):
    if not overlappingFunctionForOthers: overlappingFunctionForOthers = overlappingFunction
    overlappingSet = set()
    for otherItem in otherItems: overlappingSet.add(overlappingFunctionForOthers(otherItem))
    nonOverlappingItems, indexValid = zeros(len(items), dtype=items.dtype), 0
    for item in items:
        if overlappingFunction(item) not in overlappingSet:
            nonOverlappingItems[indexValid] = item
            indexValid += 1
    return resize(nonOverlappingItems, indexValid)


################################################################################
def flagOverlappingItems(items, otherItems, overlappingFunction, flagField, flagValue, overlappingFunctionForOthers=False):
    if not overlappingFunctionForOthers: overlappingFunctionForOthers = overlappingFunction
    overlappingSet = set()
    for otherItem in otherItems: overlappingSet.add(overlappingFunctionForOthers(otherItem))
    for index in arange(len(items)):
        if overlappingFunction(items[index]) in overlappingSet: items[index][flagField] = flagValue
    return items


################################################################################
def mergeDictionnaries(mainDictionnary, overridingDictionnary):
    if not isinstance(overridingDictionnary, dict): return overridingDictionnary
    result = deepcopy(mainDictionnary)
    for k, v in overridingDictionnary.items():
        if k in result and isinstance(result[k], dict): result[k] = mergeDictionnaries(result[k], v)
        else: result[k] = deepcopy(v)
    return result


################################################################################
def countItems(items, valueType="U300"):
    valuesKeys = {}
    uniqueItems = unique(items)
    for uniqueItem in uniqueItems: valuesKeys[uniqueItem] = 0
    for item in items: valuesKeys[item] += 1
    result = zeros(len(valuesKeys), dtype=[("value", valueType), ("count", "i8")])
    index = 0
    for key in valuesKeys:
        result[index] = (key, valuesKeys[key])
        index += 1
    return sort(result, order="count")


################################################################################
def nans(shape, dtype=float):
    return -1 + zeros(shape, dtype=dtype)


################################################################################
def fields_view(arr, fields):
    dtype2 = dtype({name: arr.dtype.fields[name] for name in fields})
    return ndarray(arr.shape, dtype2, arr, 0, arr.strides)


################################################################################
def sortDictKeysAlphabetically(dict):
    return OrderedDict(sorted(dict.items(), key=lambda t: t[0]))


################################################################################
def buildIndex(anArray, keyFields):
    indexes = {}
    for index in arange(len(anArray)): indexes[ss.makeKeyFromArray([anArray[index][keyField] for keyField in keyFields])] = index
    return indexes


################################################################################
def buildIndexForKeyFunction(anArray, keyFunction):
    indexes = {}
    for index in arange(len(anArray)): indexes[keyFunction(anArray[index])] = index
    return indexes


################################################################################
def customDistributionGenerateCountsValues(datas, resolution=3000, range=None):
    return histogram(datas, bins=resolution, range=range)


################################################################################
def customDistributionGenerateChoicesArray(counts, values):
    nbBins = len(counts)
    probabilities = counts / sum(counts)
    cdf = cumsum(probabilities)
    distributionsChoices = zeros(len(cdf))
    for index in arange(nbBins): distributionsChoices[index] = values[searchsorted(cdf, index / nbBins)]
    return distributionsChoices

################################################################################
def getFieldsIndexesOfDataStructure(dataStructure):
    fieldsIndexes = {}
    index=0
    for field in dataStructure:
        fieldsIndexes[field[0]]=index
        index+=1
    return fieldsIndexes
