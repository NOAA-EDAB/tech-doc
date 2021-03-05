# -*- coding: utf-8 -*-

import csv
from cbibs.qc.QCEntry import QCEntry
import numpy as np
import logging, os


class QCUserDataMgr(object):
    filePath = "qc/userfiles/"

    def __init__(self, station, groupName):
        self.station = station
        self.groupName = groupName
        self.qcEntries = []

    def getFileName(self):
        fileLoc = self.filePath + self.station + '_' + self.groupName + '.csv'
        exists = os.path.isfile(fileLoc)
        if exists:
            return fileLoc
        return None

    def loadFlags(self):
        fileName = self.getFileName()
        if fileName is not None:
            with open(fileName, newline='\n') as csvfile:
                cfgreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                header = True
                for row in cfgreader:
                    if header:
                        header = False
                        continue
                    # Check if the file format is correct
                    if len(row) < 6:
                        continue
                    # logging.debug(f"User data for  {self.groupName} {row}")
                    qc = QCEntry(row)
                    self.qcEntries.append(qc)

    def applyOverrideFlags(self, parameterName, times, origQC, logFlag=False):
        self.loadFlags()
        if logFlag:
            logging.debug("%" * 50)
            logging.debug(np.shape(origQC))
            logging.debug("Applying Flags")
        if self.qcEntries is None or len(self.qcEntries) < 1:
            return origQC

        self.qcEntries.sort(key=lambda x: x.beginDate, reverse=False)
        for qc in self.qcEntries:
            # Filter on the parameter name
            if qc.param == parameterName:
                index = 0
                for time in times:
                    if time >= qc.getBeginDT() and time <= qc.getEndDT():
                        origQC[index] = qc.qc
                    index += 1
        # print(np.shape(origQC))
        return origQC
