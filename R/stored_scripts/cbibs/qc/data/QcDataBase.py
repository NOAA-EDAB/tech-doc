# -*- coding: utf-8 -*-

from cbibs.qc.data.QCUserDataMgr import QCUserDataMgr


class QcDataBase():

    def applyOverrideFlags(self, parameterName, times, processedQc):
        qcMgr = QCUserDataMgr(self.shortName, self.qc_name)
        newQC = qcMgr.applyOverrideFlags(parameterName, times, processedQc)
        return newQC
