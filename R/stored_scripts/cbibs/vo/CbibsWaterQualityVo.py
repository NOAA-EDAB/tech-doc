# -*- coding: utf-8 -*-
from cbibs.CbibsConstants import CbibsConstants
from cbibs.vo.CbibsBaseVo import CbibsBaseVo


class CbibsWaterQualityVo(CbibsBaseVo):
    ''' Init with a row from the database '''

    def __init__(self, useSI=False):
        super().__init__(useSI)
        self.units = [None] * 5

        ''' Database Query
        0 obs_time
        1 elevation
        2 chlorophyll, 3 chlorophyll_unit, 4 chlorophyll_qc
        5 do, 6 do_unit, 7 do_qc
        8 salinity, 9 salinity_unit, 10 salinity_qc
        11 turbidity, 12 turbidity_unit, 13 turbidity_qc
        14 sw_temp, 15 sw_temp_unit, 16 sw_temp_qc '''


    def getUnits(self, row):
        # Set the units, order is important
        if self.units[CbibsConstants.API_CHLOROPHYLL.unitIdx] is None:
            self.units[CbibsConstants.API_CHLOROPHYLL.unitIdx] = row[3]
        if self.units[CbibsConstants.API_DISSOLVED_OXYGEN.unitIdx] is None:
            self.units[CbibsConstants.API_DISSOLVED_OXYGEN.unitIdx] = row[6]
        if self.units[CbibsConstants.API_WATER_SALINITY.unitIdx] is None:
            self.units[CbibsConstants.API_WATER_SALINITY.unitIdx] = row[9]
        if self.units[CbibsConstants.API_TURBIDITY.unitIdx] is None:
            self.units[CbibsConstants.API_TURBIDITY.unitIdx] = row[12]
        if self.units[CbibsConstants.API_WATER_TEMP.unitIdx] is None:
            if self.useSI:
                self.units[CbibsConstants.API_WATER_TEMP.unitIdx] = 'F'
            else:
                self.units[CbibsConstants.API_WATER_TEMP.unitIdx] = row[15]

    ''' Add a row, the units are stored in metadata fields '''

    def addRow(self, row):
        self.getUnits(row)
        time = row[0]
        elevation = row[1]
        chlorophyll = row[2]
        chlorophyll_qc = row[4]
        dissolved_oxygen = row[5]
        dissolved_oxygen_qc = row[7]
        salinity = row[8]
        salinity_qc = row[10]
        turbidity = row[11]
        turbidity_qc = row[13]
        if self.useSI and row[14] is not None:
            water_temp = (row[14] * (9/5)) + 32
        else:
            water_temp = row[14]
        water_temp_qc = row[16]
        # My measures are a 2Darray in this format. The indices are fixed by CbibsConstants
        self.measures.append(
            [time, elevation, chlorophyll, chlorophyll_qc, dissolved_oxygen, dissolved_oxygen_qc, salinity, salinity_qc,
             turbidity,
             turbidity_qc, water_temp, water_temp_qc])

    def getHeader(self):
        header = ["Time", "elevation",
                  f"{CbibsConstants.API_CHLOROPHYLL.displayName} ({self.units[CbibsConstants.API_CHLOROPHYLL.unitIdx]})",
                  f"{CbibsConstants.API_CHLOROPHYLL.displayName} QC",
                  f"{CbibsConstants.API_DISSOLVED_OXYGEN.displayName} ({self.units[CbibsConstants.API_DISSOLVED_OXYGEN.unitIdx]})",
                  f"{CbibsConstants.API_DISSOLVED_OXYGEN.displayName} QC",
                  f"{CbibsConstants.API_WATER_SALINITY.displayName} ({self.units[CbibsConstants.API_WATER_SALINITY.unitIdx]})",
                  f"{CbibsConstants.API_WATER_SALINITY.displayName} QC",
                  f"{CbibsConstants.API_TURBIDITY.displayName} ({self.units[CbibsConstants.API_TURBIDITY.unitIdx]})",
                  f"{CbibsConstants.API_TURBIDITY.displayName} QC",
                  f"{CbibsConstants.API_WATER_TEMP.displayName} ({self.units[CbibsConstants.API_WATER_TEMP.unitIdx]})",
                  f"{CbibsConstants.API_WATER_TEMP.displayName} QC"]
        return header

