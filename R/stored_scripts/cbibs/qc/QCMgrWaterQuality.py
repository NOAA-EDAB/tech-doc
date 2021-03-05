import logging

import numpy

from cbibs.db.DBOriginalMgr import DBOriginalMgr
from cbibs.db.DBWaterQualityMgr import DBWaterQualityMgr
from cbibs.qc.QCMgrBase import QCMgrBase
from cbibs.qc.data.QcWaterQuality import QcWaterQuality
from cbibs.vo.CbibsWaterQualityVo import CbibsWaterQualityVo


class QCMgrWaterQuality(QCMgrBase):

    def runWaterQuality(self, stationName, beginDateEpoch, endDateEpoch):
        logging.debug("Running Water Quality")
        cbibsDataVo = self.getOriginalData(stationName, beginDateEpoch, endDateEpoch)
        if cbibsDataVo is None:
            return  # No data found

        # Flatten data into MET array, run QC
        metDataStruct = cbibsDataVo.getMeasures()
        qcMgr = QcWaterQuality(stationName)
        newDataStruct = qcMgr.runQcFlags(metDataStruct, cbibsDataVo.step)

        # The data has been extracted and processed, now write the processed file
        dbPro = DBWaterQualityMgr(stationName)
        dbPro.insertOriginal(beginDateEpoch, endDateEpoch, newDataStruct, cbibsDataVo)

    def getOriginalData(self, stationName, beginDateEpoch, endDateEpoch):

        # get the data from the database as an array
        dbOrig = DBOriginalMgr(stationName)
        dataWaterQuality = dbOrig.getWQDataFromDbFile(beginDateEpoch, endDateEpoch)

        # Now take that array and create objects
        if len(dataWaterQuality) < QCMgrBase.minRecordCount:
            return

        # I have data, at least one row
        cbibsWq = CbibsWaterQualityVo()
        for row in dataWaterQuality:
            cbibsWq.addRow(row)

        timeArray = cbibsWq.getTimeArray()
        cbibsWq.step = self.getStep(timeArray)
        if cbibsWq.step == 0:
            return cbibsWq
        fullTimeSet = numpy.arange(timeArray[0], timeArray[-1], cbibsWq.step)
        if len(fullTimeSet) != len(timeArray):
            logging.debug(f"Not a full set: shape {numpy.shape(fullTimeSet)} {numpy.shape(dataWaterQuality)[1] - 1}")
            # Now fill gaps
            missingTimes = list(set(fullTimeSet).symmetric_difference(timeArray))
            for time in missingTimes:
                #  [time,elevation,  chlorophyll, chlorophyll_qc, dissolved_oxygen, dissolved_oxygen_qc, salinity, salinity_qc, turbidity,
                #              turbidity_qc, water_temp, water_temp_qc]
                cbibsWq.measures.append([time, None, None, None, None, None, None, None, None, None, None, None])
        else:
            logging.debug("Got a full set")
        return cbibsWq

    def getMinuteData(self, stationName, beginDateEpoch, endDateEpoch):

        # get the data from the database as an array
        dbOrig = DBWaterQualityMgr(stationName)
        cbibsWq = dbOrig.getGroupData(beginDateEpoch, endDateEpoch)
        if cbibsWq.isEmpty():
            return cbibsWq

        timeArray = cbibsWq.getTimeArray()
        cbibsWq.step = self.getStep(timeArray)
        if cbibsWq.step == 0:
            return cbibsWq

        # Get the full time array using minutes
        fullTimeSet = numpy.arange(beginDateEpoch, endDateEpoch, 60)
        logging.debug(
            f"Begin and End Epoch {beginDateEpoch} , {endDateEpoch} full time set {len(fullTimeSet)} timearray {len(timeArray)}")
        if len(fullTimeSet) != len(timeArray):
            # Now fill gaps
            missingTimes = list(set(fullTimeSet).symmetric_difference(timeArray))
            for time in missingTimes:
                cbibsWq.measures.append([time, None, None, None, None, None, None, None, None, None, None, None])
        else:
            logging.debug("Got a full set")

        logging.debug(f"POST length of measures {len(cbibsWq.measures)}")
        return cbibsWq
