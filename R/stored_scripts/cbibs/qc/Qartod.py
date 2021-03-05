# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 08:24:33 2019
@author: byron

!Psuedocode time!
a. this is a function !! that takes inputs of data (wind), time, station. 
The size and shape of data and time must be identical.
b. use station to make station specific quality determinations ...
for example, if a sensor is known to be faulty for a period, specifically
assign quality flags to those data. 
c. apply quality algorithm to determine good(1), not evaluated(2), suspect(3), bad(4), and missing(9)
d. output vector of quality flags that is the length of data (input)  
"""
import numpy
import traceback
import sys
from cbibs.qc.QC import QC
from cbibs.qc.CbibsLocationsMetadata import CbibsLocationsMetadata
import logging

# Remove this import after cleaning up dates
from matplotlib import dates


# import gc


class Qartod():

    @staticmethod
    def checkTwoArrays(arrayOne, arrayTwo, logFlag=False):
        '''
        Compare the length of two arrays
        '''
        L0 = len(arrayOne)
        L1 = len(arrayTwo)
        if (L0 == L1):
            if logFlag:
                logging.debug('size check passed, continuing')
            return True
        else:
            print("*" * 60)
            print("Warning: Size check failed, aborting")
            print("*" * 60)
            return False

    def checkThreeArrays(arrayOne, arrayTwo, arrayThree, logFlag=False):
        '''
        Compare the length of three arrays
        '''
        L0 = len(arrayOne)
        L1 = len(arrayTwo)
        L2 = len(arrayThree)
        if (L0 == L1 == L2):
            if logFlag:
                logging.debug('size check passed, continuing')
            return True
        else:
            print("*" * 60)
            print("Warning: Size check failed, aborting {},{},{}".format(L0, L1, L2))
            print("*" * 60)
            return False

    @staticmethod
    def lengthTest(arrayOne, arrayTwo, arrayThree=None, logFlag=False):
        if arrayThree is None:
            return Qartod.checkTwoArrays(arrayOne, arrayTwo, logFlag)
        return Qartod.checkThreeArrays(arrayOne, arrayTwo, arrayThree, logFlag)

    @staticmethod
    def missingValsAndRangeTest(inputArray, minVal, maxVal, logFlag=False):
        '''
        Generic function to test an array for missing values
        '''
        flag = numpy.ones(len(inputArray)) * QC.NOT_EVAL.intValue

        # TEST 1 (missing values)
        # logging.debug(" -- Data Types ---")
        # logging.debug(inputArray.dtype)
        missing = numpy.isnan(inputArray)
        flag[missing] = QC.MISSING.intValue
        if logFlag:
            logging.debug("Missing Test Flags")
            logging.debug(flag)
        del (missing)

        bad = (inputArray < minVal) + (inputArray > maxVal)
        good = numpy.isfinite(inputArray)

        flag[good] = QC.GOOD.intValue
        flag[bad] = QC.BAD.intValue
        if logFlag:
            logging.debug("Gross Range Test Flags")
            logging.debug(flag)

        return flag


    @staticmethod
    def rateOfChangeTest(timeArray, dataArray, ddlim, logFlag=False):

        good = numpy.isfinite(dataArray)
        # L = sum(good)
        dd = numpy.diff(dataArray[good])
        dt = numpy.diff(timeArray[good]) * 86400
        dddt = numpy.true_divide(dd, dt)
        flag = numpy.ones([len(dataArray)])  # full length flag vector
        tflag = numpy.ones(len(dataArray))  #  Not L limited length flag vector
        for n in range(2, len(dddt) - 1):
            # this catched bad if the dddt is flat for three indeces, or if dddt \
            # is greater than the bad threshold
            if ((dddt[n] == dddt[n - 1] == dddt[n - 2] == 0) or (numpy.abs(dddt[n]) >= ddlim[1])):
                tflag[n + 1] = 4
            # this catches data with a flat dddt two indeces and find dddt in the suspect range
            elif ((dddt[n] == dddt[n - 1] == 0 and dddt[n - 2] != 0) or (
                    numpy.abs(dddt[n]) >= ddlim[0] and numpy.abs(dddt[n]) < ddlim[1])):
                tflag[n + 1] = 3
            # this catches data with dddt == 0 repeated at most once and below the dd limits 
            elif (numpy.abs(dddt[n]) >= 0 and numpy.abs(dddt[n]) < ddlim[0]):
                tflag[n + 1] = 1
            # this should not catch anything, if twos are in the flag then there is a problem
            else:
                tflag[n + 1] = 2

        # reindexing example code from matrixizer        
        # C,ia,ib = numpy.intersect1d(Utime,temp_time,assume_unique=True,return_indices=True)
        # fdat[ia,m] = temp_dat
        # elev[ia,m] = temp_elev
        #C, ia, ib = numpy.intersect1d(timeArray, timeArray[good], assume_unique=True, return_indices=True)
        #flag[ia] = tflag

        if logFlag:
            logging.debug("Rate of change test flags")
            logging.debug(flag)

        return tflag

    @staticmethod
    def windsQC(station, dTime, wspd, wdir, logFlag=False):
        if logFlag:
            logging.debug("=-=-=-=-=-=-=-=- WINDS QC -=-=-=-=-=-=-=-=")
            logging.debug("Station[" + station)
        # wspd = wind speed, wdir = wind direction (from),
        # dtime is the time at a data point, station is the station designator i.e 'FL'
        # error checking
        if not Qartod.lengthTest(dTime, wspd, wdir):
            return False

        numberOfTests = 4
        secondsInADay = 86400
        windSpeedMin = 0
        windSpeedMax = 32
        windSpeedWeakSignalBad = 0.1
        windSpeedWeakSignalSuspect = 0.4
        windSpeedMinDeg = 0
        windSpeedMaxDeg = 360

        # Initialize a 2D flag array [the number of tests and not eval]
        flag = numpy.ones([numberOfTests, len(dTime)]) * QC.NOT_EVAL.intValue
        logging.debug("Initial flag array. All not eval")
        logging.debug(flag)

        # TEST 1 (missing values and gross range)
        flag[0] = Qartod.missingValsAndRangeTest(wspd, windSpeedMin, windSpeedMax)

        # weak signal to noise test
        bad = (wspd < windSpeedWeakSignalBad)
        suspect = (wspd >= windSpeedWeakSignalBad) * (wspd <= windSpeedWeakSignalSuspect)
        good = (wspd > windSpeedWeakSignalSuspect)
        flag[1, good] = QC.GOOD.intValue
        flag[1, bad] = QC.BAD.intValue
        flag[1, suspect] = QC.SUSPECT.intValue
        del [bad, suspect]

        logging.debug("Weak signal to noise" +
                      str(windSpeedWeakSignalSuspect) + "-" + str(windSpeedWeakSignalBad))
        logging.debug(flag[1])

        # rate of change test
        ddlim = numpy.asarray([2., 5.]) * 1e-3
        flag[2] = Qartod.rateOfChangeTest(dTime, wspd, ddlim)
        logging.debug("rate of change  test Flags")
        logging.debug(flag[2])

        # test validity of wind direction
        bad = (wdir < windSpeedMinDeg) + (wdir > windSpeedMaxDeg)
        good = (wdir >= windSpeedMinDeg) + (wdir >= windSpeedMaxDeg)
        flag[3, good] = QC.GOOD.intValue
        flag[3, bad] = QC.BAD.intValue
        logging.debug("wind direction  test Flags")
        logging.debug(flag[3])

        flag = numpy.amax(flag, axis=0)
        logging.debug("Final Flags")
        logging.debug(flag)
        return flag

    @staticmethod
    def airTemperatureQC(station, dTime, data, timeStep, units='c', logFlag=False):
        logging.debug("=-=-=-=-=-=-=-=- AIR TEMPERTURE QC -=-=-=-=-=-=-=-=")
        logging.debug("Station[" + station + "] Units[" + units + "]")
        data = data.astype(float)
        dTime = dTime.astype(float)
        numpy.warnings.filterwarnings('ignore')
        # secondsInADay = 86400
        numberOfTests = 4

        # Min/Max temp values in celsius
        minTemp = -17
        maxTemp = 44
        staticHigh = 20
        staticLow = 15
        # identify areas varying in extremis from climatological norms
        StaClimLim = {'N': [14, 14, 0.7], 'FL': [16, 13, -1.35], 'J': [14.5, 17, 0.7], 'YS': [14.5, 13, 0.7],
                      'SR': [13, 16, 0.7], 'PL': [14, 14, 0.7], 'GR': [14.5, 13, 0.7], 'AN': [14.5, 13, 0.7],
                      'SN': [14.5, 13, 0.7], 'UP': [14.5, 13, 0.7], 'S': [14.5, 13, 0.7]}
        if units.lower() == "k":
            # Adjust for Kelvin
            # Min/Max temp values in celsius
            kelvin = 273.15
            minTemp = -17 + kelvin  # K which is -17 C
            maxTemp = 44 + kelvin  # 317.15  # K which is 44 C
            staticHigh = 20 + kelvin
            staticLow = 15 + kelvin
            # identify areas varying in extremis from climatological norms
            StaClimLim = {'N': [14 + kelvin, 14 + kelvin, 0.7],
                          'FL': [16 + kelvin, 13 + kelvin, -1.35], 'J': [14.5 + kelvin, 17 + kelvin, 0.7],
                          'YS': [14.5 + kelvin, 13 + kelvin, 0.7],
                          'SR': [13 + kelvin, 16 + kelvin, 0.7], 'PL': [14 + kelvin, 14 + kelvin, 0.7],
                          'GR': [14.5 + kelvin, 13 + kelvin, 0.7], 'AN': [14.5 + kelvin, 13 + kelvin, 0.7],
                          'SN': [14.5 + kelvin, 13 + kelvin, 0.7], 'UP': [14.5 + kelvin, 13 + kelvin, 0.7],
                          'S': [14.5 + kelvin, 13 + kelvin, 0.7]}
        try:
            if not Qartod.lengthTest(dTime, data):
                return False

            # Initialize a 2D flag array [the number of tests and not eval]
            flag = numpy.ones([numberOfTests, len(dTime)]) * QC.NOT_EVAL.intValue
            if logFlag:
                logging.debug("Initial flag settings")
                logging.debug(flag)

            # TEST 1 (missing values and gross range)
            flag[0] = Qartod.missingValsAndRangeTest(data, minTemp, maxTemp)

            # TEST 2 rate of change
            ddlim = numpy.asarray([3., 5.]) * 1e-3
            flag[1] = Qartod.rateOfChangeTest(dTime, data, ddlim)

            # "bad patch" removal
            # Standard Deviations Limits Dictionary
            # Variations depend on physical locations
            SDLimDict = {'FL': [5, 6], 'N': [5, 6], 'J': [5, 6], 'YS': [5, 6], 'SR': [3, 4], 'PL': [
                6, 7], 'GR': [5, 6], 'AN': [6, 7], 'SN': [7, 8], 'UP': [7, 8], 'S': [5, 6]}
            temp_flag = numpy.amax(flag[0:2, :], axis=0)

            # tv = numpy.arange(numpy.min(dTime), numpy.max(dTime), (1/144))
            # Use seconds instead of days (600)
            # tv = numpy.arange(numpy.min(dTime), numpy.max(dTime), (600))

            tv = dTime
            # ind = numpy.where(temp_flag == QC.GOOD.intValue)[0]
            ind = numpy.where(temp_flag == QC.GOOD.intValue, True, False)
            temp_temp = data[ind]
            temp_time = dTime[ind]

            # Only run this test if we don't have all fails from above test
            if len(temp_temp) != 0 and len(temp_time) != 0:
                if logFlag:
                    Qartod.printFlags(dTime, flag)

                flag[2, :] = Qartod.badPatchRemoval(station, dTime, data, flag, timeStep)
                if logFlag:
                    Qartod.printFlags(dTime, flag)

                ofst = StaClimLim[station][0]
                ampl = StaClimLim[station][1]
                phas = StaClimLim[station][2]
                climate = ofst + ampl * numpy.sin(dTime * (2 * numpy.pi) * (1 / 365) + phas * numpy.pi)
                bad = (numpy.abs(climate - data) >= staticHigh)
                suspect = (numpy.abs(climate - data) >= staticLow) * \
                          (numpy.abs(climate - data) < staticHigh)
                good = (numpy.abs(climate - data) < staticLow)
                flag[3, bad] = QC.BAD.intValue
                flag[3, suspect] = QC.SUSPECT.intValue
                flag[3, good] = QC.GOOD.intValue
                if logFlag:
                    logging.debug("Climate  test Flags")
                    logging.debug(flag[3])

            # Print out the flag array to find the failures
            if logFlag:
                Qartod.printFlags(dTime, flag)

            # Flatten the test results returning a 1D array
            flag = numpy.amax(flag, axis=0)


        except:
            print("Exception in user code (QCTempFlag) :")
            print("-" * 60)
            traceback.print_exc(file=sys.stdout)
            print("-" * 60)
            raise
        return flag

    @staticmethod
    def badPatchRemoval(station, dTime, data, flag, timeStep):
        # "bad patch" removal
        SDLimDict = {'FL': [5, 6], 'N': [5, 6], 'J': [5, 6], 'YS': [5, 6], 'SR': [3, 4], 'PL': [6, 7], 'GR': [5, 6],
                     'AN': [6, 7], 'SN': [7, 8], 'UP': [7, 8], 'S': [5, 6]}
        SDLim = SDLimDict[station]
        # Get the max flag from the first three tests
        data_flag = numpy.amax(flag[0:2, :], axis=0)

        # The data is normalized over the time range. Get the interpolated 'good data'
        ind = numpy.where(data_flag == 1)[0]
        datai = numpy.interp(data, dTime[ind], data[ind])
        data_flagi = numpy.ones(len(dTime))

        # Step through each day. Take the start time, and add X minutes
        # timeStemp % 3600 * 24* 60
        x = 0
        if timeStep == 360:  # 6 min samples
            x = 10 * 24   # 240
        elif timeStep == 600:  # 10 min samples
            x = 6 * 24   # 144
        elif timeStep == 3600:
            x = 24  # 24

        numberOfDays = int(numpy.floor((dTime[-1] - dTime[0]) / (60*60*24)))
        for dayIndex in range(0,numberOfDays):
            # the 24 hour indices will be
            ind = numpy.arange(0, 143) + dayIndex * x
            dataSD = numpy.std(datai[ind])
            # Zs = (datai[ind]-numpy.mean(datai[ind]))/dataSD
            if dataSD > SDLim[1]:
                data_flagi[ind] = 4
            elif (dataSD > SDLim[0] and dataSD < SDLim[1]):
                data_flagi[ind] = 3
            else:
                data_flagi[ind] = 1

        # flag[2, :] = numpy.ceil(numpy.interp(dTime, tv, data_flagi))
        return numpy.ceil(numpy.interp(dTime, data, data_flagi))

    @staticmethod
    def printFlags(dTime, flag):
        logging.debug("*-" * 45)
        logging.debug("Climate  test Flags")
        for x in range(0, len(dTime) - 1):
            logging.debug(f"Time: {dTime[x]} {flag[0, x]}, {flag[1, x]}, {flag[2, x]}, {flag[3, x]}")

    @staticmethod
    def locationQC(station, dTime, lat, lon, logFlag=False):
        if not Qartod.lengthTest(dTime, lon, lat):
            return False
        if logFlag:
            logging.debug("=-=-=-=-=-=-=-=- locationQC QC -=-=-=-=-=-=-=-=")
            logging.debug("Station[" + station + "]")

        # Get the user configured lat/lon for the station
        # for aDateTime in dTime:
        #    lat, lon = CbibsLocationsMetadata.getLatLon(station, aDateTime)

        dataLength = len(dTime)
        flag = numpy.ones([len(dTime)]) * 2
        if logFlag:
            logging.debug("Initial flag array. All not eval")
            logging.debug(flag)

        dist = numpy.ones([dataLength]) * numpy.nan
        for n in range(0, dataLength):
            latt, lont = CbibsLocationsMetadata.getInstance().getLatLon(station, dTime[n])
            distx = (lon[n] - lont) * 111. * numpy.cos(lat[n] * (numpy.pi / 180.))
            disty = (lat[n] - latt) * 111.
            dist[n] = (distx ** 2 + disty ** 2) ** (0.5)

        missing = numpy.isnan(dist)
        bad = dist >= 1
        suspect = (dist > 0.2) * (dist < 1)
        good = dist <= 0.2

        flag[missing] = 9
        flag[bad] = 4
        flag[suspect] = 3
        flag[good] = 1

        if logFlag:
            logging.debug("Finished flag array. All not eval")
            logging.debug(flag)
        return flag

    @staticmethod
    def relativeHumidityQC(station, dTime, data, logFlag=False):
        if not Qartod.lengthTest(dTime, data):
            return False
        flag = numpy.ones([2, len(dTime)]) * 2

        if logFlag:
            logging.debug("relativeHumidityQC Initial flag array. All not eval")
            logging.debug(flag)

        minRelH = 20
        maxRelH = 100

        # TEST 1 (missing values and gross range)
        flag[0] = Qartod.missingValsAndRangeTest(data, minRelH, maxRelH)
        # Qartod.grossRangeTest(flag, 0, data, minRelH, maxRelH)

        # logging.debug("relativeHumidityQC")
        # logging.debug(flag)

        # TEST 2 rate of change
        ddlim = numpy.asarray([3., 5.]) * 1e-3
        flag[1, :] = Qartod.rateOfChangeTest(dTime, data, ddlim)

        if logFlag:
            logging.debug("Initial flag array. All not eval")
            logging.debug(flag)


        flag = numpy.amax(flag, axis=0)
        return flag

    @staticmethod
    def airPressureQC(station, dTime, data,logFlag=False):
        if not Qartod.lengthTest(dTime, data):
            return False

        flag = numpy.ones([2, len(dTime)]) * 2

        minGrossRange = 950
        maxGrossRange = 1050

        # TEST 1 (missing values and gross range)
        flag[0] = Qartod.missingValsAndRangeTest(data, minGrossRange, maxGrossRange)

        # TEST 2 rate of change
        ddlim = numpy.asarray([3., 5.]) * 1e-3
        flag[1, :] = Qartod.rateOfChangeTest(dTime, data, ddlim)

        flag = numpy.amax(flag, axis=0)
        return flag

    @staticmethod
    def salinityQC(station, dTime, data,stepInterval):
        if not Qartod.lengthTest(dTime, data):
            return False

        flag = numpy.ones([2, len(dTime)]) * 2

        minGrossRange = 0
        maxGrossRange = 40

        # TEST 1 (missing values and gross range)
        flag[0] = Qartod.missingValsAndRangeTest(data, minGrossRange, maxGrossRange)

        # rate of change test
        # tempdat = salt
        ddlim = numpy.asarray([0.5, 1.]) * 1e-3
        flag[1, :] = Qartod.rateOfChangeTest(dTime, data, ddlim)

        # One day is 1440 seconds
        # Get the number of time slots. 6 min data is 360 seconds, hourly data is 3600 seconds
        # Start with the starting time and then increment be second interval

        # create a flag array for this test
        stdFlag = numpy.ones(len(dTime)) * 2
        # Create copies of the data and get the max flags
        tempdat = data
        tempflag = numpy.amax(flag, axis=0)

        ''' 
        Calculate the number of buckets per hour
           3600/3600 * 24  = 24  - Hourly
           3600/600 * 24 = 144  - 10 Min
           3600/360 * 24 = 240   - 6 min 
        '''
        # TODO Use the stop the we have found once
        # interval = Qartod.findTimeInterval(dTime)
        # TODO Is this right for a stoep??
        bPerH = int(3600 / stepInterval * 24)  # Account for zero based arrays
        bucketCount = int(len(dTime) / bPerH)

        # Iterate over the buckets
        for bucket in range(bucketCount):
            ind = numpy.asarray(range(bucket * bPerH, bucket * bPerH + bPerH, 1))

            # get the standard deviation over the day
            data = tempdat[ind[tempflag[ind] == 1]]
            data_mean, data_std = numpy.mean(data), numpy.std(data)

            # identify outliers
            cut_off_bad = data_std * 3.5
            lower_bad, upper_bad = data_mean - cut_off_bad, data_mean + cut_off_bad
            cut_off_suspect = data_std * 3
            lower_suspect, upper_suspect = data_mean - cut_off_suspect, data_mean + cut_off_suspect
            for tmp in ind:
                if (numpy.isnan(tempdat[tmp]) or tempdat[tmp] < lower_bad or tempdat[tmp] > upper_bad):
                    stdFlag[tmp] = 4
                elif (numpy.isnan(tempdat[tmp]) or tempdat[tmp] < lower_suspect or tempdat[tmp] > upper_suspect):
                    stdFlag[ind] = 3
                else:
                    stdFlag[tmp] = 1

        flag = numpy.vstack((flag, stdFlag))
        flag = numpy.amax(flag, axis=0)
        # flag = numpy.amax(stdFlag, axis=0)
        return flag

    @staticmethod
    def seaWaterTempQC(station, dTime, data):
        if not Qartod.lengthTest(dTime, data):
            return False

        flag = numpy.ones([2, len(dTime)]) * 2

        minGrossRange = -2
        maxGrossRange = 40

        # TEST 1 (missing values and gross range)
        flag[0] = Qartod.missingValsAndRangeTest(data, minGrossRange, maxGrossRange)

        # TEST 2 rate of change
        ddlim = numpy.asarray([3., 5.]) * 1e-3
        flag[1, :] = Qartod.rateOfChangeTest(dTime, data, ddlim)

        flag = numpy.amax(flag, axis=0)
        return flag

    def chlorophyllQC(station, dTime, data):
        if not Qartod.lengthTest(dTime, data):
            return False

        flag = numpy.ones([2, len(dTime)]) * 2

        minGrossRange = 0
        maxGrossRange = 100

        # TEST 1 (missing values and gross range)
        flag[0] = Qartod.missingValsAndRangeTest(data, minGrossRange, maxGrossRange)

        # TEST 2 rate of change
        ddlim = numpy.asarray([3., 5.]) * 1e-3
        flag[1, :] = Qartod.rateOfChangeTest(dTime, data, ddlim)

        flag = numpy.amax(flag, axis=0)
        return flag

    @staticmethod
    def disolvedOxygenQC(station, dTime, data):
        if not Qartod.lengthTest(dTime, data):
            return False

        flag = numpy.ones([2, len(dTime)]) * 2
        minGrossRange = 0
        maxGrossRange = 100

        # TEST 1 (missing values and gross range)
        flag[0] = Qartod.missingValsAndRangeTest(data, minGrossRange, maxGrossRange)

        # TEST 2 rate of change
        ddlim = numpy.asarray([3., 5.]) * 1e-3
        flag[1, :] = Qartod.rateOfChangeTest(dTime, data, ddlim)

        flag = numpy.amax(flag, axis=0)
        return flag

    @staticmethod
    def turbidityQC(station, dTime, data):
        if not Qartod.lengthTest(dTime, data):
            return False

        flag = numpy.ones([2, len(dTime)]) * 2

        minGrossRange = 0
        maxGrossRange = 100

        # TEST 1 (missing values and gross range)
        flag[0] = Qartod.missingValsAndRangeTest(data, minGrossRange, maxGrossRange)

        # TEST 2 rate of change
        ddlim = numpy.asarray([3., 5.]) * 1e-3
        flag[1, :] = Qartod.rateOfChangeTest(dTime, data, ddlim)

        flag = numpy.amax(flag, axis=0)
        return flag

    @staticmethod
    def QCWaveFlag(station, dTime, data, logFlag=False):
        if not Qartod.lengthTest(dTime, data):
            return False

        flag = numpy.ones([2, len(dTime)]) * 2
        if logFlag:
            logging.debug("Initial flag array. All not eval")
            logging.debug(flag)

        minGrossRange = 0
        maxGrossRange = 5

        # TEST 1 (missing values and gross range)
        flag[0] = Qartod.missingValsAndRangeTest(data, minGrossRange, maxGrossRange)
        if logFlag:
            logging.debug("TEST 1")
            logging.debug(flag)

        # TODO THIS TEST HAS A SUSPECT VALUE?
        # gross range and missing value test
        '''
        missing = numpy.isnan(data)
        bad = (data < 0)+(data >= 5)
        suspect = (data > 3)*(data < 5)
        good = numpy.isfinite(data)
        flag[0, missing] = 9
        flag[0, good] = 1
        flag[0, suspect] = 3
        flag[0, bad] = 4
        '''
        # TEST 2 rate of change
        ddlim = numpy.asarray([2., 3.5]) * 1e-4
        flag[1, :] = Qartod.rateOfChangeTest(dTime, data, ddlim)
        if logFlag:
            logging.debug("TEST 2")
            logging.debug(flag)
        '''
        dddat = numpy.interp(dTime, dTime[good], data[good])
        dd = numpy.diff(dddat)
        dt = numpy.diff(dTime)*86400
        dddt = numpy.true_divide(dd, dt)
        ddlim = numpy.asarray([2., 3.5])*1e-4
        bad = numpy.where((dddt == 0)+(numpy.abs(dddt) >= ddlim[1]))[0]
        suspect = numpy.where(
            (numpy.abs(dddt) > ddlim[0])*(numpy.abs(dddt) <= ddlim[1]))[0]
        good = numpy.where(numpy.abs(dddt) < ddlim[0])[0]

        flag[1, 0] = 1  # forward difference does not reach index 0
        flag[1, good+1] = 1
        flag[1, suspect+1] = 3
        flag[1, bad+1] = 4
        '''

        flag = numpy.amax(flag, axis=0)
        if logFlag:
            logging.debug("Final Flags")
            logging.debug(flag)
        return flag

    @staticmethod
    def currentsQC(station, dTime, data, logFlag=False):
        numOfTests = 2  # Change to three when the last test is implemented TODO
        # Test the length of data arrays
        if not Qartod.lengthTest(dTime, data):
            return False

        # Initialize empty array 
        flag = numpy.ones([numOfTests, len(dTime)]) * QC.NOT_EVAL.intValue

        # TEST 1 (missing values and gross range)
        minGrossRange = -2000
        maxGrossRange = 2000
        flag[0] = Qartod.missingValsAndRangeTest(data, minGrossRange, maxGrossRange)
        if logFlag:
            logging.debug("TEST 1")
            logging.debug(flag)
        '''
        Oring Code
        # gross range and missing value test
        missing = numpy.isnan(data)
        bad = (numpy.abs(data)>2000)
        good = numpy.isfinite(data)*(numpy.abs(data)<=2000)
        flag[0,missing] = 9
        flag[0,good] = 1
        flag[0,bad] = 4
        '''

        # TEST 2 rate of change
        ddlim = numpy.asarray([1.5, 2.]) * 1e-4
        flag[1, :] = Qartod.rateOfChangeTest(dTime, data, ddlim)
        if logFlag:
            logging.debug("TEST 2")
            logging.debug(flag)

        '''
        Oring Code
        #rate of change test
        ddlim = numpy.asarray([1.5,2.])*1e-4
        tflag = ROCTest(data,dTime,ddlim)
        flag[1,:] = tflag
        '''

        '''
        TODO What is this test?
        tflag = dVarTest(data,dTime,[0.5,1]*1e4,0)
        flag[2,:] = tflag
        '''

        # Flatten the flag array and return
        flag = numpy.amax(flag, axis=0)
        if logFlag:
            logging.debug("Final Flags")
            logging.debug(flag)
        return flag

    # @staticmethod
    # def findTimeInterval(timeDataArray):
    #     # First, get the non-null data from the array. This should find the 'good' data
    #     good = numpy.isfinite(timeDataArray)
    #     times = timeDataArray[good]
    #
    #     # I have a list of the good times now. Iterate until we have three in a row, that will be the interval
    #     counter = 0
    #     interval = 0  # This is the interval we are trying to find
    #     foundCounter = 0
    #     for t in times:
    #         if counter == 0:
    #             counter += 1
    #             continue
    #         tempT = times[counter] - times[counter - 1]
    #         # If this is the first comparison then continue
    #         if interval == 0:
    #             interval = tempT
    #             continue
    #         if interval == tempT:
    #             if foundCounter > 2:
    #                 # Success, there have been 3 found
    #                 return interval
    #             foundCounter += 1
    #         else:
    #             interval = tempT
    #         # Increment my count and look at the next difference
    #         counter += 1
    #
    #     return interval
