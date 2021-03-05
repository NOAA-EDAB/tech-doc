# -*- coding: utf-8 -*-

import enum

class QC(enum.Enum):
   
    UNKNOWN = 0, 'unknown'
    GOOD = 1,'GOOD Value'
    NOT_EVAL = 2, 'Not Evaluated, Not Available, Unknown'
    SUSPECT = 3, 'Questionable or Suspect'
    BAD = 4,'BAD'
    MISSING = 9, 'MISSING'
   
    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, intValue, description):
       self.intValue = intValue
       self.description = description
