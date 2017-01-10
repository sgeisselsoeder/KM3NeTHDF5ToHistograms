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

def storeHistogramAsPGM(hist, filename):
	histFile = open(filename, 'w')
	# write a valid header for a pgm image file
	# maximalValueThisHist = np.amax(hist[0])
	maximalValueThisHist = 2
	histFile.write("P2\n"+str(hist[0].shape[1])+" "+str(hist[0].shape[0])+"\n"+str(int(maximalValueThisHist))+"\n")
	# write the actual data
	for row in histIDvsT[0]:
		for entry in row:
			# write the actual values
			histFile.write(str(int(entry)) + " ")
			"""
			# or binarize the histogram 
			# Advantage: the simulation of number of PMTs could be off. this is ignore by this
			# disadvantage: only keeps the information: OM hit at that time or not
			if entry >= 1: 
				histFile.write("255 ")
			else:
				histFile.write("50 ")
			"""
		histFile.write("\n")
	histFile.close()




if len(sys.argv) < 2 or str(sys.argv[1]) == "-h":
	print "Usage: python " + str(sys.argv[0]) + " file.h5"
	sys.exit(1)

filenameBase = str(sys.argv[1])
print "Generating histograms from the hits in ID-format for files based on " + filenameBase
filenameTracks = filenameBase + "_tracks.txt"
filenameHits = filenameBase + "_hits.txt"
filenameHitsTriggered = filenameBase + "_hitsTriggered.txt"
filenameGeometry = "km3GeoOm.txt"
manuallySetNumberOfBinsInTime = 100

# read in the geometry
geo = readNumpyArrayFromFile(filenameGeometry)
domIDs = geo[:,0]
numberOfDomIDs = len(set(domIDs))

numberBinsT = manuallySetNumberOfBinsInTime
numberBinsID = numberOfDomIDs

# read in the tracks for all events
tracks = readNumpyArrayFromFile(filenameTracks)
zeniths = np.array(tracks[:,2], np.float32)
print tracks[0:5]

# read in all hits for all events
hits = readNumpyArrayFromFile(filenameHits)
# assuming the format to be: event_id dom_id channel_id time

# evaluate each event separately
allEventNumbers = set(hits[:,0])	# TODO: use the set of tracks to also include events that did not produce any hits(?)
for eventID in allEventNumbers:
	# evaluate one event
	
	# filter all hits belonging to this event
	currentHitRows = np.where(hits[:,0] == eventID)[0]
	print "... found " + str(len(currentHitRows)) + " hits for event " + str(eventID)
	curHits = hits[currentHitRows]
	
	# slice out the times of the current hits
	times = np.array(curHits[:,3], np.int32)
	timeOfFirstHit = np.amin(times)
	timesRelative = times - timeOfFirstHit
	# slice out the OM ids of the current hits
	ids = np.array(curHits[:,1], np.int32)

	# create a histogram for this event
	histIDvsT = np.histogram2d(timesRelative, ids, [numberBinsT, numberBinsID])
	# histIDvsT = np.histogram2d(times, ids, [numberBinsT, numberBinsID], [[consideredStart, consideredEnd],])

	# store the histogram to file
	histFilename = "results/hist_"+filenameTracks+"_event"+str(eventID)+"_TvsOMID.pgm"
	storeHistogramAsPGM(histIDvsT, histFilename) 





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



