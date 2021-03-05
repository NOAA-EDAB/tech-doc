import datetime
import logging
import os
import sqlite3


# local imports
from cbibs.CbibsUtil import CbibsUtil


class DBProcessedMgr(object):
    originalDbName = "Processed.db"
    epoch = datetime.datetime.utcfromtimestamp(0)

    def __init__(self, station, useSI=False):
        self.station = station
        self.useSI = useSI

    def getDatabaseName(self):
        if not os.path.exists(CbibsUtil.basedirProcessed):
            os.makedirs(CbibsUtil.basedirProcessed)
        fileName = self.station + "_" + DBProcessedMgr.originalDbName
        database = os.path.join(CbibsUtil.basedirProcessed, fileName)
        return database

    def getConnection(self):
        # First get the database. This will create the path
        databaseName = self.getDatabaseName()
        conn = sqlite3.connect(databaseName)
        if not self.checkForTable(conn, self.tableName):  # Check if the table exists
            self.createNewTable(conn)
        return conn

    # TODO All dates are epoch at this point
    def unix_time_millis(self, dt):
        ''' Get the UTC time in epoch seconds '''
        return int((dt - DBProcessedMgr.epoch).total_seconds())  # * 1000.0

    def checkForTable(self, conn, tableName):
        cur = conn.cursor()
        cur.execute('BEGIN TRANSACTION')
        tbl = cur.execute('''SELECT name FROM sqlite_master WHERE type = "table" AND name = ?''',
                          (tableName,)).fetchall()
        cur.execute('COMMIT')
        if len(tbl) == 1:
            return True
        return False

    def queryOriginalData(self, limit=25):
        conn = self.getConnection()
        cur = conn.cursor()
        rows = cur.execute(f'select * from {self.tableName} limit {limit}')
        data = rows.fetchall()
        for row in data:
            logging.debug(row)
        return data



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
