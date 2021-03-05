import datetime
import logging
import os
import pysqlite3

import numpy

# local imports
from cbibs.CbibsUtil import CbibsUtil


class DBOriginalMgr(object):
    '''Manage the original DB files'''
    originalDbSuffix = "Original.db"
    epoch = datetime.datetime.utcfromtimestamp(0)

    def __init__(self, station):
        self.station = station

    # # TODO All dates are epoch at this point
    # def unix_time_millis(self, dt):
    #     # Get the UTC time in epoch seconds
    #     return int((dt - DBOriginalMgr.epoch).total_seconds())  # * 1000.0

    # @staticmethod
    # def getFileDir(baseDir):
    #     return fileCfg.basedirOriginal

    def getDatabaseName(self):
        origDir = CbibsUtil.basedirOriginal
        if not os.path.exists(origDir):
            os.makedirs(origDir)
        database = origDir + os.path.sep + self.station + "_" + DBOriginalMgr.originalDbSuffix
        return database

    def createOriginalDb(self, database):
        conn = pysqlite3.connect(database)
        c = conn.cursor()

        # Create table
        # ('AN', 1258570800.0, None, 4, 'sea_water_salinity', 'PSU', 38.9636, -76.4468, 0.0)
        c.execute('''CREATE TABLE obs
                     (station text, obs_time integer , obs_value real, qc_code integer, varname text, units text, 
                     lat real, lon real, elevation real)''')

        # Save (commit) the changes
        conn.commit()

        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        conn.close()

    def getConnection(self):
        # First get the database. This will create the path
        database = self.getDatabaseName()
        if not os.path.exists(database):
            # First run, create the table
            self.createOriginalDb(database)
        return pysqlite3.connect(database)

    def deleteData(self, beginEpoch, endTimeEpoch):
        ''' Delete data before inserting to avoid duplicates and maintain idempotency '''
        conn = self.getConnection()
        cur = conn.cursor()
        cur.execute('BEGIN TRANSACTION')

        # beginEpoch = self.unix_time_millis(beginDate)
        # ndTimeEpoch = self.unix_time_millis(endDate)
        rowcount = cur.execute('delete from obs where obs_time between ? and ?', (beginEpoch, endTimeEpoch)).rowcount

        # Save (commit) the changes
        conn.commit()

        logging.debug(f"deleted {rowcount} records from the database")
        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        conn.close()

    def insertOriginal(self, beginDateEpoch, endDateEpoch, data):
        self.deleteData(beginDateEpoch, endDateEpoch)  # Don't insert duplicates
        conn = self.getConnection()
        cur = conn.cursor()
        cur.execute('BEGIN TRANSACTION')
        for chunk in data:
            cur.execute(
                'INSERT OR IGNORE INTO obs (station, obs_time, obs_value, qc_code, varname, units, lat, lon, elevation) VALUES (?,?,?,?,?,?,?,?,?)',
                (chunk[0], chunk[1], chunk[2], chunk[3], chunk[4], chunk[5], chunk[6], chunk[7], chunk[8]))

        cur.execute('COMMIT')

    def queryOriginalData(self):
        conn = self.getConnection()
        cur = conn.cursor()
        rows = cur.execute('select * from obs limit 25')
        # cur.execute('BEGIN TRANSACTION')
        for row in rows:
            logging.debug(row)

    def getTimeArray(self, beginDate, endDate):
        conn = self.getConnection()
        cur = conn.cursor()
        cursor = cur.execute('select distinct obs_time from obs where obs_time between ? and ?',
                             (beginDate, endDate))
        dataArr = []
        for row in cursor:
            dataArr.append(int(row[0]))
        return dataArr

    def getDataFromDbFile(self, timeArray, index, beginDate, endDate, variableName, elevation=0):
        logging.debug("getDataFromDbFile")
        # pklData = pd.read_pickle(dbfile)
        conn = self.getConnection()
        cur = conn.cursor()
        cur.execute(
            'select obs_time, obs_value, qc_code from obs where obs_time between ? and ? and varname=? and elevation=?',
            (beginDate, endDate, variableName, elevation))
        rows = cur.fetchall()
        # dataArr = numpy.zeros([3,len(rows)])
        counter = 0
        for row in rows:
            # iterate over the time array
            for tx in timeArray[0,]:
                if tx == row[0]:
                    timeArray[index, counter] = row[1]
                    timeArray[index + 1, counter] = row[2]
                    continue
            counter += 1

        logging.debug(numpy.shape(timeArray))
        logging.debug(timeArray)
        logging.debug("Trying to get a slice of variables")
        return timeArray

    def getMetDataFromDbFile(self, beginDateEpoch, endDateEpoch):

        logging.debug("getMetDataFromDbFile")
        conn = self.getConnection()
        cur = conn.cursor()
        query = '''with times as (select distinct obs_time from obs where obs_time between ? and ?)
            select
                CAST(times.obs_time AS REAL) ,    
                atemp.obs_value + 273.15,
                "K",
                atemp.qc_code,
                apres.obs_value,
                apres.units,
                apres.qc_code,
                rh.obs_value,
                rh.units,
                rh.qc_code,
                lat.obs_value,
                lat.units,
                lon.obs_value,
                lon.units,
                lon.qc_code                
            from
                times
                left outer join obs atemp 
                    on times.obs_time = atemp.obs_time
                    and atemp.varname='air_temperature'
                    and atemp.obs_time between ? and ?
                left outer join obs apres 
                    on times.obs_time = apres.obs_time
                    and apres.varname='air_pressure'
                    and apres.obs_time between ? and ?
                left outer join obs rh
                    on times.obs_time = rh.obs_time
                    and rh.varname='relative_humidity'
                    and rh.obs_time between ? and ?
                left outer join obs lat
                    on times.obs_time = lat.obs_time
                    and lat.varname='grid_latitude'
                    and lat.obs_time between ? and ?     
                left outer join obs lon
                    on times.obs_time = lon.obs_time
                    and lon.varname='grid_longitude'
                    and lon.obs_time between ? and ?                                                
            order by times.obs_time'''
        #  where (atemp.obs_value is not null and apres.obs_value is not null and rh.obs_value is not null
        #                 and lat.obs_value is not null and lon.obs_value is not null)
        cursor = cur.execute(query,
                             (beginDateEpoch, endDateEpoch, beginDateEpoch, endDateEpoch, beginDateEpoch, endDateEpoch,
                              beginDateEpoch, endDateEpoch, beginDateEpoch, endDateEpoch, beginDateEpoch, endDateEpoch))

        dataArr = []  # numpy.zeros([3,len(rows)])
        counter = 0
        for row in cursor:
            # logging.debug(row)
            counter += 1
            if (row[1] is None and row[4] is None and row[7] is None and row[10] is None and row[12] is None):
                logging.debug(f"*-*-*-*-*-*-*-*-*-*-*-*-*-*- SKIPPING {row[0]} *-*-*-*-*-*-*-*-*-*-*-*-*-*-")
                continue
            dataArr.append(numpy.asarray(
                row))  # .astype(float))  # numpy.row.a[0],float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5]),float(row[6])))

        logging.debug(f"Total records: {counter} and data length: {len(dataArr)}")
        if len(dataArr) != 0:
            logging.debug(dataArr[0])
        return dataArr

    def getWindDataFromDbFile(self, beginDateEpoch, endDateEpoch):

        conn = self.getConnection()
        cur = conn.cursor()
        query = '''with times as (select distinct obs_time from obs where obs_time between ? and ?)
            select
                times.obs_time,    
                ws.obs_value,
                ws.units,
                ws.qc_code,                
                wd.obs_value,
                wd.units,
                wd.qc_code              
            from
                times
                left outer join obs ws 
                    on times.obs_time = ws.obs_time
                    and ws.varname='wind_speed'
                    and ws.obs_time between ? and ?
                left outer join obs wd 
                    on times.obs_time = wd.obs_time
                    and wd.varname='wind_from_direction'
                    and wd.obs_time between ? and ?            
            order by times.obs_time'''
        cursor = cur.execute(query,
                             (beginDateEpoch, endDateEpoch, beginDateEpoch, endDateEpoch, beginDateEpoch, endDateEpoch))

        dataArr = []
        for row in cursor:
            # Cast to a float to turn None into nan
            if (row[1] is None and row[4] is None):
                continue
            # dataArr.append(numpy.asarray(row).astype(float))
            dataArr.append(numpy.asarray(row))

        if len(dataArr) > 0:
            logging.debug(dataArr[0])
        return numpy.asarray(dataArr)

    def getWaveDataFromDbFile(self, beginDateEpoch, endDateEpoch):

        conn = self.getConnection()
        cur = conn.cursor()
        query = '''with times as (select distinct obs_time from obs where obs_time between ? and ?)
            select
                times.obs_time,
                sswfd.obs_value,
                sswfd.units, 
                sswwp.obs_value,
                sswwp.units,
                sswsh.obs_value,
                sswsh.units,
                sswsh.qc_code			
            from
                times
                inner join obs sswfd 
                    on times.obs_time = sswfd.obs_time
                    and sswfd.varname='sea_surface_wave_from_direction'
                    and sswfd.obs_time between ? and ?
                inner join obs sswwp 
                    on times.obs_time = sswwp.obs_time
                    and sswwp.varname='sea_surface_wind_wave_period'
                    and sswwp.obs_time between ? and ?
                inner join obs sswsh 
                    on times.obs_time = sswsh.obs_time
                    and sswsh.varname='sea_surface_wave_significant_height'
                    and sswsh.obs_time between ? and ?
            order by times.obs_time'''
        cursor = cur.execute(query,
                             (beginDateEpoch, endDateEpoch, beginDateEpoch, endDateEpoch, beginDateEpoch, endDateEpoch,
                              beginDateEpoch, endDateEpoch))

        dataArr = []
        for row in cursor:
            # Cast to a float to turn None into nan
            if (row[1] is None and row[3] is None and row[5] is None):
                continue
            # dataArr.append(numpy.asarray(row).astype(float))
            dataArr.append(numpy.asarray(row))

        if len(dataArr) > 0:
            logging.debug(dataArr[0])
        return numpy.asarray(dataArr)

    def getWQDataFromDbFile(self, beginDateEpoch, endDateEpoch):
        conn = self.getConnection()
        cur = conn.cursor()
        query = '''with times as (select distinct obs_time, elevation from obs where obs_time between ? and ?)
            select
                times.obs_time,
                times.elevation,
                cholo.obs_value,
                cholo.units,
                cholo.qc_code,
                diso.obs_value,
                diso.units,
                diso.qc_code,
                sws.obs_value,
                sws.units,
                sws.qc_code,
                st.obs_value,
                st.units,
                st.qc_code,
                swt.obs_value,
                swt.units,
                swt.qc_code				
            from
                times
                inner join obs cholo 
                    on times.obs_time = cholo.obs_time
                    and cholo.varname='mass_concentration_of_chlorophyll_in_sea_water'
                    and cholo.elevation = times.elevation
                    and cholo.obs_time between ? and ?
                inner join obs diso 
                    on times.obs_time = diso.obs_time
                    and diso.varname='mass_concentration_of_oxygen_in_sea_water'
                    and diso.elevation = times.elevation
                    and diso.obs_time between ? and ?
                inner join obs sws 
                    on times.obs_time = sws.obs_time
                    and sws.varname='sea_water_salinity'
                    and sws.elevation = times.elevation
                    and sws.obs_time between ? and ?
                inner join obs st 
                    on times.obs_time = st.obs_time
                    and st.varname='simple_turbidity'
                    and st.elevation = times.elevation
                    and st.obs_time between ? and ?
                inner join obs swt 
                    on times.obs_time = swt.obs_time
                    and swt.varname='sea_water_temperature'
                    and swt.elevation = times.elevation
                    and swt.obs_time between ? and ?            
                where times.elevation == 0
                order by times.obs_time'''
        cursor = cur.execute(query,
                             (beginDateEpoch, endDateEpoch, beginDateEpoch, endDateEpoch, beginDateEpoch, endDateEpoch,
                              beginDateEpoch, endDateEpoch, beginDateEpoch, endDateEpoch, beginDateEpoch, endDateEpoch))

        dataArr = []
        for row in cursor:
            # Cast to a float to turn None into nan
            if (row[2] is None and row[5] is None and row[8] is None and row[11] is None and row[14] is None):
                continue
            # dataArr.append(numpy.asarray(row).astype(float))
            dataArr.append(numpy.asarray(row))

        if len(dataArr) > 0:
            logging.debug(dataArr[0])
        return numpy.asarray(dataArr)

    # def checkWQDuplicates(self, beginDateEpoch, endDateEpoch):
    #
    #     conn = self.getConnection()
    #     cur = conn.cursor()
    #     query = '''with times as (select distinct obs_time, elevation from obs where obs_time between ? and ?)
    #         select
    #             times.obs_time,
    #             times.elevation,
    #             cholo.obs_value,
    #             cholo.qc_code,
    # 			diso.obs_value,
    #             diso.qc_code,
    #             sws.obs_value,
    #             sws.qc_code,
    #             st.obs_value,
    #             st.qc_code,
    #             swt.obs_value,
    #             swt.qc_code
    #         from
    #             times
    #             inner join obs cholo
    #                 on times.obs_time = cholo.obs_time
    #                 and cholo.varname='mass_concentration_of_chlorophyll_in_sea_water'
    #                 and cholo.elevation = times.elevation
    #                 and cholo.obs_time between ? and ?
    #             inner join obs diso
    #                 on times.obs_time = diso.obs_time
    #                 and diso.varname='mass_concentration_of_oxygen_in_sea_water'
    #                 and diso.elevation = times.elevation
    #                 and diso.obs_time between ? and ?
    #             inner join obs sws
    #                 on times.obs_time = sws.obs_time
    #                 and sws.varname='sea_water_salinity'
    #                 and sws.elevation = times.elevation
    #                 and sws.obs_time between ? and ?
    #             inner join obs st
    #                 on times.obs_time = st.obs_time
    #                 and st.varname='simple_turbidity'
    #                 and st.elevation = times.elevation
    #                 and st.obs_time between ? and ?
    #             inner join obs swt
    #                 on times.obs_time = swt.obs_time
    #                 and swt.varname='sea_water_temperature'
    #                 and swt.elevation = times.elevation
    #                 and swt.obs_time between ? and ?
    #         group by times.obs_time
    #         having count(*)>1'''
    #     cursor = cur.execute(query,
    #                          (beginDateEpoch, endDateEpoch, beginDateEpoch, endDateEpoch, beginDateEpoch, endDateEpoch,
    #                           beginDateEpoch, endDateEpoch, beginDateEpoch, endDateEpoch, beginDateEpoch, endDateEpoch))
    #
    #     if cursor.rowcount > 0:
    #         sys.exit(f"Found duplicates, check it out {beginDateEpoch}, {endDateEpoch}")
    #         return True
    #     return False

    # def deleteDuplicates(self, beginDateEpoch, endDateEpoch, parameter):
    #
    #     conn = self.getConnection()
    #     cur = conn.cursor()
    #     query = '''
    #         with times as (
    #         select max(rowid) as maxrow, obs_time, elevation from obs
    #         where obs_time between ? and ?
    #         and varname='?'
    #         group by obs_time, elevation
    #         having count( * ) > 1
    #         order by obs_time
    #         )
    #         delete
    #         from obs where
    #         ROWID in (select maxrow from times)'''
    #     cursor = cur.execute(query, (beginDateEpoch, endDateEpoch, parameter))

    def getCurrentsAvgDataFromDbFile(self, beginDateEpoch, endDateEpoch):
        conn = self.getConnection()
        cur = conn.cursor()
        cursor = cur.execute(
            '''with times as (select distinct obs_time, elevation from obs where obs_time between ? and ?)
            select
                times.obs_time,    
                cspeed.obs_value,
                cspeed.units,
                cdir.obs_value,
                cdir.units,
                cdir.elevation
            from
                times
                inner join obs cspeed 
                    on times.obs_time = cspeed.obs_time
                    and cspeed.varname='current_average_speed'
                    and times.elevation = cspeed.elevation
                    and cspeed.obs_time between ? and ?
                inner join obs cdir 
                    on times.obs_time = cdir.obs_time
                    and cdir.varname='current_average_direction'
                    and times.elevation = cdir.elevation
                    and cdir.obs_time between ? and ?                             
                    ''',
            (beginDateEpoch, endDateEpoch, beginDateEpoch, endDateEpoch, beginDateEpoch, endDateEpoch))

        dataArr = []  # numpy.zeros([3,len(rows)])
        counter = 0
        for row in cursor:
            # logging.debug(row)
            counter += 1
            # dataArr.append(numpy.asarray(row).astype(float))
            dataArr.append(numpy.asarray(row))

        if len(dataArr) > 0:
            logging.debug(dataArr[0])
        return numpy.asarray(dataArr)

    def getCurrentsProfileDataFromDbFile(self, beginDateEpoch, endDateEpoch):
        conn = self.getConnection()
        cur = conn.cursor()
        cursor = cur.execute(
            '''with times as (select distinct obs_time, elevation from obs where obs_time between ? and ?)
            select
                times.obs_time,    
                cspeed.obs_value,
                cspeed.units,
                cdir.obs_value,
                cdir.units,
                cdir.elevation
            from
                times
                inner join obs cspeed 
                    on times.obs_time = cspeed.obs_time
                    and cspeed.varname='current_speed'
					and times.elevation = cspeed.elevation
					and cspeed.elevation > -11
                    and cspeed.obs_time between ? and ?
                inner join obs cdir 
                    on times.obs_time = cdir.obs_time
                    and cdir.varname='current_direction'
					and times.elevation = cdir.elevation
					and cdir.elevation > -11
                    and cdir.obs_time between ? and ?    
                order by times.obs_time, cdir.elevation desc                         
                    ''',
            (beginDateEpoch, endDateEpoch, beginDateEpoch, endDateEpoch, beginDateEpoch, endDateEpoch))

        dataArr = []  # numpy.zeros([3,len(rows)])
        counter = 0
        for row in cursor:
            # logging.debug(row)
            counter += 1
            # dataArr.append(numpy.asarray(row).astype(float))
            dataArr.append(numpy.asarray(row))

        if len(dataArr) > 0:
            logging.debug(dataArr[0])
        return numpy.asarray(dataArr)
