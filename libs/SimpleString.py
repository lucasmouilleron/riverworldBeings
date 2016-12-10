################################################################################
import csv
import hashlib
import json
import re
import string
import sys
import uuid
import pickle
from numpy import *
from . import SimpleFile as sf
import html

try: from StringIO import StringIO
except: from io import StringIO

################################################################################
# python3 fixes
if sys.version_info > (3,): long = int
################################################################################
# python2 fixes
try:
    reload(sys)
    sys.setdefaultencoding("utf8")
except:  pass

################################################################################
# REGEX_SENTENCES = re.compile("[^.?!]*[.?!]", re.S)
REGEX_SENTENCES = re.compile("[^.!?\s][^.!?]*(?:[.!?](?!['\"]?\s|$)[^.!?]*)*[.!?]?['\"]?(?=\s|$)", re.S)
REGEX_DOUBLE_SPACES = re.compile('\s\s+')
REGEX_SPACES = re.compile('\s')
REGEX_CLEAN_AGRESSIVE = re.compile('[^\w]', re.I)
REGEX_NON_PRINTABLE = re.compile('[\x00-\x08\x0B\x0C\x0E-\x1F\x80-\x9F]', re.UNICODE)
REGEX_NON_PRINTABLE_MORE = re.compile('[^\s!-~]')
REGEX_HTML_TAGS = re.compile('<[^<]+?>')
REGEX_HTML_SCRIPT_TAGS = re.compile('<script.*?</script>', re.S | re.I)
REGEX_HTML_STYLE_TAGS = re.compile('<style.*?</style>', re.S | re.I)
REGEX_HTML_CONTENTS_TAGS = re.compile('<!--.*?-->', re.S | re.I)
REGEX_PRICE_WITHOUT_CURRENCIES = re.compile("([\d,.]+)", re.I | re.S)


################################################################################
def dumps(obj, jsonFormat=False):
    if jsonFormat: json.dumps(obj)
    else: return json.dumps(obj, default=JSONPrintSetDefault)


################################################################################
def uniqueID():
    return str(uuid.uuid4())


################################################################################
def makeMessage(*args):
    cleanedArgs = []
    for arg in args: cleanedArgs.append(dumps(arg).strip('"'))
    return ' / '.join(cleanedArgs)


################################################################################
def makeMessageKeyValueFromArray(items):
    if len(items) == 1: return items[0]
    cleanedArgs = []
    for i in range(0, len(items) - 1, 2): cleanedArgs.append(str(items[i]) + " : " + dumps(str(items[i + 1])).strip('"'))
    return ' / '.join(cleanedArgs)


################################################################################
def makeMessageKeyValue(*args):
    return makeMessageKeyValueFromArray(args)


################################################################################
def join(items, sep="/"):
    return sep.join([str(item) for item in items])


################################################################################
def removeHeaderLines(string, nbHeaderLines):
    strings = string.split("\n")
    if len(strings) > nbHeaderLines:
        strings = strings[nbHeaderLines:]
    return "\n".join(strings)


################################################################################
def removeFooterLines(string, nbFooterLines):
    strings = string.split("\n")
    if len(strings) > nbFooterLines:
        strings = strings[:-nbFooterLines]
    return "\n".join(strings)


################################################################################
def removeDoubleSpaces(string):
    return REGEX_DOUBLE_SPACES.sub(' ', string)


################################################################################
def removeSpaces(string):
    return REGEX_SPACES.sub('', string)


################################################################################
def removeLineBreaks(string):
    return string.replace('\n', ' ').replace('\r', ' ')


################################################################################
def removeNonPrintableChars(theString):
    return ''.join([x for x in theString if x in string.printable])


################################################################################
def removeMoreNonPrintableChars(string):
    return REGEX_NON_PRINTABLE_MORE.sub(' ', string)


################################################################################
def removeScriptsCSSAndComments(string):
    return REGEX_HTML_CONTENTS_TAGS.sub(' ', REGEX_HTML_SCRIPT_TAGS.sub(' ', REGEX_HTML_STYLE_TAGS.sub(' ', string)))


################################################################################
def replaceSpaces(content, replaceChar="_"):
    return content.replace(" ", replaceChar)


################################################################################
def cleanFromHTML(string):
    return removeNonPrintableChars(removeDoubleSpaces(decodeHTMLEntitites(REGEX_HTML_TAGS.sub(' ', removeScriptsCSSAndComments(string))).strip()))


################################################################################
def cleanAgressive(string):
    return REGEX_CLEAN_AGRESSIVE.sub('', cleanFromHTML(string)).lower()


################################################################################
def cleanNumber(number):
    return re.sub("[^\d\.-]", "", number).rstrip("\.")


################################################################################
def cleanOnlyLetters(string):
    return ''.join([c for c in string if c.isalpha()])


################################################################################
def isNegativeFinanceNumber(numberString):
    return "(" in numberString and ")" in numberString


################################################################################
def decodeHTMLEntitites(string):
    return html.unescape(string)


################################################################################
def contains(needle, haystack):
    return needle in haystack


################################################################################
def containss(needles, haystack):
    for needle in needles:
        if needle in haystack: return True
    return False


################################################################################
def title(string):
    return ' '.join([s[0].upper() + s[1:] for s in string.split(' ')])
    # return ' '.join([s[0] + s[1:] for s in string.split(' ')])


################################################################################
def isNumber(string):
    try:
        float(string)
        return True
    except:
        return False


################################################################################
def isNaN(num):
    return num != num


################################################################################
def parseCSV(CSVString, delimiter=";", lineBreak="\n", removeHeaders=False):
    f = StringIO.StringIO(CSVString)
    datas = list(csv.reader(f, delimiter=delimiter, lineterminator=lineBreak))
    if removeHeaders and len(datas) > 0:
        datas.pop(0)
    return datas


################################################################################
def regexMakeOrGroup(items):
    return "(?:" + "|".join(items) + ")"


################################################################################
def regexCapture(item):
    return "(" + item + ")"


################################################################################
def regexCaptureNotMandatory(item):
    return "(" + item + ")?"


################################################################################
def regexSurroundBySeparators(item, canBeBeginner=False, canBeEnder=False):
    leftTokens = "\s,:;" if not canBeBeginner else "\s,:;.?!("
    rightTokens = "\s,:;" if not canBeEnder else "\s,:;.?!)"
    return "[" + leftTokens + "]+?" + item + "[" + rightTokens + "]+?"


################################################################################
def regexSurroundByOptionalSpaces(item):
    return "\s*?" + item + "\s*?"


################################################################################
def regexAnythingButDot(size=0):
    return "[^.]*?" if size == 0 else "[^.]{0," + str(size) + "}?"


################################################################################
def regexAnything(size=0):
    return ".*?" if size == 0 else ".{0," + str(size) + "}?"


################################################################################
def regexGetSentences(text, trimEndToken=True):
    sentences = []
    for sentence in REGEX_SENTENCES.findall(text):
        if len(sentence) > 1:
            sentences.append(sentence if not trimEndToken else sentence.rstrip(".!?"))
    return sentences


################################################################################
def regexGetFirstResult(matches, defaultValue=""):
    if len(matches) == 0: return defaultValue
    else: return matches[0]


################################################################################
def cleanAndParsePrice(priceString, defaultValue, factor=1):
    try:
        factor = 1 * factor if not isNegativeFinanceNumber(priceString) else -1 * factor
        return factor * float(cleanNumber(priceString))
    except ValueError:
        return defaultValue


################################################################################
def parsePrice(priceString, multiplierString="", defaultValue=0):
    try:
        price = float(REGEX_PRICE_WITHOUT_CURRENCIES.search(priceString).group(1))
        k = {"k"}
        millions = {"m", "million"}
        billions = {"b", "billion"}
        precents = {"%"}
        if multiplierString.lower() in k: return price * 1e3
        if multiplierString.lower() in millions: return price * 1e6
        if multiplierString.lower() in billions: return price * 1e9
        if multiplierString.lower() in precents: return price * 1e-2
        return price
    except Exception:
        return defaultValue


################################################################################
def parseFloat(floatString, defaultValue):
    try:
        return float(floatString)
    except ValueError:
        return defaultValue


################################################################################
def parseLong(longstring, defaultValue):
    try:
        return long(longstring)
    except ValueError:
        return defaultValue


################################################################################
def parseInt(intString, defaultValue):
    try:
        return int(intString)
    except ValueError:
        return defaultValue


################################################################################
def makeHashFromArguments(*args):
    serializedString = []
    for arg in args: serializedString.append(pickle.dumps(arg))
    for index in arange(len(serializedString)): serializedString[index] = serializedString[index].decode("latin1")
    return hashlib.md5('-'.join(serializedString).encode()).hexdigest()


################################################################################
def makeHashFromDict(dict, authorizedKeys={}, md5=False):
    items = []
    for (key, value) in sorted(dict.items()):
        if len(authorizedKeys) == 0 or key in authorizedKeys: items.append(str(key) + "--" + str(value))
    if not md5: return sf.cleanFileName("---".join(items))
    else: return hashlib.md5("---".join(items).encode()).hexdigest()


################################################################################
def makeKeyFromArguments(*args):
    return "--".join(str(arg) for arg in args)


################################################################################
def makeKeyFromArray(array):
    return "--".join(str(item) for item in array)


################################################################################
def joinObjects(*args, **kwargs):
    sep = kwargs.get("sep", "-")
    joined = ""
    for index in range(len(args)):
        if index != 0: joined += sep
        if isinstance(args[index], dict): joined += makeHashFromArguments(args[index])
        else: joined += str(args[index])
    return joined


################################################################################
def toString(item):
    if isNaN(item): return ""
    return str(item)


################################################################################
def getWords(content, lower=True):
    if lower: content = content.lower()
    return re.sub("[^\w]", " ", content).split()


################################################################################
def containsItemsBeforePosition(items, content, position, length):
    return containss(items, content[max(0, position - length):position])


################################################################################
def containsItemsAfterPosition(items, content, position, length):
    return containss(items, content[position:min(len(content) - 1, position + length - 1)])


################################################################################
def camelCaseToString(string):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1 \2', s1).lower()


################################################################################
def JSONPrintSetDefault(obj):
    if isinstance(obj, set): return list(obj)
    if isinstance(obj, ndarray): return obj.tolist()
    return str(obj)


################################################################################
def percentFormat(number, decimals=2):
    return floatFormat(100 * number, decimals)


################################################################################
def floatFormat(number, decimals=2):
    if decimals == 0: return str(int(number))
    else: return str(around(number, decimals=decimals))
