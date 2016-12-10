################################################################################
import matplotlib as mp
import matplotlib.colors as colors
import numpy as np
from . import SimpleFile as sf
from . import SimpleString as ss
from . import SimpleTime as st
from . import SimpleLogger as sl
from . import SimpleCommons as sc
from cycler import cycler

################################################################################
mp.use("Agg")
import matplotlib.pyplot as plt

################################################################################
INTERACTIVE_MODE = True
ANNOTATE_STEP = 0.02
################################################################################
COLOR_ALPHA = 0.8
COLOR_WHITE = "#FFFFFF"
COLOR_GRAY = "#F1F1F1"
COLOR_LIGHT_GRAY = "#F9F9F9"
COLOR_MEDIUM_GRAY = "#808080"
COLOR_DARKER_GRAY = "#333333"
COLOR_BLUE = "#0194ed"
COLOR_GREEN = "#37a500"
COLOR_RED = "#e53b00"
COLOR_CYAN = "#8e009b"
COLOR_MAGENTA = "#ff4c8f"
COLOR_YELLOW = "#ffb514"
COLOR_BLACK = "#000000"

################################################################################
someFiguresHaveBeenWorkedOn = False
colorIndex = 0
createdPlots = []
createdFigures = []


################################################################################
def init(interactiveMode=True):
    global INTERACTIVE_MODE
    INTERACTIVE_MODE = interactiveMode
    if not INTERACTIVE_MODE: plt.switch_backend('Agg')
    else: plt.switch_backend("TkAgg")  # so windows are mosaicable, if not working, comment line for default backend


################################################################################
def colorToRGBA(color, alpha):
    return mp.colors.ColorConverter().to_rgba(color, alpha)


################################################################################
def getNextColor():
    global colorIndex
    color = plt.rcParams["axes.prop_cycle"].by_key()["color"][colorIndex % len(plt.rcParams["axes.prop_cycle"])]
    colorIndex += 1
    return color


################################################################################
def setNameAndSave(figure, plot, title, format="pdf", folder="", datePrefix=False, prefix=False):
    global createdPlots
    # for createdPlot in createdPlots: modifyPlotHelper(createdPlot)
    modifyPlotHelper(plot)
    if prefix: title = prefix + " - " + title
    title = ss.title(title)
    figure.suptitle(title)
    fileName = sf.cleanFileName(ss.replaceSpaces(title, replaceChar="_")) + "." + format.lower()
    if datePrefix: fileName = st.formatTimestamp(st.now(), "YYYYMMDD-HHmm-") + fileName
    if folder: fileName = sf.makePath(folder, fileName)
    figure.savefig(fileName, format=format)
    sl.debug("Plot saved", title)
    return fileName


################################################################################
def figure():
    global colorIndex, annotateIndex, someFiguresHaveBeenWorkedOn
    someFiguresHaveBeenWorkedOn = True
    colorIndex = 0
    annotateIndex = 1
    theFigure = plt.figure()
    # theFigure.gca().set_frame_on(False)
    return theFigure


################################################################################
def figureAndPlot():
    global createdPlots, createdFigures
    theFigure = figure()
    thePlot = theFigure.add_subplot(111)
    thePlot.tick_params(labelright=True)
    createdPlots.append(thePlot)
    createdFigures.append(theFigure)
    return theFigure, thePlot


################################################################################
def figureAndDayPlot():
    figure, plot = figureAndPlot()
    setAxisDayFormatter(plot.xaxis)
    return figure, plot


################################################################################
def figureAndDayTimePlot():
    figure, plot = figureAndPlot()
    setAxisDayTimeFormatter(plot.xaxis)
    return figure, plot


################################################################################
def close(figure):
    plt.close(figure)


################################################################################
def subplot():
    global createdPlots
    theSubplot = plt.subplot()
    createdPlots.append(theSubplot)
    return theSubplot


################################################################################
def setAxisDayFormatter(axis):
    axis.set_major_formatter(mp.dates.DateFormatter('%d-%m-%Y'))


################################################################################
def setAxisDayTimeFormatter(axis):
    axis.set_major_formatter(mp.dates.DateFormatter('%d-%m-%Y-%H:%M'))


################################################################################
def setAxisMajorLocator(axis, locator):
    axis.set_major_locator(mp.ticker.MultipleLocator(locator))


################################################################################
def setAxisFormatter(axis, formatter):
    axis.set_major_formatter(formatter)


################################################################################
def showPlots(block=True):
    global createdPlots, createdFigures
    if INTERACTIVE_MODE:
        for createdPlot in createdPlots: modifyPlotHelper(createdPlot)
        if not block: plt.show(block=block)
        else: plt.show()
    else: closePlots()


################################################################################
def closePlots():
    for createdFigure in createdFigures: close(createdFigure)


################################################################################
def show(block=True):
    if someFiguresHaveBeenWorkedOn: showPlots(block)


################################################################################
def isOutlier(points, thresh=3.5):
    if len(points.shape) == 1:
        points = points[:, None]
    median = np.median(points, axis=0)
    diff = np.sum((points - median) ** 2, axis=-1)
    diff = np.sqrt(diff)
    med_abs_deviation = np.median(diff)
    modified_z_score = 0.6745 * diff / med_abs_deviation
    return modified_z_score > thresh


#################################################################################
def annotate(plot, *texts):
    global annotateIndex
    plot.text(0.015, 1 - annotateIndex * ANNOTATE_STEP, ss.makeMessageKeyValueFromArray(texts), horizontalalignment='right', verticalalignment='top', transform=plot.transAxes)
    annotateIndex += 1


#################################################################################
def setupPlots():
    plt.rcParams["text.usetex"] = False
    plt.rcParams["text.color"] = COLOR_DARKER_GRAY
    plt.rcParams["font.size"] = 10
    plt.rcParams["axes.titlesize"] = 1.1 * plt.rcParams["font.size"]
    plt.rcParams["legend.fontsize"] = plt.rcParams["font.size"]
    plt.rcParams["xtick.labelsize"] = plt.rcParams["font.size"]
    plt.rcParams["ytick.labelsize"] = plt.rcParams["font.size"]
    plt.rcParams["axes.labelsize"] = 10
    plt.rcParams["font.family"] = "Montserrat"
    plt.rcParams["axes.facecolor"] = COLOR_WHITE
    plt.rcParams["axes.edgecolor"] = COLOR_GRAY
    plt.rcParams["axes.labelcolor"] = COLOR_DARKER_GRAY
    availableColors = np.array([[31, 67, 174], [229, 59, 0], [55, 165, 0], [255, 76, 230], [0, 221, 184], [255, 181, 20], [72, 0, 121], [184, 207, 133], [137, 0, 1], [1, 152, 137], [255, 76, 143], [122, 202, 255], [75, 56, 0], [226, 130, 255], [255, 135, 118], [224, 1, 175], [26, 35, 75], [103, 0, 69], [1, 110, 225], [216, 85, 0]]) / 255.
    # geotheque colors
    # availableColors = np.array([[196, 22, 49], [34, 34, 34], [55, 165, 0], [255, 76, 230], [0, 221, 184], [255, 181, 20], [72, 0, 121], [184, 207, 133], [137, 0, 1], [1, 152, 137], [255, 76, 143], [122, 202, 255], [75, 56, 0], [226, 130, 255], [255, 135, 118], [224, 1, 175], [26, 35, 75], [103, 0, 69], [1, 110, 225], [216, 85, 0]]) / 255.
    plt.rcParams["axes.prop_cycle"] = cycler("color", availableColors.tolist())
    plt.rcParams["xtick.color"] = COLOR_DARKER_GRAY
    plt.rcParams["ytick.color"] = COLOR_DARKER_GRAY
    plt.rcParams["axes.grid"] = True
    plt.rcParams["patch.edgecolor"] = "none"
    # plt.rcParams["patch.facecolor"] = COLOR_DARK_GRAY
    plt.rcParams["grid.alpha"] = 0.3
    plt.rcParams["figure.subplot.hspace"] = 0.3
    plt.rcParams["figure.subplot.wspace"] = 0.3
    plt.rcParams["figure.subplot.top"] = 0.94
    plt.rcParams["figure.subplot.bottom"] = 0.06
    plt.rcParams["figure.subplot.right"] = 0.94
    plt.rcParams["figure.subplot.left"] = 0.06
    plt.rcParams["figure.facecolor"] = COLOR_WHITE
    plt.rcParams["figure.figsize"] = (14, 10)
    plt.rcParams["figure.max_open_warning"] = 50
    plt.rcParams["figure.titlesize"] = 1.2 * plt.rcParams["font.size"]
    plt.rcParams["legend.fancybox"] = True
    # plt.rcParams["legend.framealpha"] = 0.5
    plt.rcParams["legend.frameon"] = False
    plt.rcParams["legend.fontsize"] = 10
    plt.rcParams["xtick.major.pad"] = 8
    plt.rcParams["ytick.major.pad"] = 10
    plt.rcParams["axes.formatter.useoffset"] = False
    pass


#################################################################################
def modifyPlotHelper(plot):
    plot.legend(loc="upper left")
    plot.autoscale(enable=True, axis='x', tight=True)
    # hideSpines(plot,all=True)


#################################################################################
def hideSpines(plot, all=False, top=False, bottom=False, left=False, right=False, vertical=False, horizontal=False):
    # for ticks in plot.xaxis.get_ticklines() + plot.yaxis.get_ticklines():
    #     ticks.set_color(COLOR_WHITE)
    if all or top or horizontal: plot.spines["top"].set_edgecolor(COLOR_WHITE)
    if all or bottom or horizontal: plot.spines["bottom"].set_edgecolor(COLOR_WHITE)
    if all or left or vertical: plot.spines["left"].set_edgecolor(COLOR_WHITE)
    if all or right or vertical: plot.spines["right"].set_edgecolor(COLOR_WHITE)


#################################################################################
def showAvailableFonts():
    import matplotlib.font_manager
    print([f.name for f in matplotlib.font_manager.fontManager.ttflist])
    sl.debug("Remove matplotlib font cache to force update (~/.matplotlib/xxxx)")
