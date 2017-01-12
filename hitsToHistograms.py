import pandas as pd
import numpy as np
import sys
import json
import pickle


def singleStringTo2dNumpyArray(dataAsSingleString):
	# the separator used in output files between entries (e.g. whitespace, comma, tab, ...)
	s = " "	# s = "\t" s = ", "

	dataAsList = dataAsSingleString.split("\n")
	numEntries = len(dataAsList)-1

	dataAsListList = dataAsList[0:numEntries]       # TODO investigate why the last entry of the read in list is empty
	for i in range(0,numEntries):
		dataAsListList[i] = dataAsList[i].split(s)

	dataAsNpArray = np.array(dataAsListList)
	# dataAsNpArray = np.array(dataAsListList, dtype=np.float32)
	return dataAsNpArray

def readNumpyArrayFromFile(filename):
	# open the file
	fileToRead = open(filename, 'r')
	# read the contents
	dataPlain = fileToRead.read()
	fileToRead.close()
	# parse the read data to a numpy array
	return singleStringTo2dNumpyArray(dataPlain)


# def storeHistogramAsPGM(hist, filename):
def store2dHistogramAsPGM(hist, filename):
	histFile = open(filename, 'w')
	maximalValueThisHist = np.amax(hist[0])
	# maximalValueThisHist = 2	# just to see better
	# write a valid header for a pgm image file
	histFile.write("P2\n"+str(hist[0].shape[1])+" "+str(hist[0].shape[0])+"\n"+str(int(maximalValueThisHist))+"\n")
	# write the actual data
	for row in hist[0]:
		for entry in row:
			# write the actual values
			histFile.write(str(int(entry)) + " ")
		histFile.write("\n")
	histFile.close()

def store4dHistogramAsPlainFile(hist, filename):
	histFile = open(filename, 'w')
	# write the actual data
	for row in hist[0]:
		for secondRow in row:
			for thirdRow in secondRow:
				for entry in thirdRow:
					# write the actual values
					histFile.write(str(float(entry)) + " ")
	histFile.close()

def store4dHistogramAsTimeSeriesOf3dHists(hist, filenameBase):
	# len(hist[0][0][0][0])	= time bins 	len(hist[0][0][0]) = z bins  	len(hist[0][0]) = y bins	len(hist[0]) = x bins
	numberOfTimeBins = len(hist[0][0][0][0])
	for time in range(0,numberOfTimeBins):
		histFile = open(filenameBase+str(time)+".hist", 'w')
		# write the actual data
		for xDim in hist[0]:
			for yDim in xDim:
				for zDim in yDim:
					entry = zDim[time]
					# write the actual value
					histFile.write(str(float(entry)) + " ")
		histFile.close()


if len(sys.argv) < 2 or str(sys.argv[1]) == "-h":
	print "Usage: python " + str(sys.argv[0]) + " file.h5"
	sys.exit(1)

filenameBase = str(sys.argv[1])
# print "Generating histograms from the hits in XYZ-format for files based on " + filenameBase
filenameTracks = filenameBase + "_tracks.txt"
filenameHitsXYZT = filenameBase + "_hitsXYZ.txt"
filenameHitsOMIDT = filenameBase + "_hits.txt"
filenameGeometry = "km3GeoOm.txt"
manuallySetNumberOfBinsInTime = 100
manuallySetNumberOfBinsInSpace = 20

"""
# read in the geometry
# the geometry can be used to automatically derive the number of bins. this is not used for now
geo = readNumpyArrayFromFile(filenameGeometry)
xValues = np.array(geo[:,1], np.float32)
yValues = np.array(geo[:,2], np.float32)
zValues = np.array(geo[:,3], np.float32)
xMin = np.amin(xValues)
xMax = np.amax(xValues)
yMin = np.amin(yValues)
yMax = np.amax(yValues)
zMin = np.amin(zValues)
zMax = np.amax(zValues)
xDistance = xMax - xMin
yDistance = yMax - yMin
zDistance = zMax - zMin
print "x from " + str(xMin) + " to " + str(xMax) + " --- distance " + str(xDistance)
print "y from " + str(yMin) + " to " + str(yMax) + " --- distance " + str(yDistance)
print "z from " + str(zMin) + " to " + str(zMax) + " --- distance " + str(zDistance)
"""

# read in the tracks for all events
# the tracks can be used to determine the class / desired outcome(s) for each event	# BEWARE: they may not end up as "features" !
# tracks = readNumpyArrayFromFile(filenameTracks)
# zeniths = np.array(tracks[:,2], np.float32)

numberBinsT = manuallySetNumberOfBinsInTime
numberBinsX = manuallySetNumberOfBinsInSpace
numberBinsY = manuallySetNumberOfBinsInSpace
numberBinsZ = manuallySetNumberOfBinsInSpace


print "Generating histograms from the hits in OMID versus time format for files based on " + filenameBase

# read in all hits (OMID vs time format) for all events
hits = readNumpyArrayFromFile(filenameHitsOMIDT)

# evaluate each event separately
allEventNumbers = set(hits[:,0])
for eventID in allEventNumbers:
        # evaluate one event at a time

        # filter all hits belonging to this event
        currentHitRows = np.where(hits[:,0] == eventID)[0]
        print "... found " + str(len(currentHitRows)) + " hits for event " + str(eventID)
        curHits = hits[currentHitRows]

        # slice out the OM ids of the current hits
        ids = np.array(curHits[:,1], np.int32)

        # slice out the times of the current hits
        times = np.array(curHits[:,3], np.int32)

        # create a histogram for this event
        histIDvsT = np.histogram2d(times, ids, [numberBinsT, numberBinsID])
        # histIDvsT = np.histogram2d(times, ids, [numberBinsT, numberBinsID], [[consideredStart, consideredEnd],])

        # store the histogram to file
        histFilename = "results/2dTo2d/omIDt/hist_"+filenameTracks+"_event"+str(eventID)+"_TvsOMID.pgm"
        store2dHistogramAsPGM(histIDvsT, histFilename)



print "Generating histograms from the hits in XYZT format for files based on " + filenameBase

# read in all hits for all events
hits = readNumpyArrayFromFile(filenameHitsXYZT)

# evaluate each event separately
# allEventNumbers = set(hits[:,0]) not required again
for eventID in allEventNumbers:
        # evaluate one event at a time
	
	# filter all hits belonging to this event
	currentHitRows = np.where(hits[:,0] == eventID)[0]
	print "... found " + str(len(currentHitRows)) + " hits for event " + str(eventID)
	curHits = hits[currentHitRows]

# do the 2d histograms first

	# slice out the times of the current hits
        times = np.array(curHits[:,4], np.float32)
        # slice out the coordinates of the current hits
        x = np.array(curHits[:,1], np.float32)
        y = np.array(curHits[:,2], np.float32)
        z = np.array(curHits[:,3], np.float32)

        # create histograms for this event
        histXvsT = np.histogram2d(times, x, [numberBinsT, numberBinsX])
        histYvsT = np.histogram2d(times, y, [numberBinsT, numberBinsY])
        histZvsT = np.histogram2d(times, z, [numberBinsT, numberBinsZ])
        histXvsY = np.histogram2d(y, x, [numberBinsY, numberBinsX])
        histXvsZ = np.histogram2d(z, x, [numberBinsZ, numberBinsX])
        histYvsZ = np.histogram2d(z, y, [numberBinsZ, numberBinsY])

        # store the histograms to files
        storeHistogramAsPGM(histXvsT, "results/4dTo2d/xt/hist_"+filenameTracks+"_event"+str(eventID)+"_TvsX.pgm")
        storeHistogramAsPGM(histYvsT, "results/4dTo2d/yt/hist_"+filenameTracks+"_event"+str(eventID)+"_TvsY.pgm")
        storeHistogramAsPGM(histZvsT, "results/4dTo2d/zt/hist_"+filenameTracks+"_event"+str(eventID)+"_TvsZ.pgm")
        storeHistogramAsPGM(histXvsY, "results/4dTo2d/xy/hist_"+filenameTracks+"_event"+str(eventID)+"_XvsY.pgm")
        storeHistogramAsPGM(histXvsZ, "results/4dTo2d/xz/hist_"+filenameTracks+"_event"+str(eventID)+"_XvsZ.pgm")
        storeHistogramAsPGM(histYvsZ, "results/4dTo2d/yz/hist_"+filenameTracks+"_event"+str(eventID)+"_YvsZ.pgm")


# do the 4d and 3d time series histograms next
	curHitsWithoutEventID = np.array(curHits[:,1:5], np.float32)
	histXYZT = np.histogramdd(curHitsWithoutEventID, [numberBinsX, numberBinsY, numberBinsZ, numberBinsT])

	# store the 4 dimensional histogram to file
	store4dHistogramAsPlainFile( histXYZT, "results/4dTo4d/xyzt/hist_"+filenameTracks+"_event"+str(eventID)+"_XYZT.hist")
	store4dHistogramAsTimeSeriesOf3dHists( histXYZT, "results/4dTo3dTimeSeries/xyzTimeSeries/hist_"+filenameTracks+"_event"+str(eventID)+"_XYZ")


	# this is just some code for ideas how to treat time windows better, but not relevant right now
	"""
	# Remove outliers and only consider hits close to the mean time for this event
	sortedTimes = sorted(times)
	print sortedTimes
	percentage = 0.2	# use the fraction to determine what is still considered the inner (main / certainly relevant) part of the event
	startXp = int(len(sortedTimes)*percentage)
	end1mXp = int(len(sortedTimes)*(1.0-percentage))
	#print startXp
	#print end1mXp
	innerStart = sortedTimes[startXp]
	innerEnd = sortedTimes[end1mXp]
	print "innerStart = " + str(innerStart)
	print "innerEnd = " + str(innerEnd)

	# extend the considered time window beyond the inner part to include the beginning and end of the event, but no wiered outliers
	additionalTimeFactor = 1.0	# 1.0 means 100% additional time is considered around the core, 50% before, 50% after
	consideredDuration = innerEnd - innerStart
	consideredStart = innerStart - 0.5*additionalTimeFactor*consideredDuration
	consideredEnd = innerEnd + 0.5*additionalTimeFactor*consideredDuration
	"""

	"""
	# alternative: consider a fixed time window around the mean time of the hits
	# this probably aids the comparison between events
	meanTime = np.mean(times)
	# print meanTime
	timeWindow = 2000	# the time window to consider hits, before and after the mean time of the hits. 
				# A particle should have traversed a km^3 detector in about 4000ns, the light might be around a bit longer (prob. up to 7000)
				# Usig a fixed number of bins, a smaller time window gives a finer resolution

	consideredStart = meanTime - timeWindow
	consideredEnd = meanTime + timeWindow
	timesRelative = times - consideredStart
	"""



