import logging
import numpy


class QCMgrBase(object):

    minRecordCount = 10

    def getStep(self, times):
        if len(times) < 6:
            return 0
        # Look at 100 records. If you get a difference at least 6 times then assume that is the frequency
        maxCount = 100 if 100 < len(times) else len(times)
        index = 0
        timeStep = 0
        freq = {}
        while maxCount > 0:
            diff = times[index + 1] - times[index]
            if diff == 0:
                # This is a duplicate record, try to fix later
                index += 1
                continue
            if diff in freq:
                freq[diff] += 1
            else:
                freq[diff] = 1
            if freq[diff] > 6:  # Call it good with 6 in a row?
                return diff
            if timeStep == 0 or timeStep == diff:
                timeStep = diff
            maxCount = maxCount - 1
            index += 1
        logging.debug("%" * 80)
        logging.debug("Could not find a step")
        logging.debug("%" * 80)
        return 0

    # def fillMiddleGaps(self, fullTimeSet, dataSet, noneCount):
    #     logging.debug(f"fillMiddleGaps::Full array size {len(fullTimeSet)} and actual data {len(dataSet[:, 0])} ")
    #     goodArray = []
    #     for etime in fullTimeSet:
    #         found = False
    #         for x in range(0, numpy.shape(dataSet)[0]):
    #             if etime == dataSet[x, 0]:
    #                 goodArray.append(dataSet[x])
    #                 # I found the record, go to the next one
    #                 found = True
    #                 break
    #         if not found:
    #             goodArray.append(self.getNoneArray(etime, noneCount))
    #     # All done, now overwrite the the new data
    #     dataSet = numpy.asarray(goodArray)  # .astype(float)
    #     logging.debug("Fixed the data structure. Running QC")
    #     return dataSet

    def getNoneArray(self, etime, noneCount):
        if noneCount == 1:
            return numpy.asarray([etime, None]).astype(float)
        if noneCount == 2:
            return numpy.asarray([etime, None, None]).astype(float)
        if noneCount == 3:
            return numpy.asarray([etime, None, None, None]).astype(float)
        if noneCount == 4:
            return numpy.asarray([etime, None, None, None, None]).astype(float)
        if noneCount == 5:
            return numpy.asarray([etime, None, None, None, None, None]).astype(float)
        if noneCount == 6:
            return numpy.asarray([etime, None, None, None, None, None, None]).astype(float)
        if noneCount == 7:
            return numpy.asarray([etime, None, None, None, None, None, None, None]).astype(float)
        if noneCount == 8:
            return numpy.asarray([etime, None, None, None, None, None, None, None, None]).astype(float)
        if noneCount == 9:
            return numpy.asarray([etime, None, None, None, None, None, None, None, None, None]).astype(float)
        if noneCount == 10:
            return numpy.asarray([etime, None, None, None, None, None, None, None, None, None, None]).astype(float)
        if noneCount == 11:
            return numpy.asarray([etime, None, None, None, None, None, None, None, None, None, None, None]).astype(
                float)
        if noneCount == 12:
            return numpy.asarray(
                [etime, None, None, None, None, None, None, None, None, None, None, None, None]).astype(float)
        if noneCount == 13:
            return numpy.asarray(
                [etime, None, None, None, None, None, None, None, None, None, None, None, None, None]).astype(float)
        if noneCount == 14:
            return numpy.asarray(
                [etime, None, None, None, None, None, None, None, None, None, None, None, None, None, None]).astype(
                float)
        if noneCount == 15:
            return numpy.asarray(
                [etime, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                 None]).astype(float)
        if noneCount == 16:
            return numpy.asarray(
                [etime, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                 None]).astype(float)
        if noneCount == 17:
            return numpy.asarray(
                [etime, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                 None]).astype(float)
