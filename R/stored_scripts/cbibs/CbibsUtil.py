import os
from datetime import datetime

import pytz


class CbibsUtil:
    # This is the project root, which can be used safely in any class that needs relative path information
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    print(f"ROOT DIR: {ROOT_DIR}")
    basedirOriginal = os.path.join(ROOT_DIR, 'data', 'original')
    basedirProcessed = os.path.join(ROOT_DIR, 'data', 'processed')
    netCDFOutputDir = os.path.join(ROOT_DIR, 'data', 'netCDFOutput')

    dataSuffix = "_data.db"

    @staticmethod
    def convert(seconds):
        seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        return "%d:%02d:%02d" % (hour, minutes, seconds)

    @staticmethod
    def vectorDateChange(X):
        ''' Always use this function when changing date vectors '''
        return pytz.UTC.localize(datetime.utcfromtimestamp(X))
