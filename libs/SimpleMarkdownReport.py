################################################################################
from pip._vendor.requests.packages.urllib3.util import url

from . import SimpleCommons as sc
from . import SimpleCollections as scl
from . import SimpleLogger as sl
from . import SimpleString as ss
from . import SimpleFile as sf
from numpy import *
from tabulate import tabulate
import pdfkit
from markdown import markdown
from collections import OrderedDict
import urllib.parse as urllib


################################################################################
class Report:
    ################################################################################
    def __init__(self):
        self.reportString = ""

    ################################################################################
    def line(self, text="",attrs=""):
        text = text.replace("{:", "@@@@@@").replace("{", "\{").replace("@@@@@@", "{:")
        self.reportString += text
        self.reportString += "\n"

    ################################################################################
    def paragraph(self, text="", attrs=""):
        self.line(text)
        self.appendAttrs(attrs)
        self.line()

    ################################################################################
    def sectionSeparator(self):
        self.line("---")
        self.line()

    ################################################################################
    def title(self, title, attrs="", line="="):
        self.line()
        self.line(title)
        self.line(line * len(title))
        self.appendAttrs(attrs)
        self.line()

    ################################################################################
    def subTitle(self, title, attrs=""):
        self.title(title, attrs, line="-")

    ################################################################################
    def table(self, headers, datas, attrs="", format="pipe"):
        self.line(tabulate(datas, headers, tablefmt=format) + self.formatAttrs(attrs))
        # self.appendAttrs(attrs)
        self.line()

    ################################################################################
    def keyValue(self, keys, values, keyName="Key", valueName="Value", attrs=""):
        headers = [keyName, valueName]
        datas = []
        for index in arange(len(keys)):
            if isinstance(values[index], dict): stringValue = ss.dumps(scl.sortDictKeysAlphabetically(values[index]))
            else: stringValue = str(values[index])
            datas.append([keys[index], stringValue])
        self.table(headers, datas, attrs)

    ################################################################################
    def tableFromDict(self, dict, keyName="Key", valueName="Value", attrs="", sortKeys=False):
        if sortKeys: scl.sortDictKeysAlphabetically(dict)
        self.keyValue(list(dict.keys()), list(dict.values()), keyName, valueName, attrs)

    ################################################################################
    def image(self, imagePath, attrs="", alt="image"):
        self.line("""![%s](%s)""" % (alt, urllib.quote(imagePath)) + self.formatAttrs(attrs))
        self.line()

    ################################################################################
    def save(self, filePath):
        sf.writeToFile(filePath, self.reportString)
        sl.debug("Report saved", filePath)

    ################################################################################
    def savePdf(self, filePath, cssPath=""):
        html_text = markdown(self.reportString, extensions=['markdown.extensions.tables', 'markdown.extensions.nl2br', 'markdown.extensions.attr_list'], output_format='html4')
        # print(html_text)
        pdfkit.from_string(html_text, filePath, css=cssPath, options={"quiet": "", "encoding": "UTF-8", "footer-right": "[page]/[toPage]", "footer-font-size": 9})
        sl.debug("Report saved", filePath)

    ################################################################################
    def boldText(self, text):
        return "**" + str(text) + "**"

    ################################################################################
    def italicText(self, text):
        return "*" + str(text) + "*"

    ################################################################################
    def appendAttrs(self, attrs, newLine=True):
        if attrs:
            if newLine: self.line(self.formatAttrs(attrs))
            else: self.reportString += self.formatAttrs(attrs)

    ################################################################################
    def formatAttrs(self, attrs):
        if attrs: return "{: " + attrs + " }"
        else: return ""
