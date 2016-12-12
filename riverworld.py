################################################################################
import libs.SimpleCommons as sc
import libs.SimpleFile as sf
import libs.SimpleLogger as sl
import libs.SimpleString as ss
import libs.SimplePlot as sp
import libs.SimpleTime as st
import libs.SimpleMarkdownReport as smr
from numpy import *
from collections import *
import sys


################################################################################
# HELPERS
################################################################################
def computeAdultsAndBeingsForEera(yearFrom, yearTo, computedPopluationDatas):
    start, countBeingsForEra, countAdultsForEra = False, 0, 0
    for computedData in computedPopluationDatas:
        if computedData["year"] == yearFrom: start = True
        if start:
            countBeingsForEra += computedData["count beings"]
            countAdultsForEra += computedData["count adults"]
        if computedData["year"] == yearTo: break
    return countBeingsForEra, countAdultsForEra


################################################################################
def computeLifeExpectancyForEra(yearFrom, yearTo, popluationDatas):
    start, leFrom, leTo, leaFrom, leaTo = False, 0, 0, 0, 0
    for populationData in popluationDatas:
        if populationData["year"] <= yearFrom: start = True
        if start and leFrom == 0:
            leFrom = populationData["life expectancy"]
            leaFrom = populationData["life expectancy of adults"]
        if populationData["year"] > yearTo:
            leTo = populationData["life expectancy"]
            leaTo = populationData["life expectancy of adults"]
            break
    return (leFrom + leTo) / 2, (leaFrom + leaTo) / 2


################################################################################
def annotations(plot):
    # sp.annotate(plot, ss.makeMessageKeyValueFromArray(["begining of mankind", -700000, "walking homo erectus"]))
    # sp.annotate(plot, ss.makeMessageKeyValueFromArray(["end of mankind", 2016]))
    # sp.annotate(plot, ss.makeMessageKeyValueFromArray(["adult being", "born human being who passed age 5"]))
    # sp.annotate(plot, ss.makeMessageKeyValueFromArray(["being", "born human being"]))
    pass


################################################################################
# INIT
################################################################################
dataVersion = sys.argv[1] if len(sys.argv) >= 2 else "avg"
outputFolder = sf.makeDirPath(sc.SCRIPTS_OUTPUT_FOLDER, dataVersion)
populationSourceFile = sf.makePath(sf.makePath(sc.SCRIPTS_DATA_FOLDER), "population-%s.csv" % dataVersion)
sl.debug("Using dataset %s" % populationSourceFile)
continentFields = ["world", "africa", "asia", "europe", "latin america", "north america", "oceania"]

################################################################################
# LOAD
################################################################################
populationDatas = sf.loadNPFromCSV(populationSourceFile, [(0, "year", "i8"), (1, "count", "f8"), (2, "child mortality", "f8"), (3, "life expectancy", "i4"), (4, "life expectancy of adults", "i4"), (5, "c world", "f4"), (6, "c africa", "f4"), (7, "c asia", "f4"), (8, "c europe", "f4"), (9, "c latin america", "f4"), (10, "c north america", "f4"), (11, "c oceania", "f4")], headers=True)
populationDatas["count"] *= 1e6
computedPopluationDatas = zeros(len(populationDatas), dtype=[("year", "i8"), ("count beings", "i8"), ("count beings function", "i8"), ("count adults", "i8"), ("% total adults", "f8"), ("% total beings", "f8"), ("count adults world", "f4"), ("count adults africa", "f4"), ("count adults asia", "f4"), ("count adults europe", "f4"), ("count adults latin america", "f4"), ("count adults north america", "f4"), ("count adults oceania", "f4")])

################################################################################
# COMPUTE
################################################################################
for index in arange(0, len(populationDatas)):
    computedPopluationDatas[index]["year"] = populationDatas[index]["year"]
    if index == 0: continue
    acm = (populationDatas[index]["child mortality"] + populationDatas[index - 1]["child mortality"]) / 2
    apc = (populationDatas[index]["count"] + populationDatas[index - 1]["count"]) / 2
    alea = (populationDatas[index]["life expectancy of adults"] + populationDatas[index - 1]["life expectancy of adults"]) / 2
    ale = (populationDatas[index]["life expectancy"] + populationDatas[index - 1]["life expectancy"]) / 2
    te = populationDatas[index]["year"] - populationDatas[index - 1]["year"]
    computedPopluationDatas[index]["count adults"] = (1 - acm) * te * apc / alea
    computedPopluationDatas[index]["count beings"] = te * apc / ale
    apcFunction = (populationDatas[index]["count"] - populationDatas[index - 1]["count"]) * te / (log(populationDatas[index]["count"]) - log(populationDatas[index - 1]["count"]))
    computedPopluationDatas[index]["count beings function"] = apcFunction / ale
    for continentField in continentFields: computedPopluationDatas[index]["count adults %s" % continentField] = ((populationDatas[index]["c %s" % continentField] + populationDatas[index - 1]["c %s" % continentField]) / 2) * computedPopluationDatas[index]["count adults"] / 100

totalBeings = sum(computedPopluationDatas["count beings"])
totalAdults = sum(computedPopluationDatas["count adults"])
totalAdultsFunction = sum(computedPopluationDatas["count beings function"])
computedPopluationDatas["% total adults"] = computedPopluationDatas["count adults"] / totalAdults
computedPopluationDatas["% total beings"] = computedPopluationDatas["count beings"] / totalBeings

totalCumulatedAdults = cumsum(computedPopluationDatas["count adults"])
medianIndexAdults = searchsorted(totalCumulatedAdults, totalAdults / 2)
yearMedianAdults = computedPopluationDatas[medianIndexAdults - 1]["year"]
medianPopulationAdults = median(computedPopluationDatas["count adults"])
totalCumulatedBeings = cumsum(computedPopluationDatas["count beings"])
totalCumulatedBeingsFunction = cumsum(computedPopluationDatas["count beings function"])
medianIndexBeings = searchsorted(totalCumulatedBeings, totalBeings / 2)
yearMedianBeings = computedPopluationDatas[medianIndexBeings - 1]["year"]
medianPopulationBeings = median(computedPopluationDatas["count beings"])

totalBeingsByContinents = zeros(len(continentFields))
for index in arange(len(continentFields)): totalBeingsByContinents[index] = sum(computedPopluationDatas["count adults %s" % continentFields[index]])
totalBeingsByContinentsRatio = totalBeingsByContinents / totalAdults

paleolithicalCountBeings, paleolithicalCountAdults = computeAdultsAndBeingsForEera(-700000, -50000, computedPopluationDatas)
neolithicalCountBeings, neolithicalCountAdults = computeAdultsAndBeingsForEera(-50000, -10000, computedPopluationDatas)
neolithicalUntiJCCountBeings, neolithicalUntiJCCountAdults = computeAdultsAndBeingsForEera(-10000, 1, computedPopluationDatas)
afterWWICountBeings, afterWWICountAdults = computeAdultsAndBeingsForEera(1950, inf, computedPopluationDatas)
classicalAthensWithCivilRightsAdultsCount = (-322 - -508) * 3e4 / computeLifeExpectancyForEra(-508, -322, populationDatas)[1]
classicalAthensAdultsCount = (-322 - -508) * 2.5e5 / computeLifeExpectancyForEra(-508, -322, populationDatas)[1]
romanRepublicAdultsCount = (-27 - -509) * 3e5 / computeLifeExpectancyForEra(-509, -27, populationDatas)[1]
westerRomanEmpireAdultsCount = (476 - -27) * 45e6 / computeLifeExpectancyForEra(-27, 476, populationDatas)[1]

################################################################################
# PLOT
################################################################################
tickLabels = zeros(len(computedPopluationDatas), dtype="U20")
for index in arange(0, len(computedPopluationDatas)):
    if index == 0: tickLabels[index] = r"$-\infty>$" + str(computedPopluationDatas[index]["year"])
    else: tickLabels[index] = str(computedPopluationDatas[index - 1]["year"]) + ">" + str(computedPopluationDatas[index]["year"])

figure, plot = sp.figureAndPlot()
annotations(plot)
plot.xaxis.grid(False)
plot.xaxis.set_ticks_position("none")
h = plot.bar(arange(len(computedPopluationDatas)), 100 * computedPopluationDatas["% total adults"], 0.7, label="% of total adult beings", color=sp.getNextColor())
plot.set_xticks([0.5 * patch.get_width() + patch.get_xy()[0] for patch in h])
plot.set_xticklabels(tickLabels, rotation=20)
sp.hideSpines(plot, vertical=True)
sp.setNameAndSave(figure, plot, "Riverworld distribution of adult beings eras amongst all adult beings ever born", folder=outputFolder, datePrefix=False, format="svg")

figure, plot = sp.figureAndPlot()
annotations(plot)
plot.xaxis.grid(False)
plot.xaxis.set_ticks_position("none")
h = plot.bar(arange(len(continentFields) - 1), 100 * totalBeingsByContinentsRatio[1:len(continentFields)], 0.7, label="% of total adult beings", color=sp.getNextColor())
plot.set_xticks([0.65 * patch.get_width() + patch.get_xy()[0] for patch in h])
plot.set_xticklabels(continentFields[1:len(continentFields)], rotation=20, ha="right")
sp.hideSpines(plot, vertical=True)
sp.setNameAndSave(figure, plot, "Riverworld distribution of adult beings continents amongst all adult beings ever born", folder=outputFolder, datePrefix=False, format="svg")

figure, plot = sp.figureAndPlot()
annotations(plot)
plot.xaxis.grid(False)
plot.xaxis.set_ticks_position("none")
h = plot.bar(arange(len(computedPopluationDatas)), totalCumulatedAdults, 0.7, label="cumulated amount of adult beings", color=sp.getNextColor())
plot.set_xticks([0.5 * patch.get_width() + patch.get_xy()[0] for patch in h])
plot.set_xticklabels(tickLabels, rotation=20)
sp.hideSpines(plot, vertical=True)
sp.setNameAndSave(figure, plot, "Riverworld cumulated amount of adult beings ever born", folder=outputFolder, datePrefix=False, format="svg")

figure, plot = sp.figureAndPlot()
annotations(plot)
plot.xaxis.grid(False)
plot.xaxis.set_ticks_position("none")
h = plot.bar(arange(len(computedPopluationDatas)), 100 * computedPopluationDatas["% total beings"], 0.35, label="% of total beings", color=sp.getNextColor())
h = plot.bar(arange(len(computedPopluationDatas)) + 0.35, 100 * computedPopluationDatas["% total adults"], 0.35, label="% of total adult beings", color=sp.getNextColor())
# h = plot.bar(arange(len(computedPopluationDatas)), 100 * computedPopluationDatas["% total beings"], 0.35, label="% des êtres humains parmis l'intégralité des êtres humains", color=sp.getNextColor())
# h = plot.bar(arange(len(computedPopluationDatas)) + 0.35, 100 * computedPopluationDatas["% total adults"], 0.35, label="% des êtres humains adultes parmis l'intégralité des êtres humains adultes", color=sp.getNextColor())
plot.set_xticks([0.2 * patch.get_width() + patch.get_xy()[0] for patch in h])
plot.set_xticklabels(tickLabels, rotation=20)
sp.hideSpines(plot, vertical=True)
sp.setNameAndSave(figure, plot, "Riverworld distribution of beings eras amongst all beings ever born", folder=outputFolder, datePrefix=False, format="svg")
# sp.setNameAndSave(figure, plot, "Distribution des êtres humains par période historique", folder=outputFolder, datePrefix=False, format="png")

figure, plot = sp.figureAndPlot()
annotations(plot)
plot.xaxis.grid(False)
plot.xaxis.set_ticks_position("none")
h = plot.bar(arange(len(computedPopluationDatas)), totalCumulatedBeings, 0.7, label="cumulated amount of beings", color=sp.getNextColor())
h = plot.bar(arange(len(computedPopluationDatas)), totalCumulatedAdults, 0.7, label="cumulated amount of adult beings", color=sp.getNextColor())
# h = plot.bar(arange(len(computedPopluationDatas)), totalCumulatedBeings, 0.7, label="cumul des êtres humains", color=sp.getNextColor())
# h = plot.bar(arange(len(computedPopluationDatas)), totalCumulatedAdults, 0.7, label="cumul des êtres humains adultes", color=sp.getNextColor())
plot.set_xticks([0.2 * patch.get_width() + patch.get_xy()[0] for patch in h])
plot.set_xticklabels(tickLabels, rotation=20)
sp.hideSpines(plot, vertical=True)
sp.setNameAndSave(figure, plot, "Riverworld cumulated amount of beings ever born", folder=outputFolder, datePrefix=False, format="svg")
# sp.setNameAndSave(figure, plot, "Cumul des êtres humains", folder=outputFolder, datePrefix=False, format="png")

figure, plot = sp.figureAndPlot()
annotations(plot)
plot.xaxis.grid(False)
plot.xaxis.set_ticks_position("none")
h = plot.bar(arange(len(computedPopluationDatas)), totalCumulatedBeings, 0.7, label="cumulated amount of beings - numercial integration", color=sp.getNextColor())
h = plot.bar(arange(len(computedPopluationDatas)), totalCumulatedBeingsFunction, 0.7, label="cumulated amount of beings - growth function integration", color=sp.getNextColor())
# h = plot.bar(arange(len(computedPopluationDatas)), totalCumulatedBeings, 0.7, label="cumul des êtres humains nés - intégration numérique", color=sp.getNextColor())
# h = plot.bar(arange(len(computedPopluationDatas)), totalCumulatedBeingsFunction, 0.7, label="cumul des êtres humains nés - intégration de la fonction de croissance", color=sp.getNextColor())
plot.set_xticks([0.2 * patch.get_width() + patch.get_xy()[0] for patch in h])
plot.set_xticklabels(tickLabels, rotation=20)
sp.hideSpines(plot, vertical=True)
sp.setNameAndSave(figure, plot, "Riverworld cumulated amount of beings ever born - calculs comparaison", folder=outputFolder, datePrefix=False, format="svg")
# sp.setNameAndSave(figure, plot, "Cumul des êtres humains - comparaison des méthodes de calcul", folder=outputFolder, datePrefix=False, format="png")

sp.show()

mainResults = OrderedDict([
    ("Total beigns ever born", ss.floatFormat(totalBeings / 1e9, 1) + " billions"),
    ("Total adult beigns ever born", ss.floatFormat(totalAdults / 1e9, 1) + " billions"),
    ("Proportion of alive beings amongst all beings ever born", ss.floatFormat(100 * populationDatas[-1]["count"] / totalBeings, 1) + "%"),
    ("Median year of adult beings ever born", yearMedianAdults),
    ("Median year of beings ever born", yearMedianBeings)
])

proportionResults = OrderedDict([
    ("Me", "%s%% (%s)" % (ss.floatFormat(100 / totalBeings, 20), 1)),
    ("Asians", "%s%% (%.2e)" % (ss.floatFormat(100 * totalBeingsByContinentsRatio[continentFields.index("asia")], 0), totalBeingsByContinents[continentFields.index("asia")])),
    ("Paloelithical era", "%s%% (%.1e)" % (ss.floatFormat(100 * paleolithicalCountAdults / totalAdults, 1), paleolithicalCountAdults)),
    ("Neolithical era", "%s%% (%.1e)" % (ss.floatFormat(100 * neolithicalCountAdults / totalAdults, 1), neolithicalCountAdults)),
    ("-10K until the birh of Jesus Christ", "%s%% (%.1e)" % (ss.floatFormat(100 * neolithicalUntiJCCountAdults / totalAdults, 1), neolithicalUntiJCCountAdults)),
    ("Classical Athens (508 BC - 322 BC) (with civil rights)", "%s%% (%.1e)" % (ss.floatFormat(100 * classicalAthensWithCivilRightsAdultsCount / totalAdults, 3), classicalAthensWithCivilRightsAdultsCount)),
    ("Classical Athens (508 BC - 322 BC)", "%s%% (%.1e)" % (ss.floatFormat(100 * classicalAthensAdultsCount / totalAdults, 3), classicalAthensAdultsCount)),
    ("Roman Republic (509 BC - 27 BC)", "%s%% (%.1e)" % (ss.floatFormat(100 * romanRepublicAdultsCount / totalAdults, 3), romanRepublicAdultsCount)),
    ("Western Roman Empire (27 BC - 476 AD)", "%s%% (%.1e)" % (ss.floatFormat(100 * westerRomanEmpireAdultsCount / totalAdults, 1), westerRomanEmpireAdultsCount)),
    ("After WWII", "%s%% (%.1e)" % (ss.floatFormat(100 * afterWWICountAdults / totalAdults, 0), afterWWICountAdults)),
])

report = smr.Report()
report.line(sf.readFile(sc.ROOT_FOLDER + "/README.md", encoding="utf8"))
report.sectionSeparator()
report.title("Results")
report.line("Dataset used : `%s`" % populationSourceFile.split("/")[-1])
report.subTitle("Main results")
report.tableFromDict(mainResults, "metric", "value", attrs=".std-table")
report.subTitle("Proportion of adult beings amongst all adults ever born")
report.tableFromDict(proportionResults, "sub population", "value", attrs=".std-table")
report.sectionSeparator()
report.subTitle("Adult beings results")
report.image(sf.makePath(outputFolder, "Riverworld_Distribution_Of_Adult_Beings_Eras_Amongst_All_Adult_Beings_Ever_Born.svg"), ".plot")
report.paragraph("figure 1", ".legend")
report.image(sf.makePath(outputFolder, "Riverworld_Distribution_Of_Adult_Beings_Continents_Amongst_All_Adult_Beings_Ever_Born.svg"), ".plot")
report.paragraph("figure 2", ".legend")
report.image(sf.makePath(outputFolder, "Riverworld_Cumulated_Amount_Of_Adult_Beings_Ever_Born.svg"), ".plot")
report.paragraph("figure 3", ".legend")
report.sectionSeparator()
report.subTitle("All beings results")
report.image(sf.makePath(outputFolder, "Riverworld_Distribution_Of_Beings_Eras_Amongst_All_Beings_Ever_Born.svg"), ".plot")
report.paragraph("figure 4", ".legend")
report.image(sf.makePath(outputFolder, "Riverworld_Cumulated_Amount_Of_Beings_Ever_Born.svg"), ".plot")
report.paragraph("figure 5", ".legend")
report.image(sf.makePath(outputFolder, "Riverworld_Cumulated_Amount_Of_Beings_Ever_Born_-_Calculs_Comparaison.svg"), ".plot")
report.paragraph("figure 6", ".legend")
# report.save(sf.makePath(outputFolder, "report.md"))
report.savePdf(sf.makePath(outputFolder, "report.pdf"), sf.makePath(sc.RESOURCES_FOLDER, "report.css"))
