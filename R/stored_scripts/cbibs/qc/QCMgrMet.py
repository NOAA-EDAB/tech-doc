import logging

import numpy

from cbibs.db.DBMetMgr import DBMetMgr
from cbibs.db.DBOriginalMgr import DBOriginalMgr
from cbibs.qc.QCMgrBase import QCMgrBase
from cbibs.qc.data.QcMet import QcMet
from cbibs.vo.CbibsMetVo import CbibsMetVo


class QCMgrMet(QCMgrBase):

    def runMet(self, stationName, beginDateEpoch, endDateEpoch):
        cbibsDataVo = self.getOriginalData(stationName, beginDateEpoch, endDateEpoch)
        if cbibsDataVo is None:
            return  # No data found

        # Flatten data into MET array, run QC
        metDataStruct = cbibsDataVo.getMeasures()
        qcMet = QcMet(stationName)
        newDataStruct = qcMet.runQcFlags(metDataStruct, cbibsDataVo.step)

        # The data has been extracted and processed, now write the processed file. Send in the VO for the units
        dbPro = DBMetMgr(stationName)
        dbPro.insertOriginal(beginDateEpoch, endDateEpoch, newDataStruct, cbibsDataVo)

    def getOriginalData(self, stationName, beginDateEpoch, endDateEpoch):
        ''' * Private function. do not use outside * '''
        # get the data from the database as an array
        dbOrig = DBOriginalMgr(stationName)
        dataAirTemp = dbOrig.getMetDataFromDbFile(beginDateEpoch, endDateEpoch)

        # Now take that array and create objects
        if len(dataAirTemp) < QCMgrBase.minRecordCount:
            return

        # I have data, at least one row
        cbibsMet = CbibsMetVo()
        for row in dataAirTemp:
            cbibsMet.addRow(row)

        timeArray = cbibsMet.getTimeArray()
        cbibsMet.step = self.getStep(timeArray)
        if cbibsMet.step == 0:
            return cbibsMet
        fullTimeSet = numpy.arange(timeArray[0], timeArray[-1], cbibsMet.step)
        if len(fullTimeSet) != len(timeArray):
            logging.debug(f"Not a full set: shape {numpy.shape(fullTimeSet)} {numpy.shape(dataAirTemp)[1] - 1}")
            # Now fill gaps
            missingTimes = list(set(fullTimeSet).symmetric_difference(timeArray))
            for time in missingTimes:
                # airTemp, airTempQc, airPress, airPressQc, rh, rhQc, lat, lon, locQc
                cbibsMet.measures.append([time, None, None, None, None, None, None, None, None, None])
        else:
            logging.debug("Got a full set")
        return cbibsMet

    ''' Query the processed file. Use a minute time step starting at the beginning of the data and fill gaps
        There will always be gaps, this is using the lowest common denominator for all times in a grid  '''

    def getMinuteData(self, stationName, beginDateEpoch, endDateEpoch):

        # get the data from the database as an array
        dbOrig = DBMetMgr(stationName)
        cbibsMet = dbOrig.getGroupData(beginDateEpoch, endDateEpoch)
        if cbibsMet.isEmpty():
            return cbibsMet

        logging.debug(f"PRE length of measures {len(cbibsMet.measures)}")
        timeArray = cbibsMet.getTimeArray()
        cbibsMet.step = self.getStep(timeArray)


        fullTimeSet = numpy.arange(beginDateEpoch, endDateEpoch, 60)
        logging.debug(f"Begin and End Epoch {beginDateEpoch} , {endDateEpoch} full time set {len(fullTimeSet)} timearray {len(timeArray)}")
        if len(fullTimeSet) != len(timeArray):
            # logging.debug(f"Not a full set: shape {numpy.shape(fullTimeSet)} {numpy.shape(cbibsMet)[1] - 1}")
            # Now fill gaps
            missingTimes = list(set(timeArray).symmetric_difference(fullTimeSet))
            for time in missingTimes:
                if time % 60 != 0:
                    logging.debug(f"++++++++++++++++ {time} ++++++++++++++++ ")
                else:
                    # airTemp, airTempQc, airPress, airPressQc, rh, rhQc, lat, lon, locQc
                    cbibsMet.measures.append([time, None, None, None, None, None, None, None, None, None])
        else:
            logging.debug("Got a full set")

        logging.debug(f"POST length of measures {len(cbibsMet.measures)}")
        return cbibsMet
