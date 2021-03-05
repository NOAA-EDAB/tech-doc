import logging

import numpy

# local imports
from cbibs.CbibsConstants import CbibsConstants
from cbibs.db.DBProcessedMgr import DBProcessedMgr
from cbibs.vo.CbibsMetVo import CbibsMetVo


class DBMetMgr(DBProcessedMgr):

    def __init__(self, station, useSI=False):
        super().__init__(station, useSI)
        self.station = station
        self.tableName = "met"

    def createNewTable(self, dbConnection):
        c = dbConnection.cursor()

        # Create table
        # ('AN', 1258570800.0, None, 4, 'sea_water_salinity', 'PSU', 38.9636, -76.4468, 0.0)
        c.execute('''CREATE TABLE met          
                     (obs_time integer , air_temp real, air_temp_unit, air_temp_qc integer, air_pres real, 
                     air_pres_unit, air_pres_qc integer, rh real, rh_unit, rh_qc integer, lat real, lat_unit,
                      lon real, lon_unit, loc_qc integer)''')

        # Save (commit) the changes
        dbConnection.commit()
        c.execute('''CREATE INDEX "met_time_idx" ON "met"("obs_time")''')
        dbConnection.commit()

        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        # dbConnection.close()

    def insertOriginal(self, beginDate, endDate, data, cbibsVo):
        self.deleteData(beginDate, endDate)  # Don't insert duplicates
        conn = self.getConnection()
        cur = conn.cursor()
        cur.execute('BEGIN TRANSACTION')
        for chunk in data:
            cur.execute(
                'INSERT OR IGNORE INTO met (obs_time, air_temp, air_temp_unit, air_temp_qc, air_pres, air_pres_unit,'
                ' air_pres_qc, rh, rh_unit, rh_qc, lat, lat_unit, lon, lon_unit, loc_qc) '
                'VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                (chunk[0],
                 chunk[CbibsConstants.API_AIR_TEMPERATURE.dataIdx], cbibsVo.units[CbibsConstants.API_AIR_TEMPERATURE.unitIdx],
                 chunk[CbibsConstants.API_AIR_TEMPERATURE.qcIdx],
                 chunk[CbibsConstants.API_AIR_PRESSURE.dataIdx],  cbibsVo.units[CbibsConstants.API_AIR_PRESSURE.unitIdx],
                 chunk[CbibsConstants.API_AIR_PRESSURE.qcIdx],
                 chunk[CbibsConstants.API_RELATIVE_HUMIDITY.dataIdx],  cbibsVo.units[CbibsConstants.API_RELATIVE_HUMIDITY.unitIdx],
                 chunk[CbibsConstants.API_RELATIVE_HUMIDITY.qcIdx],
                 chunk[CbibsConstants.API_LATITUDE.dataIdx],  cbibsVo.units[CbibsConstants.API_LATITUDE.unitIdx],
                 chunk[CbibsConstants.API_LONGITUDE.dataIdx],
                 cbibsVo.units[CbibsConstants.API_LONGITUDE.unitIdx], chunk[CbibsConstants.API_LONGITUDE.qcIdx]))

        cur.execute('COMMIT')

    def deleteData(self, beginDateEpoch, endDateEpoch):
        ''' Delete data before inserting to avoid duplicates and maintain idempotency '''
        conn = self.getConnection()
        cur = conn.cursor()
        cur.execute('BEGIN TRANSACTION')
        rowcount = cur.execute('delete from met where obs_time between ? and ?',
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
            'select distinct obs_time, air_temp, air_temp_unit, air_temp_qc, air_pres, air_pres_unit, air_pres_qc, rh,'
            'rh_unit, rh_qc, lat, lat_unit, lon, lon_unit, loc_qc '
            'from met where obs_time >= ? and obs_time < ? order by obs_time',
            (beginDateEpoch, endDateEpoch))
        allr = rows.fetchall()

        # If no data return None
        #if len(allr) < 1:
        #    return None

        # I have data, at least one row
        cbibsVo = CbibsMetVo(self.useSI)
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
                cbibsVo.measures.append([time, None, None, None, None, None, None, None, None, None])
        else:
            logging.debug("Got a full set")
        return cbibsVo