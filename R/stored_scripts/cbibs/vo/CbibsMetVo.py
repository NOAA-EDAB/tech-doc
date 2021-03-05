# -*- coding: utf-8 -*-
import numpy

from cbibs.CbibsConstants import CbibsConstants
from cbibs.vo.CbibsBaseVo import CbibsBaseVo


class CbibsMetVo(CbibsBaseVo):
    ''' Init with a row from the database, Only pull units here '''

    def __init__(self, useSI=False):
        super().__init__(useSI)
        self.units = [None] * 5


    def getUnits(self, row):
        if self.units[CbibsConstants.API_AIR_TEMPERATURE.unitIdx] is None:
            if row[2] == 'K' and self.useSI:
                self.units[CbibsConstants.API_AIR_TEMPERATURE.unitIdx] = 'F'
            elif row[2] == 'K' and self.useSI:
                self.units[CbibsConstants.API_AIR_TEMPERATURE.unitIdx] = 'C'
        if self.units[CbibsConstants.API_AIR_PRESSURE.unitIdx] is None:
            self.units[CbibsConstants.API_AIR_PRESSURE.unitIdx] = row[5]
        if self.units[CbibsConstants.API_RELATIVE_HUMIDITY.unitIdx] is None:
            self.units[CbibsConstants.API_RELATIVE_HUMIDITY.unitIdx] = row[8]
        if self.units[CbibsConstants.API_LATITUDE.unitIdx] is None:
            self.units[CbibsConstants.API_LATITUDE.unitIdx] = row[11]
        if self.units[CbibsConstants.API_LONGITUDE.unitIdx] is None:
            self.units[CbibsConstants.API_LONGITUDE.unitIdx] = row[13]

    ''' Add a row, the units are stored in metadata fields '''

    def addRow(self, row):
        self.getUnits(row)
        time = row[0]
        # Convert to deg F if flagged
        if self.useSI and row[1] is not None:
            airTemp = ((row[1] + self.KELVIN) * (9 / 5)) + 32
        elif row[1] is not None:
            print(f"{type(row[1])} {row[1]}")
            airTemp = float(row[1]) + self.KELVIN
        else:
            airTemp = row[1]
            # airTempUnits = row[2]
        airTempQc = row[3]
        airPress = row[4]
        airPressUnits = row[5]
        airPressQc = row[6]
        rh = row[7]
        # rhUnits = row[8]
        rhQc = row[9]
        lat = row[10]
        # latUnits = row[11]
        lon = row[12]
        # lonUnits = row[13]
        locQc = row[14]

        # Stick the deg F to the end, should not effect anything
        self.measures.append([time, airTemp, airTempQc, airPress, airPressQc, rh, rhQc, lat, lon, locQc])

    def getHeader(self):
        header = ["Time",
                  f"{CbibsConstants.API_AIR_TEMPERATURE.displayName} ({self.units[CbibsConstants.API_AIR_TEMPERATURE.unitIdx]})",
                  f"{CbibsConstants.API_AIR_TEMPERATURE.displayName} QC",
                  f"{CbibsConstants.API_AIR_PRESSURE.displayName} ({self.units[CbibsConstants.API_AIR_PRESSURE.unitIdx]})",
                  f"{CbibsConstants.API_AIR_PRESSURE.displayName} QC",
                  f"{CbibsConstants.API_RELATIVE_HUMIDITY.displayName} ({self.units[CbibsConstants.API_RELATIVE_HUMIDITY.unitIdx]})",
                  f"{CbibsConstants.API_RELATIVE_HUMIDITY.displayName} QC",
                  f"{CbibsConstants.API_LATITUDE.displayName} ({self.units[CbibsConstants.API_LATITUDE.unitIdx]})",
                  f"{CbibsConstants.API_LONGITUDE.displayName} ({self.units[CbibsConstants.API_LONGITUDE.unitIdx]})",
                  f"Location QC"]
        return header
