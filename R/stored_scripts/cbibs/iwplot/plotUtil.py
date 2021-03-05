import logging
import sys
import traceback

import numpy
import pytz
from datetime import datetime, timezone, timedelta

from cbibs.CbibsConstants import CbibsConstants
from cbibs.CbibsUtil import CbibsUtil


class PlotUtil:

    def getStationColor(stationName):
        if stationName == 'AN':
            return 'green'
        if stationName == 'GR':
            return 'blue'
        if stationName == 'FL':
            return 'orange'
        # Didn't find the station, return default
        return 'black'

    @staticmethod
    def getMinMaxRange(varEnum, units=''):
        if varEnum == CbibsConstants.API_AIR_TEMPERATURE \
                or varEnum == CbibsConstants.API_WATER_TEMP:
            if units == 'F':
                return 0, 100
            else:
                return 0, 40
        if varEnum == CbibsConstants.API_DISSOLVED_OXYGEN:
            return 0, 20
        if varEnum == CbibsConstants.API_TURBIDITY:
            return 0, 110
        if varEnum == CbibsConstants.API_CHLOROPHYLL:
            return 0, 18
        if varEnum == CbibsConstants.API_WATER_SALINITY:
            return 0, 36
        if varEnum == CbibsConstants.API_RELATIVE_HUMIDITY:
            return -2, 102
        return None, None  # Just let the data define it

    @staticmethod
    def getDatesFromClimate(climate, dates):
        # climate is the avg /std/min/max data over a year in that order
        bucketDates = []
        avg = []

        # Create an array of days using the beginning and end date. This is a sorted list of epoch times
        firstDate = pytz.UTC.localize(datetime(dates[0].year, dates[0].month, dates[0].day, 0, 0, 0)).timestamp()
        lastDate = pytz.UTC.localize(datetime(dates[-1].year, dates[-1].month, dates[-1].day, 0, 0, 0)).timestamp()
        epochDates = numpy.arange(firstDate, lastDate, 86400)
        dateconv = numpy.vectorize(CbibsUtil.vectorDateChange)
        days = dateconv(epochDates)

        # Iterate over the dates and get the climate data at that location
        logging.debug("------------------getDatesFromClimate-----------------------------------------")
        logging.debug("Testing the dates")
        for date in days:
            logging.debug(date)
            bucket = PlotUtil.findBucket(date)
            if bucket is not None:
                # We may skip buckets like leap years
                bucketDates.append(date)
                avg.append(climate[0, bucket])
        return numpy.asarray(bucketDates), numpy.asarray(avg)

    @staticmethod
    def findDays(timeArray):
        newTimes = []
        for time in timeArray:
            if not time in newTimes:
                # When adding a time always use UTC
                # logging.debug("Date: ")
                newTimes.append(pytz.UTC.localize(datetime(time.year, time.month, time.day, 0, 0, 0)))
        return sorted(newTimes)

    @staticmethod
    def getDatesFromBuckets(climate, dates):
        ''' Create an array with the entire day '''
        bucketDates = []
        minData = []
        maxData = []
        minDataRaw = []
        maxDataRaw = []
        stdMin = []
        stdMax = []
        avgData = []
        # Iterate over the 372 dates
        days = PlotUtil.findDays(dates)
        for day in days:
            b = PlotUtil.findBucket(day)
            if b is not None:
                bucketDates.append(day)
                avgData.append(climate[0, b])
                minDataRaw.append(climate[2, b])
                minData.append(climate[2, b])
                maxDataRaw.append(climate[3, b])
                maxData.append(climate[3, b])
                stdMin.append(climate[0, b] - (climate[1, b]))
                stdMax.append(climate[0, b] + (climate[1, b]))
                bucketDates.append(day + timedelta(minutes=1439, seconds=59))  # datetime.timedelta(0,1439*100))
                minData.append(climate[2, b])
                maxData.append(climate[3, b])
                stdMin.append(climate[0, b] - (climate[1, b]))
                stdMax.append(climate[0, b] + (climate[1, b]))

        # Strip the last day out of the buckets, This will prevent the graph from extending that last day
        # in the shaded area which looks a little odd
        del bucketDates[-1]
        del minData[-1]
        del maxData[-1]
        del stdMin[-1]
        del stdMax[-1]
        # del avgData[-1]
        return numpy.asarray(bucketDates), numpy.asarray(minData), numpy.asarray(maxData), numpy.asarray(
            stdMin), numpy.asarray(stdMax), numpy.asarray(avgData), numpy.asarray(minDataRaw), numpy.asarray(maxDataRaw),

    @staticmethod
    def findDateFromBucket(bucket, testDate):
        ''' Use a bucket number to create a date. The buckets are 372 '''
        # Dates are 1 based and our arrays are 0 so subtract 1
        # Get the month
        month = int((bucket) / 31)
        day = (bucket - month * 31)
        bucket = month * 31 + day

        # print("Month {}, Day {}".format(month, day))
        try:
            cdate = datetime(testDate.year, month + 1, day + 1, 0, 0, 0, tzinfo=timezone.utc)
        except ValueError:
            traceback.print_exc(file=sys.stdout)
            return None
        else:
            return cdate

    def findBucket(testDate):
        ''' Use a datetime to find the right bucket for it '''
        # Dates are 1 based and our arrays are 0 so subtract 1
        month = testDate.month - 1
        day = testDate.day - 1
        bucket = month * 31 + day
        if month == 2 and day == 29:
            # Skip leap years
            return None
        return bucket
