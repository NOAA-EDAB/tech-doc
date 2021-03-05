# -*- coding: utf-8 -*-

import numpy as np
import logging

# Local imports
from cbibs.CbibsConstants import CbibsConstants
from cbibs.qc.Qartod import Qartod
from cbibs.qc.data.QcDataBase import QcDataBase


class QcWaterQuality(QcDataBase):

    def __init__(self, shortName):
        self.shortName = shortName
        self.qc_name = "WaterQuality"

    def runQcFlags(self, cbibsDataStruct, stepInterval):
        # Create a new data structure
        self.chlorophyllQc(cbibsDataStruct, CbibsConstants.API_CHLOROPHYLL)
        self.disolvedOxygenQc(cbibsDataStruct, CbibsConstants.API_DISSOLVED_OXYGEN)
        self.salinityQc(cbibsDataStruct, CbibsConstants.API_WATER_SALINITY,stepInterval)
        self.turbidityQc(cbibsDataStruct, CbibsConstants.API_TURBIDITY)
        self.seaWaterTempQc(cbibsDataStruct, CbibsConstants.API_WATER_TEMP)
        return cbibsDataStruct

    def chlorophyllQc(self, cbibsDataStruct, enum, logFlag=False):
        timeArray = cbibsDataStruct[:, 0].astype(float)
        dataArray = cbibsDataStruct[:, enum.dataIdx].astype(float)
        processedQc = Qartod.chlorophyllQC(self.shortName, timeArray, dataArray)
        if logFlag:
            logging.debug("QC - chlorophyllQc")
            logging.debug(processedQc)
        # Human QC
        processedQc = self.applyOverrideFlags(
            enum.apiName, timeArray, processedQc)

        if logFlag:
            logging.debug("QC - chlorophyllQc")
            logging.debug(processedQc)

        # Assign the new QC values
        cbibsDataStruct[:, enum.qcIdx] = processedQc

    def disolvedOxygenQc(self, cbibsDataStruct, enum, logFlag=False):
        timeArray = cbibsDataStruct[:, 0].astype(float)
        dataArray = cbibsDataStruct[:, enum.dataIdx].astype(float)

        processedQc = Qartod.disolvedOxygenQC(self.shortName, timeArray, dataArray)
        if logFlag:
            logging.debug("QC - disolvedOxygenQc")
            logging.debug(processedQc)
        # Human QC
        processedQc = self.applyOverrideFlags(enum.apiName, timeArray, processedQc)

        if logFlag:
            logging.debug("QC - disolvedOxygenQc")
            logging.debug(processedQc)

        # Assign the new QC values
        cbibsDataStruct[:, enum.qcIdx] = processedQc

    def salinityQc(self, cbibsDataStruct, enum, stepInterval, logFlag=False):
        timeArray = cbibsDataStruct[:, 0].astype(float)
        dataArray = cbibsDataStruct[:, enum.dataIdx].astype(float)
        processedQc = Qartod.salinityQC(self.shortName, timeArray, dataArray,stepInterval)
        if logFlag:
            logging.debug("QC - salinityQc")
            logging.debug(processedQc)
        # Human QC
        processedQc = self.applyOverrideFlags(enum.apiName, cbibsDataStruct[:, 0], processedQc)

        if logFlag:
            logging.debug("QC - salinityQc")
            logging.debug(processedQc)

        # Assign the new QC values
        cbibsDataStruct[:, enum.qcIdx] = processedQc

    def turbidityQc(self, cbibsDataStruct, enum, logFlag=False):
        timeArray = cbibsDataStruct[:, 0].astype(float)
        dataArray = cbibsDataStruct[:, enum.dataIdx].astype(float)
        processedQc = Qartod.turbidityQC(self.shortName, timeArray, dataArray)
        if logFlag:
            logging.debug("QC - turbidityQc")
            logging.debug(processedQc)
        # Human QC
        processedQc = self.applyOverrideFlags(
            enum.apiName, cbibsDataStruct[:, 0], processedQc)

        if logFlag:
            logging.debug("QC - turbidityQc")
            logging.debug(processedQc)

        # Assign the new QC values
        cbibsDataStruct[:, enum.qcIdx] = processedQc

    def seaWaterTempQc(self, cbibsDataStruct, enum, logFlag=False):
        timeArray = cbibsDataStruct[:, 0].astype(float)
        dataArray = cbibsDataStruct[:, enum.dataIdx].astype(float)
        processedQc = Qartod.seaWaterTempQC(self.shortName, timeArray, dataArray)
        if logFlag:
            logging.debug("QC - seaWaterTempQc")
            logging.debug(processedQc)
        # Human QC
        processedQc = self.applyOverrideFlags(
            enum.apiName, cbibsDataStruct[:, 0], processedQc)

        if logFlag:
            logging.debug("QC - seaWaterTempQc")
            logging.debug(processedQc)

        # Assign the new QC values
        cbibsDataStruct[:, enum.qcIdx] = processedQc
