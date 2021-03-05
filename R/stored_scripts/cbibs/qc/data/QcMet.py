# -*- coding: utf-8 -*-

import numpy as np
import logging

# Local imports
from cbibs.CbibsConstants import CbibsConstants
from cbibs.qc.Qartod import Qartod
from cbibs.qc.data.QcDataBase import QcDataBase


class QcMet(QcDataBase):

    def __init__(self, shortName):
        self.shortName = shortName
        self.qc_name = "Met"

    def runQcFlags(self, cbibsDataStruct, timeStep):
        # Create a new data structure
        self.airTempQc(cbibsDataStruct, timeStep)
        self.airPressureQc(cbibsDataStruct)
        self.relativeHumidityQc(cbibsDataStruct)
        self.latLonQC(cbibsDataStruct)
        return cbibsDataStruct

    def airTempQc(self, cbibsDataStruct, timeStep, logFlag=False):

        timeArray = cbibsDataStruct[:, 0].astype(float)
        dataArray = cbibsDataStruct[:, CbibsConstants.API_AIR_TEMPERATURE.dataIdx].astype(float)
        processedQc = Qartod.airTemperatureQC(self.shortName, timeArray, dataArray, timeStep, "K", logFlag)

        if logFlag:
            logging.debug("QC - AirTemperature")
            logging.debug(processedQc)

        # Human QC
        processedQc = self.applyOverrideFlags(
            CbibsConstants.API_AIR_TEMPERATURE.apiName, cbibsDataStruct[:, 0], processedQc)

        if logFlag:
            logging.debug("QC - Air Temperature")
            logging.debug(processedQc)

        # Assign the new QC values
        cbibsDataStruct[:, CbibsConstants.API_AIR_TEMPERATURE.qcIdx] = processedQc

    def airPressureQc(self, cbibsDataStruct, logFlag=False):
        timeArray = cbibsDataStruct[:, 0].astype(float)
        dataArray = cbibsDataStruct[:, CbibsConstants.API_AIR_PRESSURE.dataIdx].astype(float)
        processedQc = Qartod.airPressureQC(self.shortName, timeArray, dataArray, logFlag)

        if logFlag:
            logging.debug("QC - airPressureNetCdf")
            logging.debug(processedQc)

        # Human QC
        processedQc = self.applyOverrideFlags(
            CbibsConstants.API_AIR_PRESSURE.apiName, cbibsDataStruct[:, 0], processedQc)

        if logFlag:
            logging.debug("QC - airPressureNetCdf")
            logging.debug(processedQc)

        # Assign the new QC values
        cbibsDataStruct[:, CbibsConstants.API_AIR_PRESSURE.qcIdx] = processedQc

    def relativeHumidityQc(self, cbibsDataStruct, logFlag=False):
        timeArray = cbibsDataStruct[:, 0].astype(float)
        dataArray = cbibsDataStruct[:, CbibsConstants.API_RELATIVE_HUMIDITY.dataIdx].astype(float)
        processedQc = Qartod.relativeHumidityQC(self.shortName, timeArray, dataArray, logFlag)

        if logFlag:
            logging.debug("QC - relativeHumidityNetCdf")
            logging.debug(processedQc)

        # Human QC
        processedQc = self.applyOverrideFlags(
            CbibsConstants.API_RELATIVE_HUMIDITY.apiName, cbibsDataStruct[:, 0], processedQc)

        if logFlag:
            logging.debug("QC - relativeHumidityNetCdf")
            logging.debug(processedQc)

        # Assign the new QC values
        cbibsDataStruct[:, CbibsConstants.API_RELATIVE_HUMIDITY.qcIdx] = processedQc

    def latLonQC(self, cbibsDataStruct, logFlag=True):

        timeArray = cbibsDataStruct[:, 0].astype(float)
        latArray = cbibsDataStruct[:, CbibsConstants.API_LATITUDE.dataIdx].astype(float)
        lonArray = cbibsDataStruct[:, CbibsConstants.API_LONGITUDE.dataIdx].astype(float)
        processedQc = Qartod.locationQC(self.shortName, timeArray, latArray, lonArray)

        if logFlag:
            logging.debug("QC - location")
            logging.debug(processedQc)

        # Human QC
        processedQc = self.applyOverrideFlags(
            CbibsConstants.API_LATITUDE.apiName, cbibsDataStruct[:, 0], processedQc)

        if logFlag:
            logging.debug("QC - location")
            logging.debug(processedQc)

        # Assign the new QC values
        cbibsDataStruct[:, CbibsConstants.API_LATITUDE.qcIdx] = processedQc
