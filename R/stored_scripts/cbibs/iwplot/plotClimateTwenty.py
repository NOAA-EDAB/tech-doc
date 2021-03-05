import numpy

from cbibs.iwplot.PlotBase import PlotBase
from cbibs.iwplot.PlottingDataVO import PlottingDataVO


class PlotClimateTwenty(PlotBase):

    def debugClimateData(self,climateData):
        # This is an array 4 x 374
        ''' Create an array with the entire day '''
        bucketDates = []
        minData = []
        maxData = []
        stdMin = []
        stdMax = []
        avgData = []

        # # Iterate over the 372 dates
        # days = PlotUtil.findDays(dates)
        # for day in days:
        #     b = PlotUtil.findBucket(day)
        #     if b is not None:
        #         bucketDates.append(day)
        #         avgData.append(climate[0, b])
        #         minData.append(climate[2, b])
        #         maxData.append(climate[3, b])
        #         stdMin.append(climate[0, b] - (climate[1, b]))
        #         stdMax.append(climate[0, b] + (climate[1, b]))
        #         bucketDates.append(day + timedelta(minutes=1439, seconds=59))  # datetime.timedelta(0,1439*100))
        #         minData.append(climate[2, b])
        #         maxData.append(climate[3, b])
        #         stdMin.append(climate[0, b] - (climate[1, b]))
        #         stdMax.append(climate[0, b] + (climate[1, b]))
        #
        #     # Strip the last day out of the buckets, This will prevent the graph from extending that last day
        #     # in the shaded area which looks a little odd
        #     del bucketDates[-1]
        #     del minData[-1]
        #     del maxData[-1]
        #     del stdMin[-1]
        #     del stdMax[-1]
        #     # del avgData[-1]
        #     return numpy.asarray(bucketDates), numpy.asarray(minData), numpy.asarray(maxData), numpy.asarray(
        #         stdMin), numpy.asarray(stdMax), numpy.asarray(avgData)
    def createPlottingDataVO(self, station, beginDateEpoch, endDateEpoch, extraYears, varEnum, minYear, maxYear,
                             skipZero=False):
        climateData, units = self.createClimateData(station, beginDateEpoch, endDateEpoch, varEnum, minYear, maxYear)

        # I need a reference dataset
        cbibsDataVo = self.getTimeDBData(station, beginDateEpoch, endDateEpoch, varEnum)
        if cbibsDataVo.isEmpty():
            # Can't graph without a reference year
            return

        # Take the data from the database and make climate records from it
        referenceData = self.getYearlyDatasetClimate(cbibsDataVo, varEnum)
        if skipZero:
            # The zeros throw off the charting so ignore them if flagged
            referenceData = numpy.ma.masked_equal(referenceData, 0)
        # Can add extra reference data if any years are sent in
        extraData = self.getExtraData(station, beginDateEpoch, endDateEpoch, extraYears, varEnum)
        plottingDataVO = PlottingDataVO(station, cbibsDataVo.getTimeArray(), referenceData, climateData, extraData)

        # Set the units that we get from the database
        plottingDataVO.setUnits(units)

        return plottingDataVO
