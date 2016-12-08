################################################################################
import datetime
import time
import arrow
import dateutil
from numpy import *
from collections import OrderedDict
from pytz import timezone
from . import SimpleCommons as sc
from datetime import timedelta as td

################################################################################
# cf http://crsmithdev.com/arrow/

################################################################################
ONE_HOUR_IN_SEC = 1 * 60 * 60
ONE_DAY_IN_SEC = 24 * 60 * 60
ONE_MONTH_IN_SEC = 31 * 24 * 60 * 60
ONE_YEAR_IN_SEC = 365 * 24 * 60 * 60
ONE_MINUTE_IN_SEC = 1 * 60
################################################################################
DAYS_OF_WEEK = {0: "monday", 1: "tuesday", 2: "wednesday", 3: "thursday", 4: "friday", 5: "saturday", 6: "sunday"}
NB_OPENED_DAYS_IN_YEAR = 252


################################################################################
def getDateTimeFromTimestamp(timestamp, timezone=sc.TIMEZONE_DEFAULT):
    return datetime.datetime.fromtimestamp(timestamp, tz=dateutil.tz.gettz(timezone))


################################################################################
def getDateTime(date, format, timezone=sc.TIMEZONE_DEFAULT):
    return datetime.datetime.fromtimestamp(parseDate(date, format, timezone), tz=dateutil.tz.gettz(timezone))


################################################################################
def getDateTimeFromYearMonthDay(yearMonthDay, timezone=sc.TIMEZONE_DEFAULT):
    return datetime.datetime(getYearFromYearMonthDay(yearMonthDay), getMonthOnlyFromYearMonthDay(yearMonthDay), getDayOnlyFromYearMonthDay(yearMonthDay), 0, 0, tzinfo=dateutil.tz.gettz(timezone))


################################################################################
def getDateTimeFromYearMonth(yearMonth, timezone=sc.TIMEZONE_DEFAULT):
    return getDateTimeFromYearMonthDay(yearMonth * 100 + 1, timezone)


################################################################################
def getDateTimeFromYear(year, timezone=sc.TIMEZONE_DEFAULT):
    return getDateTimeFromYearMonthDay(year * 10000 + 101, timezone)


################################################################################
def now():
    return arrow.now().timestamp


################################################################################
def nowMS():
    return int(round(time.time() * 1000))


################################################################################
def ms(timestamp):
    return timestamp * 1000


################################################################################
def s(timestamp):
    return int(timestamp / 1000)


################################################################################
def tomorrow(timezone, nbDays=1):
    return getBeginingOfNextDay(now(), timezone, nbDays)


################################################################################
def yersteday(timezone, nbDays=1):
    return getBeginingOfPreviousDay(now(), timezone, nbDays)


################################################################################
def formatTimestamp(timestamp, dateFormat="DD-MM-YYYY", timezone=sc.TIMEZONE_DEFAULT):
    return arrow.get(timestamp).to(timezone).format(dateFormat)


################################################################################
def formatTimestampDateTime(timestamp, timezone=sc.TIMEZONE_DEFAULT):
    return formatTimestamp(timestamp, "YYYY-MM-DD HH:mm", timezone)


################################################################################
def formatTimestampDate(timestamp, timezone=sc.TIMEZONE_DEFAULT):
    return formatTimestamp(timestamp, "YYYY-MM-DD", timezone)


################################################################################
def parseDate(dateString, dateFormat="DD-MM-YYYY", timezone=sc.TIMEZONE_DEFAULT):
    if not timezone: return arrow.get(dateString, dateFormat).timestamp
    else: return arrow.get(dateString, dateFormat).replace(tzinfo=dateutil.tz.gettz(timezone)).timestamp


################################################################################
def getEndOfDay(timestamp, timezone=sc.TIMEZONE_DEFAULT):
    return getArrowDate(timestamp, timezone).replace(hour=23, minute=59, second=59).timestamp


################################################################################
def getBeginingOfDay(timestamp, timezone=sc.TIMEZONE_DEFAULT):
    return getArrowDate(timestamp, timezone).replace(hour=0, minute=0, second=0).timestamp


################################################################################
def getBeginingOfMonth(timestamp, timezone):
    return getArrowDate(timestamp, timezone).replace(day=1, hour=0, minute=0, second=0).timestamp


################################################################################
def getBeginingOfNextMonth(timestamp, timezone, nbMonths=1):
    return getArrowDate(timestamp, timezone).replace(months=nbMonths, day=1, hour=0, minute=0, second=0).timestamp


################################################################################
def getEndOfMonth(timestamp, timezone):
    return getEndOfPreviousDay(getBeginingOfNextMonth(timestamp, timezone), timezone)


################################################################################
def getBeginingOfNextDay(timestamp, timezone=sc.TIMEZONE_DEFAULT, nbDays=1):
    return getArrowDate(timestamp, timezone).replace(days=nbDays, hour=0, minute=0, second=0).timestamp


################################################################################
def getBeginingOfPreviousDay(timestamp, timezone, nbDays=1):
    return getArrowDate(timestamp, timezone).replace(hour=0, minute=0, second=0, days=-nbDays).timestamp


################################################################################
def getEndOfPreviousDay(timestamp, timezone, nbDays=1):
    return getArrowDate(timestamp, timezone).replace(hour=23, minute=59, second=59, days=-nbDays).timestamp


################################################################################
def getBeginingOfYear(timestamp, timezone):
    return getArrowDate(timestamp, timezone).replace(month=1, day=1, hour=0, minute=0, second=0).timestamp


################################################################################
def getMonth(timestamp, timezone):
    return int(formatTimestamp(timestamp, "MM", timezone))


################################################################################
def getQuarter(timestamp, timezone):
    return (getMonth(timestamp, timezone) + 2) / 3


################################################################################
def getArrowDate(timestamp, timezone):
    return arrow.get(timestamp).to(timezone)


################################################################################
def isDayOpen(timestamp, timezone=sc.TIMEZONE_DEFAULT):
    weekDay = getArrowDate(timestamp, timezone).isoweekday()
    return weekDay != 6 and weekDay != 7


################################################################################
def getBeginingOfNextOpenDay(timestamp, timezone=sc.TIMEZONE_DEFAULT):
    nextDay = getBeginingOfNextDay(timestamp, timezone)
    while not isDayOpen(nextDay, timezone):
        nextDay = getBeginingOfNextDay(nextDay, timezone)
    return nextDay


################################################################################
def sleepMS(msSleep):
    time.sleep(msSleep * 1.0 / 1000.0)


################################################################################
def makeOffsetTime(hours, minutes):
    return hours * ONE_HOUR_IN_SEC + minutes * ONE_MINUTE_IN_SEC


################################################################################
def makeOffsetTime(hours, minutes, seconds):
    return hours * ONE_HOUR_IN_SEC + minutes * ONE_MINUTE_IN_SEC + seconds


################################################################################
def makeOffsetTime(date, timezone):
    return date - getBeginingOfDay(date, timezone)


################################################################################
def getMinuteWithinDay(date, timezone):
    return int(makeOffsetTime(date, timezone) / 60.0)


################################################################################
def getMinuteWithinDay(hour, minute):
    return int((hour * ONE_HOUR_IN_SEC + minute * ONE_MINUTE_IN_SEC) / 60.0)


################################################################################
def getMinuteWithinDayFromString(hourMinuteSecondString, sep=":"):
    if not hourMinuteSecondString: return 0
    bits = hourMinuteSecondString.split(sep)
    return getMinuteWithinDay(int(bits[0]), int(bits[1]))


################################################################################
def getMinuteWithinDayAndSecondsFromString(hourMinuteSecondString, sep=":"):
    if not hourMinuteSecondString: return 0
    bits = hourMinuteSecondString.split(sep)
    return getMinuteWithinDay(int(bits[0]), int(bits[1])), int(bits[2])


################################################################################
def getHourMinSecFromTimeInMinWithinDay(timeInMin, seconds=0, sep=":"):
    return str(int(timeInMin / 60)).zfill(2) + sep + str(int(timeInMin % 60)).zfill(2) + sep + str(seconds).zfill(2)


################################################################################
def formatMinuteOfDay(minuteOfDay, timezone):
    return formatTimestamp(getBeginingOfDay(0, timezone) + minuteOfDay * 60, "HH:mm", timezone)


################################################################################
def getOffsetTimeFromTimeString(hourMinSecString, sep=":"):
    bits = hourMinSecString.split(sep)
    return int(bits[0]) * ONE_HOUR_IN_SEC + int(bits[1]) * ONE_MINUTE_IN_SEC + int(bits[2])


# ################################################################################
# def getTradingDayIntradayIsSameDayParse(day, minuteInDay, closeInMinutes):
#     if minuteInDay > closeInMinutes: return getBeginingOfNextOpenDay(parseDate(str(day), "YYYYMMDD"))
#     else: return day
#
#
# ################################################################################
# def getTradingDayIntradayIsNextDayParse(day, minuteInDay, openInMinutes):
#     if minuteInDay > openInMinutes: return getBeginingOfNextOpenDay(parseDate(str(day), "YYYYMMDD"))
#     else: return day


################################################################################
def getTradingDay(day, minuteInDay, openInMinutes, closeInMinutes, allDaysIndexes, allDays, intradayIsNextDay=True):
    if not day in allDaysIndexes: return -1
    if not allDays[allDaysIndexes[day]]["open"]: return getNextOpenedDay(day, allDays, allDaysIndexes)

    if intradayIsNextDay:
        if minuteInDay > openInMinutes: return getNextOpenedDay(day, allDays, allDaysIndexes)
        else: return day
    else:
        if minuteInDay > closeInMinutes: return getNextOpenedDay(day, allDays, allDaysIndexes)
        else: return day


################################################################################
def isIntraday(day, minuteInDay, allDaysIndexes, allDays, openInMinutes, closeInMinutes):
    if not day in allDaysIndexes: return False
    if not allDays[allDaysIndexes[day]]["open"]: return False
    return openInMinutes <= minuteInDay < closeInMinutes


################################################################################
def getClosestNextOpenedDay(day, allDays, allDaysIndexes):
    return getNextOpenedDay(day, allDays, allDaysIndexes, 0)


################################################################################
def getNextOpenedDay(day, allDays, allDaysIndexes, offset=1):
    if not day in allDaysIndexes: return -1
    dayIndex = allDaysIndexes[day] + offset
    while dayIndex < len(allDays):
        if allDays[dayIndex]["open"]: return allDays[dayIndex]["day"]
        else: dayIndex += 1
    return -2


################################################################################
def getPreviousOpenedDay(day, allDays, allDaysIndexes, offset=1):
    if not day in allDaysIndexes: return -1
    dayIndex = allDaysIndexes[day] - offset
    while dayIndex >= 0:
        if allDays[dayIndex]["open"]: return allDays[dayIndex]["day"]
        dayIndex -= 1
    return -2


################################################################################
def getFirstDayOfYearMonth(yearMonth):
    return yearMonth * 100 + 1


################################################################################
def getYearFromYearMonthDay(yearMonthDay):
    return int(yearMonthDay / 10000)


################################################################################
def getYearFromYearMonth(yearMonth):
    return getYearFromYearMonthDay(yearMonth * 100 + 1)


################################################################################
def getMonthOnlyFromYearMonth(yearMonth):
    return getMonthOnlyFromYearMonthDay(yearMonth * 100 + 1)


################################################################################
def getMonthFromYearMonthDay(yearMonthDay):
    return int(yearMonthDay / 100)


################################################################################
def getMonthOnlyFromYearMonthDay(yearMonthDay):
    return getMonthFromYearMonthDay(yearMonthDay) % 100


################################################################################
def getDayOnlyFromYearMonthDay(yearMonthDay):
    return yearMonthDay % 100


################################################################################
def getNextMonth(yearMonth):
    if yearMonth % 100 % 12 == 0: return yearMonth + (100 - 11)
    else: return yearMonth + 1


################################################################################
def getMonthsList(monthFrom, monthTo):
    months = [monthFrom]
    while monthFrom < monthTo:
        monthFrom = getNextMonth(monthFrom)
        months.append(monthFrom)
    monthIndexes = {}
    for index in arange(len(months)): monthIndexes[months[index]] = index
    return months, monthIndexes


################################################################################
def getYearsList(yearFrom, yearTo):
    years = [yearFrom]
    while yearFrom < yearTo:
        yearFrom += 1
        years.append(yearFrom)
    yearsIndexes = {}
    for index in arange(len(years)): yearsIndexes[years[index]] = index
    return years, yearsIndexes


################################################################################
def getDaysList(dayFrom, dayTo):
    dayFrom = getDateTimeFromTimestamp(parseDate(str(dayFrom), "YYYYMMDD"))
    dayTo = getDateTimeFromTimestamp(parseDate(str(dayTo), "YYYYMMDD"))
    dateTimes, days, daysIndexes, naiveDateTimes = [], [], {}, []
    index = 0
    for currentDayArrow in arrow.Arrow.range("day", dayFrom, dayTo):
        currentDay = int(currentDayArrow.strftime('%Y%m%d'))
        days.append(currentDay)
        dateTimes.append(currentDayArrow.date())
        naiveDateTimes.append(currentDayArrow.naive)
        daysIndexes[currentDay] = index
        index += 1
    return days, daysIndexes, dateTimes, naiveDateTimes


################################################################################
def getDaysListInDays(dayFrom, dayTo, allDays, allDaysIndexes):
    if dayTo < allDays[0]["day"]: return []
    if dayFrom > allDays[-1]["day"]: return []
    if dayFrom < allDays[0]["day"]: dayStartIndex = 0
    else: dayStartIndex = allDaysIndexes[dayFrom]
    if dayTo > allDays[-1]["day"]: dayStopIndex = len(allDays)
    else: dayStopIndex = allDaysIndexes[dayTo]+1
    return allDays[dayStartIndex:dayStopIndex]["day"]


################################################################################
def paddMonthDatasAcrossYearsAndMonths(datasByMonth, months, emptyValue=0):
    datasSpread = {}
    yearFrom = getYearFromYearMonth(months[0])
    yearTo = getYearFromYearMonth(months[-1])
    years = getYearsList(yearFrom, yearTo)[0]
    for year in years: datasSpread[year] = [emptyValue for i in arange(12)]
    for index in arange(len(datasByMonth)):
        monthFromZero = getMonthOnlyFromYearMonth(months[index]) - 1
        datasSpread[getYearFromYearMonth(months[index])][monthFromZero] = datasByMonth[index]
    return datasSpread


################################################################################
def getTimeZoneHourOffsets(fromTimeZone, toTimeZone, dayFrom, dayTo):
    days, daysIndexes, dateTimes, naiveDateTimes = getDaysList(dayFrom, dayTo)
    fromTZ, toTZ = timezone(fromTimeZone), timezone(toTimeZone)
    offsetsOfDays = OrderedDict()
    for index in arange(len(naiveDateTimes)): offsetsOfDays[days[index]] = int((fromTZ.localize(naiveDateTimes[index]) - toTZ.localize(naiveDateTimes[index])).total_seconds() / 3600)
    return offsetsOfDays


################################################################################
def addHoursOffsetToYearMonthDayAndTimeInMins(yearMonthDay, timeInMins, offsetInHours):
    offsetInMins = offsetInHours * 60
    timePlusOffsetInMins = int(timeInMins + offsetInMins)
    if timePlusOffsetInMins > 1439:
        newDT = datetime.datetime(getYearFromYearMonthDay(yearMonthDay), getMonthOnlyFromYearMonthDay(yearMonthDay), getDayOnlyFromYearMonthDay(yearMonthDay)) + datetime.timedelta(1)
        return int(newDT.year * 1e4 + newDT.month * 1e2 + newDT.day), timePlusOffsetInMins - 1440
    elif timePlusOffsetInMins < 0:
        newDT = datetime.datetime(getYearFromYearMonthDay(yearMonthDay), getMonthOnlyFromYearMonthDay(yearMonthDay), getDayOnlyFromYearMonthDay(yearMonthDay)) - datetime.timedelta(1)
        return int(newDT.year * 1e4 + newDT.month * 1e2 + newDT.day), 1440 + timePlusOffsetInMins
    else: return yearMonthDay, timePlusOffsetInMins
