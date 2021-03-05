# -*- coding: utf-8 -*-

import enum


class CbibsConstants(enum.Enum):
    # MET datbase structure
    # 0 obs_time,
    # 1,2 air_temp, air_temp_qc,
    # 3,4 air_pres, air_pres_qc,
    # 5,6 rh, Rh_qc,
    # 7,8,9 lat, lon,loc_qc
    API_AIR_TEMPERATURE = 1, 2, 0, "air_temperature", "Air Temperature", "MET"
    API_AIR_PRESSURE = 3, 4, 1, "air_pressure", "Air Pressure", "MET"
    API_RELATIVE_HUMIDITY = 5, 6, 2, "relative_humidity", "Humidity", "MET"
    API_LATITUDE = 7, 9, 3, "grid_latitude", "Latitude", "MET"
    API_LONGITUDE = 8, 9, 4, "grid_longitude", "Longitude", "MET"

    # WQ database structure
    # 0,1 obs_time, # no elevation RIGHT NOWaDD??
    # 2,3 chlorophyll, chlorophyll_qc
    # 4,5 do, do_qc
    # 6,7 salinity, salinity_qc
    # 8,9 turbidity, turbidity_qc
    # 10,11 sw_temp, sw_temp_qc
    API_CHLOROPHYLL = 2, 3, 0, "mass_concentration_of_chlorophyll_in_sea_water", "Chlorophyll", "WQ"
    API_DISSOLVED_OXYGEN = 4, 5, 1, "mass_concentration_of_oxygen_in_sea_water", "Dissolved Oxygen", "WQ"
    API_WATER_SALINITY = 6, 7, 2, "sea_water_salinity", "Salinity", "WQ"
    API_TURBIDITY = 8, 9, 3, "simple_turbidity", "Turbidity", "WQ"
    API_WATER_TEMP = 10, 11, 4, "sea_water_temperature", "Sea Water Temp", "WQ"

    # WAVES obs_time
    # 1 wave_from_dir
    # 2 wind_period
    # 3 sig_height
    # 4 sig_height_qc
    API_WAVE_FROM_DIRECTION = 1, 4, 0, "sea_surface_wave_from_direction", "Wave from Direction", "WAVES"
    API_WIND_WAVE_PERIOD = 2, 4, 1, "sea_surface_wind_wave_period", "Wind Wave Period", "WAVES"
    API_WAVE_SIG_HEIGHT = 3, 4, 2, "sea_surface_wave_significant_height", "Wave Sig Height", "WAVES"

    # U and V vectors when stored in the pickle
    # 0 obs_time
    # 1 ws,
    # 2 wd,
    # 3,4 u, v,
    # 5 wind_qc
    API_WIND_SPEED = 1, 5, 0, "wind_speed", "Wind Speed", "WINDS"
    API_WIND_FROM_DIRECTION = 2, 5, 1, "wind_from_direction", "Wind From Direction", "WINDS"
    API_WIND_U = 3, 5, 0, "wind_speed", "Wind Speed U", "WINDS"
    API_WIND_V = 4, 5, 0, "wind_from_direction", "Wind From V", "WINDS"

    # Currents, this is averages. The profiles are held in the enum
    # 0 obs_time
    # 1 cspeed,
    # 2 cdir,
    # 3,4 u, v,
    # 5 qc
    # 6 elevation
    API_CURRENT_AVG_SPEED = 1, 5, 0, "current_average_speed", "Current Speed", "CURRENTS"
    API_CURRENT_AVG_DIRECTION = 2, 5, 1, "current_average_direction", "Current Direction", "CURRENTS"
    API_CURRENT_NORTH = 3, 5, 2, "current_average_speed", "Current Speed", "CURRENTS"
    API_CURRENT_EAST = 4, 5, 3, "current_average_direction", "Current Direction", "CURRENTS"

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, dataIdx, qcIdx, unitIdx, apiName, displayName, group):
        self.dataIdx = dataIdx
        self.qcIdx = qcIdx
        self.unitIdx = unitIdx
        self.apiName = apiName
        self.displayName = displayName
        self.group = group
