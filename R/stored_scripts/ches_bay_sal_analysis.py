### chesapeake bay salinity 

import numpy
import enum

class QC(enum.Enum):
    UNKNOWN = 0, 'unknown'
    GOOD = 1, 'GOOD Value'
    NOT_EVAL = 2, 'Not Evaluated, Not Available, Unknown'
    SUSPECT = 3, 'Questionable or Suspect'
    BAD = 4, 'BAD'
    MISSING = 9, 'MISSING'

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, intValue, description):
        self.intValue = intValue
        self.description = description


def findTimeInterval(timeDataArray):
    # First, get the non-null data from the array. This should find the 'good' data
    good = numpy.isfinite(timeDataArray)
    times = timeDataArray[good]

    # I have a list of the good times now. Iterate until we have three in a row, that will be the interval
    counter = 0
    interval = 0  # This is the interval we are trying to find
    foundCounter = 0
    for t in times:
        if counter == 0:
            counter += 1
            continue
        tempT = times[counter] - times[counter - 1]
        # If this is the first comparison then continue
        if interval == 0:
            interval = tempT
            continue
        if interval == tempT:
            if foundCounter > 2:
                # Success, there have been 3 found
                return interval
            foundCounter += 1
        else:
            interval = tempT
        # Increment my count and look at the next difference
        counter += 1

    return interval


def missingValsAndRangeTest(inputArray, minVal, maxVal, logFlag=False):
    '''
    Generic function to test an array for missing values
    '''
    flag = numpy.ones(len(inputArray)) * QC.NOT_EVAL.intValue

    # TEST 1 (missing values)
    missing = numpy.isnan(inputArray)
    flag[missing] = QC.MISSING.intValue
    del missing
    bad = (inputArray < minVal) + (inputArray > maxVal)
    good = numpy.isfinite(inputArray)
    flag[good] = QC.GOOD.intValue
    flag[bad] = QC.BAD.intValue
    return flag


def rateOfChangeTest(timeArray, dataArray, ddlim, logFlag=False):
    good = numpy.isfinite(dataArray)
    L = sum(good)

    dd = numpy.diff(dataArray[good])
    dt = numpy.diff(timeArray[good]) * 86400
    dddt = numpy.true_divide(dd, dt)
    flag = numpy.ones([len(dataArray)])  # full length flag vector
    tflag = numpy.ones(L)  # limited length flag vector
    for n in range(2, len(dddt) - 1):
        if (dddt[n] == dddt[n - 1] == dddt[n - 2] == 0) or (numpy.abs(dddt[n]) >= ddlim[1]):
            tflag[n + 1] = 4
        # this catches data with a flat dddt two indeces and find dddt in the suspect range
        elif ((dddt[n] == dddt[n - 1] == 0 and dddt[n - 2] != 0) or (
                ddlim[0] <= numpy.abs(dddt[n]) < ddlim[1])):
            tflag[n + 1] = 3
        # this catches data with dddt == 0 repeated at most once and below the dd limits 
        elif 0 <= numpy.abs(dddt[n]) < ddlim[0]:
            tflag[n + 1] = 1
        # this should not catch anything, if twos are in the flag then there is a problem
        else:
            tflag[n + 1] = 2

    C, ia, ib = numpy.intersect1d(timeArray, timeArray[good], assume_unique=True, return_indices=True)
    flag[ia] = tflag
    return flag


def salinityQC(dTime, data):
    flag = numpy.ones([2, len(dTime)]) * 2

    minGrossRange = 0
    maxGrossRange = 40

    # TEST 1 (missing values and gross range)
    flag[0] = missingValsAndRangeTest(data, minGrossRange, maxGrossRange)

    # rate of change test
    # tempdat = salt
    ddlim = numpy.asarray([0.5, 1.]) * 1e-3
    flag[1, :] = rateOfChangeTest(dTime, data, ddlim)

    # create a flag array for this test
    stdFlag = numpy.ones(len(dTime)) * 2
    # Create copies of the data and get the max flags
    tempdat = data
    tempflag = numpy.amax(flag, axis=0)

    interval = findTimeInterval(dTime)
    bPerH = int(3600 / interval * 24)  # Account for zero based arrays
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
            if numpy.isnan(tempdat[tmp]) or tempdat[tmp] < lower_bad or tempdat[tmp] > upper_bad:
                stdFlag[tmp] = 4
            elif numpy.isnan(tempdat[tmp]) or tempdat[tmp] < lower_suspect or tempdat[tmp] > upper_suspect:
                stdFlag[ind] = 3
            else:
                stdFlag[tmp] = 1

    flag = numpy.vstack((flag, stdFlag))
    flag = numpy.amax(flag, axis=0)
    return flag
