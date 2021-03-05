# -*- coding: utf-8 -*-

import datetime
import time
import dateutil #parser.isoparse

class QCEntry(object):

    def __init__(self, row):        
        self.station =row[0]
        self.param = row[1]
        #  Be explicit about the timezone
        self.beginDate = dateutil.parser.isoparse(row[2])
        self.endDate = dateutil.parser.isoparse(row[3]) #.astimezone(datetime.timezone.utc)
        self.qc = row[4]
        self.offset = time.timezone #18000
  
    def __str__(self):
        ''' Output object as a string '''
        return "{}-{} From: {} To: {} ".format(self.station, self.param, self.beginDate,self.endDate) 
        
    def __repr__(self):
        ''' Output object as a string '''
        return self.station+ ", " + self.param + " From: ", self.beginDate, \
            " To: ", self.endDate
      
    def getBeginDT(self):
        # epoch = datetime.datetime(1970, 1, 1)
        # The time entered is in UTC, our computer time is different. Subtract the offset to get UTC
        return datetime.datetime.timestamp(self.beginDate) - self.offset
    
    def getEndDT(self):
        return datetime.datetime.timestamp(self.endDate) - self.offset