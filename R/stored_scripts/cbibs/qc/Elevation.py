# -*- coding: utf-8 -*-

import enum


class ELEVATION(enum.Enum):
    # Query starts out like this
    # obs_time, qc_master, north_unit, east_unit,
    ONE = -1.5, 4, 9
    TWO = -2.5, 7, 8
    THREE = -3.5, 10, 7
    FOUR = -4.5, 13, 6
    FIVE = -5.5, 16, 5
    SIX = -6.5, 19, 4
    SEVEN = -7.5, 22, 3
    EIGHT = -8.5, 25, 2
    NINE = -9.5, 28, 1
    TEN = -10.5, 31, 0

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, depth, mindex, graphIndex):
        self.depth = depth
        self.mindex = mindex
        self.graphIndex = graphIndex

    @staticmethod
    def getElevationsBottomFirst():
        return sorted([ELEVATION.Double, ELEVATION.Sin], key=lambda sht: sht.depth)

    @staticmethod
    def getDepths():
        return [(ele.depth) for ele in ELEVATION]

    @staticmethod
    def getGraphIndex():
        return [(ele.graphIndex) for ele in ELEVATION]
