# -*- coding: utf-8 -*-

import enum


class CbibsStation(enum.Enum):
    S = "S", "Susquehanna", 44057, 39.5404, -76.0736
    SN = "SN", "Patapsco", 44043, 39.15191, -76.39115
    AN = "AN", "Annapolis", 44063, 38.9631, -76.4475
    UP = "UP", "Upper Potomac", 44061, 38.7877, -77.0357
    GR = "GR", "Gooses Reef", 44062, 38.5563, -76.4147
    PL = "PL", "Point Lookout", 44042, 38.033, -76.3355
    SR = "SR", "Stingray Point", 44058, 37.5672, -76.2574
    YS = "YS", "York Spit", 44072, 37.20063, -76.26598
    J = "J", "Jamestown", 44041, 37.21137, -76.78677
    FL = "FL", "First Landing", 44064, 36.9981, -76.0873
    N = "N", "Norfolk", 44059, 36.84463, -76.30044

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, shortName, longName, wmo, lat, lon):
        self.shortName = shortName
        self.longName = longName
        self.wmo = wmo
        self.lat = lat
        self.lon = lon


    @staticmethod
    def getAllStationNames():
        enum_list =[e.shortName for e in CbibsStation]
        return enum_list
