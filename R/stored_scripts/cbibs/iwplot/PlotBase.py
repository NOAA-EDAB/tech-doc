import logging

import numpy
import pytz
from datetime import datetime, timezone

from cbibs.db.DBMetMgr import DBMetMgr
from cbibs.db.DBWaterQualityMgr import DBWaterQualityMgr
from cbibs.qc.QC import QC


class PlotBase:

    def vectorDateChange(self, X):
        """ Always use this function when changing date vectors """
        return pytz.UTC.localize(datetime.utcfromtimestamp(X))

    def getTimeArray(self, timeArray):
        """ Take a epoch time array. Sort it then convert into datetime objects """
        timeArray = numpy.asarray(sorted(timeArray)).astype(float)
        dateconv = numpy.vectorize(self.vectorDateChange)
        dTime = dateconv(timeArray)
        return dTime

    def findBucket(self, testDate):
        # Dates are 1 based and our arrays are 0 so subtract 1
        month = testDate.month - 1
        day = testDate.day - 1
        bucket = month * 31 + day
        return bucket

    # Factory pattern to get the right BDMgr
    def getDBMgr(self, groupName, stationName):
        # Put true if you want SI units
        mgr = {'MET': DBMetMgr(stationName, True),
               'WQ': DBWaterQualityMgr(stationName, True)
               }
        return mgr.get(groupName)

    def createClimateFromRaw(self, climate):
        # Run the math on each bucket. This will generate the climate information
        # The climate is a list of data arranged in the date buckets (372)
        dataArr = numpy.ones([4, 372]) * numpy.nan
        for x in climate:
            data = numpy.asarray(climate[x])
            if numpy.shape(data)[0] > 0:
                goodSus = (data[:, 1] == QC.GOOD.intValue) | (data[:, 1] == QC.SUSPECT.intValue)
                tdat = data[:, 0][goodSus]
                if len(tdat) == 0:
                    continue
                dataArr[0, x] = numpy.mean(tdat)
                dataArr[1, x] = (numpy.std(tdat) / (len(goodSus) ** 0.5)) * 1.96
                dataArr[2, x] = tdat.min()
                dataArr[3, x] = tdat.max()
        return dataArr

    def getYearlyDatasetClimate(self, sqlData, cbibsEnum):
        # Get the actual data as an array
        timeArray = sqlData.getTimeArray()
        measures = sqlData.getMeasures()
        dataArray = measures[:, cbibsEnum.dataIdx]
        qcArray = measures[:, cbibsEnum.qcIdx]
        climateBuckets = {x: [] for x in range(372)}

        # Setup the raw buckets, appending the measurements to each day
        for idx in range(0, len(timeArray)):
            rowDate = datetime.utcfromtimestamp(timeArray[idx]).replace(tzinfo=timezone.utc)
            bucket = self.findBucket(rowDate)
            if qcArray[idx] == QC.GOOD.intValue or qcArray[idx] == QC.SUSPECT.intValue:
                climateBuckets[bucket].append([dataArray[idx], qcArray[idx]])

        # Now flatten the data into avg/std/min/max
        yearlyClimate = self.createClimateFromRaw(climateBuckets)

        # Just return the mean data
        return yearlyClimate[0:]


    def getExtraData(self, station, beginDateEpoch, endDateEpoch, extraYears, enum, skipZero=False):
        # If there are more years specified, add those lines to the plot
        extraData = {}
        if extraYears is not None:
            for year in extraYears:
                beginX, endX = self.getYearDates(year, beginDateEpoch, endDateEpoch)
                cbibsDataVo = self.getTimeDBData(station, beginX, endX, enum)
                if cbibsDataVo.isEmpty():
                    # Can't graph without a reference year
                    return

                # Take the data from the database and make climate records from it
                extraYearData = self.getYearlyDatasetClimate(cbibsDataVo, enum)
                if extraYearData is not None:
                    if skipZero:
                        # The zeros throw off the charting so ignore them if flagged
                        extraYearData = numpy.ma.masked_equal(extraYearData, 0)
                    extraData[year] = extraYearData
        return extraData


    def createClimateData(self, station, beginDateEpoch, endDateEpoch, enum, minYear, maxYear):
        # First get all of the station data. Start with 07 and go till now
        years = numpy.asarray(range(minYear, maxYear + 1, 1))

        # Get all of the data from the database. Skip the time range that is called out
        climate, units = self.getClimateSql(station, years, beginDateEpoch, endDateEpoch, enum)
        climateData = self.createClimateFromRaw(climate)
        return climateData, units

    def getTimeDBData(self, station, beginDateEpoch, endDateEpoch, cbibsEnum):
        # Get the data over the time range and return the manager
        dbMgr = self.getDBMgr(cbibsEnum.group, station)
        cbibsDataVo = dbMgr.getGroupData(beginDateEpoch, endDateEpoch)
        return cbibsDataVo

    def getYearDates(self, year, beginDateEpoch, endDateEpoch):
        ''' When looking at a date range you need to get previous years data. Swap out the year and get older data
        If this spans a year then add to the query'''

        # Convert the begin date from epoch into datetime object
        bdate = pytz.UTC.localize(datetime.utcfromtimestamp(beginDateEpoch))
        edate = pytz.UTC.localize(datetime.utcfromtimestamp(endDateEpoch))  # .replace(tzinfo=timezone.utc)
        beginDate = bdate.replace(year=year)
        if bdate.year < edate.year:
            # If this spans a year, need to add one
            endDate = edate.replace(year=year + 1)
        else:
            endDate = edate.replace(year=year)

        beginDateEpoch = beginDate.timestamp()  # replace(tzinfo=timezone.utc).timestamp()
        endDateEpoch = endDate.timestamp()  # .replace(tzinfo=timezone.utc).timestamp()
        return beginDateEpoch, endDateEpoch

    def getClimateSql(self, station, years, beginDateEpoch, endDateEpoch, cbibsEnum):
        # Get the data from the table into a format of bucket[index] = all years for this bucket
        climateBuckets = {x: [] for x in range(372)}

        metMgr = self.getDBMgr(cbibsEnum.group, station)
        # Store the units outside of the loop
        units = None
        for year in years:
            # get the start and end dates for the query
            tempBDEpoch, tempEDEpoch = self.getYearDates(year, beginDateEpoch, endDateEpoch)

            # Do not include the current date span in the averaging
            if beginDateEpoch == tempBDEpoch:
                # this is the span I am looking at, skip it
                continue

            cbibsDataVo = metMgr.getGroupData(tempBDEpoch, tempEDEpoch)
            if cbibsDataVo is None:
                continue
            if units is None:
                units = cbibsDataVo.units[cbibsEnum.unitIdx]
            logging.debug(f"{datetime.utcfromtimestamp(tempBDEpoch)} to {datetime.utcfromtimestamp(tempEDEpoch)} ")
            if not cbibsDataVo.isEmpty():
                measurements = cbibsDataVo.getMeasures()

                for i in range(0, numpy.shape(measurements)[0] - 1):
                    rowDate = datetime.utcfromtimestamp(measurements[i, 0]).replace(tzinfo=timezone.utc)
                    bucket = self.findBucket(rowDate)
                    climateBuckets[bucket].append(
                        [measurements[i, cbibsEnum.dataIdx], measurements[i, cbibsEnum.qcIdx]])
        return climateBuckets, units
