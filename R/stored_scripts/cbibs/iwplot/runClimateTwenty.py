import logging
import os
from datetime import datetime, timedelta

import csv
import matplotlib
import matplotlib.style
import numpy
import pytz
from matplotlib import pyplot
import matplotlib.dates as mdates
from cbibs.CbibsConstants import CbibsConstants
from cbibs.CbibsStations import CbibsStation
from cbibs.CbibsUtil import CbibsUtil
from cbibs.iwplot.plotClimateTwenty import PlotClimateTwenty
from cbibs.iwplot.plotUtil import PlotUtil

minYear = 2010
maxYear = 2020


def main():
    # Create the style
    matplotlib.style.use('seaborn-bright')
    pyplot.rcParams.update({'font.size': 16})

    # This plot uses one station
    stationName = 'GR'
    cbibsEnum = CbibsConstants.API_WATER_TEMP

    # The time range for the reference data set
    beginDate = datetime(2020, 1, 1, 0, 0, 0)
    endDate = datetime(2020, 12, 31, 23, 59, 59)
    beginDateEpoch = pytz.UTC.localize(beginDate).timestamp()
    endDateEpoch = pytz.UTC.localize(endDate).timestamp()
    dTime = [beginDate + timedelta(days=x) for x in range(367)]
    logging.debug(f"First Date {dTime[0]}")
    logging.debug(f"Last Date {dTime[-1]}")

    # Create an instance of the climate plotter. Must have the number of plots
    begYear = datetime.utcfromtimestamp(beginDateEpoch).strftime('%Y')
    plotTitle = f"NOAA CBIBS Station: {CbibsStation[stationName].longName} - {cbibsEnum.displayName} {begYear}"
    plotTitle += "\nlatitude:38.55 longitude:-76.41";
    # Create the physical plot
    figWidth = 13.0
    figHeight = 7.5
    fig, axes = pyplot.subplots(1, squeeze=False, figsize=(figWidth, figHeight), dpi=90)

    extraYears = None  # [2016, 2017]
    # plotter.setTitle(f"Station: {stationName} - {cbibsEnum.displayName}")
    pct = PlotClimateTwenty()
    plottingObject = pct.createPlottingDataVO(stationName, beginDateEpoch, endDateEpoch, extraYears, cbibsEnum, minYear,
                                              maxYear)

    if plottingObject is None:
        logging.warning("No data from the database")
        return
    # Setting it to the units here, redundant but allows for changes
    plottingObject.setLeftLabel(plottingObject.units)
    plottingObject.setRightLabel(cbibsEnum.displayName)

    # Setup is complete, create the plot
    createPrimaryPlot(axes, 0, plotTitle, plottingObject, dTime)
    fig.autofmt_xdate()
    pyplot.tight_layout()

    # Everything is setup, save the file
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(ROOT_DIR, 'genimg', os.path.splitext(os.path.basename(__file__))[0])
    if not os.path.exists(filename):
        os.makedirs(filename)
    filename += os.path.sep + f"{stationName}_2020_{cbibsEnum.displayName}.png"
    fig.savefig(filename, format='png', dpi=90)  # ,bbox_inches='tight')
    # pyplot.show()


def createPrimaryPlot(axes, axesIndex, plotTitle, plottingDataVO, dTime, showLegend=True):
    # Setup each plot, the last one will be different
    ax = axes[axesIndex][0]

    # Set the y_Axes label and the title
    ax.set_ylabel(f"{plottingDataVO.rightLabel} [{plottingDataVO.leftLabel}]")
    ax.set_title(plotTitle, pad=12)

    ax.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    ax.grid(which='major', axis='y')

    # X-Axis date labeling
    myFmt = mdates.DateFormatter('%m-%d')
    ax.xaxis.set_major_formatter(myFmt)
    ax.set_xlabel("months")

    # Get the subplot using the index
    subPlotAxes = ax  # self.getAxesByIndex(axesIndex)
    if plottingDataVO.yMin is not None and plottingDataVO.yMax is not None:
        if plottingDataVO.yMin != 0 and plottingDataVO.yMax != 0:
            subPlotAxes.set_ylim([plottingDataVO.yMin, plottingDataVO.yMax])

    # dTime = getTimeArray(plottingDataVO.timeArray)
    dataTime, dataVals = PlotUtil.getDatesFromClimate(plottingDataVO.referenceData, dTime)
    subPlotAxes.plot_date(dataTime, dataVals, 'b-', linewidth=1.5,
                          label=f"{plottingDataVO.rightLabel} daily avg obs {maxYear}")

    # This is the averaging stats plot.
    bucketTime, minData, maxData, stdMin, stdMax, avg, minDataRaw, maxDataRaw = PlotUtil.getDatesFromBuckets(
        plottingDataVO.climateData,
        dataTime)
    fillLabel = f"{plottingDataVO.rightLabel} max/min, {minYear} - {maxYear - 1}"
    # Fill the area between the max and the min
    subPlotAxes.fill_between(bucketTime, minData, maxData, color='r', interpolate=False, alpha=.1, label=fillLabel)

    # Add the averages to the plot
    dateLabel = f"{plottingDataVO.rightLabel} avg obs, {minYear} - {maxYear - 1}"
    subPlotAxes.plot_date(dataTime, avg, 'r-', linewidth=1.5, label=dateLabel)

    # Add the extra climate data
    if plottingDataVO.extraData is not None:
        for value in plottingDataVO.extraData:
            # dataTime, dataVals = CbibsClimatePlotter.getDatesFromClimate(data, dTime[0])
            dataTimex, dataValsx = PlotUtil.getDatesFromClimate(plottingDataVO.extraData[value], dTime)
            subPlotAxes.plot_date(dataTimex, dataValsx, '--', linewidth=0.5, label=value)

    fileName = "GR_Watertemp_Data.csv"
    if fileName is not None:
        with open(fileName, "w+", newline='\n') as csvfile:
            # writer = csv.writer(csvfile, delimiter=',')  # , quotechar='|')
            csvfile.write('Date,2020 Daily,2010-2019 avg, 2010-2019 min, 2010-2019 max\n')
            count = 0
            for x in dataTime:
                csvfile.write(
                    x.strftime('%m/%d/%Y %H:%M:%S') + ',{0:.2f}'.format(dataVals[count]) + ',{0:.2f}'.format(
                        avg[count]) + ',{0:.2f}'.format(minDataRaw[count]) + ',{0:.2f}'.format(
                        maxDataRaw[count]) + '\n')
                count += 1

    # Show the legend of everything that we added
    if showLegend:
        subPlotAxes.legend(loc='upper left')


def createSecondAxes(plotter, axes, plotIdx, stationName, beginDateEpoch, endDateEpoch, extraYears, cbibsEnum, minYear,
                     maxYear):
    # Get the data for the second axes
    secondAxesVO = plotter.createPlottingDataVO(stationName, beginDateEpoch, endDateEpoch, extraYears,
                                                cbibsEnum, minYear, maxYear)
    # Setup the labels - Dont need this
    secondAxesVO.setLeftLabel(secondAxesVO.units)
    secondAxesVO.setRightLabel(cbibsEnum.displayName)

    # Get the axes twin
    axes2 = axes[plotIdx][0].twinx()

    dTime = getTimeArray(secondAxesVO.timeArray)
    dataTime, dataVals = PlotUtil.getDatesFromClimate(secondAxesVO.referenceData, dTime)

    # This is the averaging stats plot.
    bucketTime, minData, maxData, stdMin, stdMax, avg = PlotUtil.getDatesFromBuckets(secondAxesVO.climateData,
                                                                                     dataTime)
    fillLabel = f"{cbibsEnum.displayName} max/min, {minYear} - {maxYear}"
    # Fill the area between the max and the min
    axes2.fill_between(bucketTime, minData, maxData, color='darkorchid', interpolate=False, alpha=.1, label=fillLabel)

    axes2.plot_date(dataTime, dataVals, fmt='-.', c='darkorchid', linewidth=1.0,
                    label=f"{cbibsEnum.displayName}")


    axes2.yaxis.set_label_position("right")
    axes2.set_ylabel(f"{cbibsEnum.displayName} [{secondAxesVO.units}]")

    # Show the legend of everything that we added
    axes2.legend(loc='upper left')


def getTimeArray(timeArray):
    ''' Take a epoch time array. Sort it then convert into datetime objects '''
    timeArray = numpy.asarray(sorted(timeArray)).astype(float)
    dateconv = numpy.vectorize(CbibsUtil.vectorDateChange)
    dTime = dateconv(timeArray)
    logging.debug(f"First Date {dTime[0]}")
    logging.debug(f"Last Date {dTime[-1]}")
    return dTime


if __name__ == '__main__':
    logFile = os.path.join(CbibsUtil.ROOT_DIR, 'logs', 'runClimateTewnty.txt')
    # Configure logging
    logging.basicConfig(filename=logFile,
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)
    # logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format="%(message)s")
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    main()
    # plotWithTwoAxes()
