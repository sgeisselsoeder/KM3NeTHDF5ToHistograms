import pandas as pd
import numpy as np
import sys
import json
import pickle

def singleStringTo2dNumpyArray(dataAsSingleString):
	# the separator used in output files between entries (e.g. whitespace, comma, tab, ...)
	s = " "	# s = "\t" s = ", "

	# print dataAsSingleString
	dataAsList = dataAsSingleString.split("\n")
	numEntries = len(dataAsList)-1

	# print dataAsList
	dataAsListList = dataAsList[0:numEntries]       # TODO investigate why the last entry of the read in list is empty
	for i in range(0,numEntries):
		dataAsListList[i] = dataAsList[i].split(s)
	# print dataAsListList

	dataAsNpArray = np.array(dataAsListList)
	# dataAsNpArray = np.array(dataAsListList, dtype=np.float32)
	# print dataAsNpArray
	# print dataAsNpArray.size
	# print dataAsNpArray.shape
	# print dataAsNpArray[:,1]
	return dataAsNpArray


if len(sys.argv) < 2 or str(sys.argv[1]) == "-h":
	print "Usage: python " + str(sys.argv[0]) + " file.h5"
	sys.exit(1)

filenameBase = str(sys.argv[1])
print "Generating histograms from the hits in ID-format for files based on " + filenameBase
filenameTracks = filenameBase + "_tracks.txt"
filenameHits = filenameBase + "_hits.txt"
filenameHitsTriggered = filenameBase + "_hitsTriggered.txt"
filenameGeometry = "km3GeoOm.txt"

# read in the geometry
geoFile = open(filenameGeometry, 'r')
geoPlain = geoFile.read()
geoFile.close()
# parse the read data to a numpy array
geo = singleStringTo2dNumpyArray(geoPlain)
# print geo[0:5,:]
# extract the relevant information from the geometry
domIDs = geo[:,0]
# print dom_ids
numberOfDomIDs = len(set(domIDs))
# print "numberOfDomIDs = " + str(numberOfDomIDs)

# read in all tracks
trackFile = open(filenameTracks, 'r')
tracksPlain = trackFile.read()
trackFile.close()
# parse the read data to a numpy array
tracks = singleStringTo2dNumpyArray(tracksPlain)
# print tracks[0:5,:]
# extract the relevant information from the tracks
zenith = np.array(tracks[:,2], np.float32)
# print zenith[0:5]

# read in all hits for all events
hitTriggeredFile = open(filenameHitsTriggered, 'r')
hitsPlain = hitTriggeredFile.read() # TODO investigate why the last entry of the read in list is empty
hitTriggeredFile.close()
# parse the read data to a numpy array
hits = singleStringTo2dNumpyArray(hitsPlain)
print hits[0:5,:]
# assuming the format to be: event_id dom_id channel_id time

numberBinsT = 100
numberBinsID = numberOfDomIDs

# evaluate each event separately
allEventNumbers = set(hits[:,0])	# TODO: use the set of tracks to also include events that did not produce any hits(?)
# for eventID in allEventNumbers:
for e in (0,1):
	eventID = str(e)
	# evaluate one event
	# print eventID
	
	# filter all hits belonging to this event
	currentHitRows = np.where(hits[:,0] == eventID)[0]
	# print "... found " + str(len(currentHitRows)) + " hits for event " + str(eventID)
	# print currentHitRows
	curHits = hits[currentHitRows]
	# print curHits
	
	# slice out the times of the current hits
	times = np.array(curHits[:,3], np.int32)
	# print times[0:20]

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

	# alternative: consider a fixed time window around the mean time of the hits
	# this probably aids the comparison between events
	meanTime = np.mean(times)
	# print meanTime
	timeWindow = 2000	# the time window to consider hits, before and after the mean time of the hits. 
				# A particle should have traversed a km^3 detector in about 4000ns, the light might be around a bit longer (prob. up to 7000)
				# Usig a fixed number of bins, a smaller time window gives a finer resolution

	consideredStart = meanTime - timeWindow
	consideredEnd = meanTime + timeWindow
	
	ids = np.array(curHits[:,1], np.int32)
	# print ids
	timesRelative = times - consideredStart
	# print timesRelative
	
	# create a histogram for this event
	histIDvsT = np.histogram2d(timesRelative, ids, [numberBinsT, numberBinsID])
	# histIDvsT = np.histogram2d(times, ids, [numberBinsT, numberBinsID], [[consideredStart, consideredEnd],])
	# print histIDvsT[0]
	# print histIDvsT[0].shape	
	# maximalValueThisHist = np.amax(histIDvsT[0])
	# print maximalValueThisHist

	# store the histogram to file
	histFilename = "hist_"+filenameTracks+"_event"+str(eventID)+"_TvsOMID.pgm"
	histFile = open(histFilename, 'w')
	# write a valid header for a pgm image file
	# histFile.write("P2\n"+str(numberBinsID)+" "+str(numberBinsT)+"\n"+str(int(maximalValueThisHist))+"\n")
	histFile.write("P2\n"+str(numberBinsID)+" "+str(numberBinsT)+"\n1\n")
	
	# binarize the histogram for the moment to only keep the information: OM hit at that time or not
	for row in histIDvsT[0]:
		for entry in row:
			if entry >= 1: 
				histFile.write("1 ")
			else:
				histFile.write("0 ")		
		histFile.write("\n")

	# np.savetxt(histFile, histIDvsT[0], fmt='%1i')

	histFile.close()

# print "minimum = " + str(np.amin(hitsTriggered, dtype=np.float32))






