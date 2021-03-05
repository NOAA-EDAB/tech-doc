import datetime

import numpy

from cbibs.CbibsUtil import CbibsUtil


class CbibsBaseVo:

    # All base object have a time array
    def __init__(self, useSI=False):
        self.useSI = useSI
        self.measures = []
        self.step = 0
        self.KELVIN = -273.15


    # TODO, not really needed becuase measures are floats again
    def getTimeArray(self):
        timeArray = numpy.asarray(self.getMeasures())
        return timeArray[:, 0].astype(float)

    def getTimeArrayAsDates(self):
        # timeArray = numpy.asarray(self.measures)
        dateconv = numpy.vectorize(CbibsUtil.vectorDateChange)
        dTime = dateconv(self.getTimeArray())
        return dTime

    def getMeasures(self):
        x = numpy.asarray(self.measures).astype(float)
        # Sort 2D numpy array by first column
        sortedArr = x[x[:, 0].argsort()]
        return sortedArr

    def isEmpty(self):
        if len(self.measures) == 0:
            return True
        return False

    def createValue(self, value):
        if value is None:
            return numpy.nan
        if numpy.isnan(value):
            return numpy.nan

        return value
