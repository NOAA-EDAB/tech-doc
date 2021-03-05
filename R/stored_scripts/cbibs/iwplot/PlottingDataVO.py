class PlottingDataVO:

    def __init__(self, station, timeArray, referenceData, climateData, extraData):
        self.station = station
        self.timeArray = timeArray
        self.referenceData = referenceData
        self.climateData = climateData
        self.extraData = extraData

        # Decorations
        self.leftLabel = ""
        self.rightLabel = ""
        self.units = ""
        self.yMin = 0
        self.yMax = 0

    def setLeftLabel(self, lbl):
        self.leftLabel = lbl

    def setRightLabel(self, lbl):
        self.rightLabel = lbl

    def setUnits(self, units):
        self.units = units

    def setYMin(self, min):
        self.yMin = min

    def setYMax(self, max):
        self.yMax = max
