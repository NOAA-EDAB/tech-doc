# local imports
import logging

from cbibs.CbibsConstants import CbibsConstants
from cbibs.db.DBProcessedMgr import DBProcessedMgr
from cbibs.vo.CbibsWaterQualityVo import CbibsWaterQualityVo
import numpy

class DBWaterQualityMgr(DBProcessedMgr):

    def __init__(self, station, useSI=False):
        super().__init__(station, useSI)
        self.station = station
        self.tableName = "wq"

    def createNewTable(self, dbConnection):
        c = dbConnection.cursor()
        # Create table
        c.execute('''CREATE TABLE wq         
                     (obs_time integer, elevation real, chlorophyll real, chlorophyll_unit text, chlorophyll_qc integer,
                      do real, do_unit text, do_qc integer, salinity real, salinity_unit text, salinity_qc integer,
                      turbidity real, turbidity_unit text, turbidity_qc integer, sw_temp real, 
                       sw_temp_unit text, sw_temp_qc integer)''')

        # Save (commit) the changes
        dbConnection.commit()
        c.execute('''CREATE INDEX "wq_time_idx" ON "wq"("obs_time, elevation")''')
        dbConnection.commit()

        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        # dbConnection.close()

    # def insertOriginal(self, beginDate, endDate, data):
    #     self.deleteData(beginDate, endDate)  # Don't insert duplicates
    #     conn = self.getConnection()
    #     cur = conn.cursor()
    #     cur.execute('BEGIN TRANSACTION')
    #     for chunk in data:
    #         cur.execute(
    #             'INSERT OR IGNORE INTO wq (obs_time, elevation, chlorophyll, chlorophyll_unit, chlorophyll_qc,'
    #             ' do, do_unit, do_qc, salinity, salinity_unit, salinity_qc, turbidity, turbidity_unit, turbidity_qc,'
    #             ' sw_temp, sw_temp_unit, sw_temp_qc) '
    #             'VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
    #             (chunk[0], chunk[1], chunk[2], chunk[3], chunk[4], chunk[5], chunk[6], chunk[7], chunk[8], chunk[9],
    #              chunk[10], chunk[11], chunk[12], chunk[13], chunk[14], chunk[15], chunk[16]))
    #     cur.execute('COMMIT')

    def insertOriginal(self, beginDate, endDate, data, cbibsVo):
        self.deleteData(beginDate, endDate)  # Don't insert duplicates
        conn = self.getConnection()
        cur = conn.cursor()
        cur.execute('BEGIN TRANSACTION')
        for chunk in data:
            cur.execute(
                'INSERT OR IGNORE INTO wq (obs_time, elevation, chlorophyll, chlorophyll_unit, chlorophyll_qc,'
                ' do, do_unit, do_qc, salinity, salinity_unit, salinity_qc, turbidity, turbidity_unit, turbidity_qc,'
                ' sw_temp, sw_temp_unit, sw_temp_qc) '
                'VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                (chunk[0], chunk[1],
                 chunk[CbibsConstants.API_CHLOROPHYLL.dataIdx], cbibsVo.units[CbibsConstants.API_CHLOROPHYLL.unitIdx],
                 chunk[CbibsConstants.API_CHLOROPHYLL.qcIdx],
                 chunk[CbibsConstants.API_DISSOLVED_OXYGEN.dataIdx],
                 cbibsVo.units[CbibsConstants.API_DISSOLVED_OXYGEN.unitIdx],
                 chunk[CbibsConstants.API_DISSOLVED_OXYGEN.qcIdx],
                 chunk[CbibsConstants.API_WATER_SALINITY.dataIdx],
                 cbibsVo.units[CbibsConstants.API_WATER_SALINITY.unitIdx],
                 chunk[CbibsConstants.API_WATER_SALINITY.qcIdx],
                 chunk[CbibsConstants.API_TURBIDITY.dataIdx], cbibsVo.units[CbibsConstants.API_TURBIDITY.unitIdx],
                 chunk[CbibsConstants.API_TURBIDITY.qcIdx],
                 chunk[CbibsConstants.API_WATER_TEMP.dataIdx], cbibsVo.units[CbibsConstants.API_WATER_TEMP.unitIdx],
                 chunk[CbibsConstants.API_WATER_TEMP.qcIdx]))

        cur.execute('COMMIT')

    def deleteData(self, beginDateEpoch, endDateEpoch):
        ''' Delete data before inserting to avoid duplicates and maintain idempotency '''
        conn = self.getConnection()
        cur = conn.cursor()
        cur.execute('BEGIN TRANSACTION')
        rowcount = cur.execute('delete from wq where obs_time between ? and ?',
                               (beginDateEpoch, endDateEpoch)).rowcount

        # Save (commit) the changes
        conn.commit()

        logging.debug(f"deleted {rowcount} records from the database")
        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        conn.close()

    def getGroupData(self, beginDateEpoch, endDateEpoch):
        conn = self.getConnection()
        cur = conn.cursor()
        rows = cur.execute(
            'select obs_time, elevation, chlorophyll, chlorophyll_unit, chlorophyll_qc, do, do_unit, do_qc,'
            'salinity, salinity_unit, salinity_qc, turbidity, turbidity_unit, turbidity_qc, sw_temp, '
            'sw_temp_unit, sw_temp_qc from wq where obs_time >= ? and obs_time <= ? order by obs_time',
            (beginDateEpoch, endDateEpoch))
        allr = rows.fetchall()

        # If no data return None
        # if len(allr) < 1:
        #    return None

        # I have data, at least one row
        cbibsVo = CbibsWaterQualityVo(self.useSI)
        for row in allr:
            if row[0] % 60 == 0:
                cbibsVo.addRow(row)

        return cbibsVo

    def getGroupDataWithGaps(self, beginDateEpoch, endDateEpoch):
        cbibsVo = self.getGroupData(beginDateEpoch, endDateEpoch)
        timeArray = cbibsVo.getTimeArray()
        cbibsVo.step = self.getStep(timeArray)

        fullTimeSet = numpy.arange(timeArray[0], timeArray[-1], cbibsVo.step)
        if len(fullTimeSet) != len(timeArray):
            logging.debug(f"Not a full set: shape {numpy.shape(fullTimeSet)}")
            # Now fill gaps
            missingTimes = list(set(fullTimeSet).symmetric_difference(timeArray))
            for time in missingTimes:
                #  [time,elevation,  chlorophyll, chlorophyll_qc, dissolved_oxygen, dissolved_oxygen_qc, salinity, salinity_qc, turbidity,
                #              turbidity_qc, water_temp, water_temp_qc]
                cbibsVo.measures.append([time, None, None, None, None, None, None, None, None, None, None, None])
        else:
            logging.debug("Got a full set")
        return cbibsVo
