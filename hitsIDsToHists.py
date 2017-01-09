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
	# print "Usage: python " + str(sys.argv[0]) + " file.h5.txt"
	# print "Usage: python " + str(sys.argv[0]) + " file.h5_tracks.txt"
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
print hits[0:35,:]
# assuming the format to be: event_id dom_id channel_id time

#TODO: evaluate each event separately

for i in range(0,len(set(hits[:,0]))):
	currentID = hits[i,0]
	# currentID = '1'
	# print currentID
	currentHitRows = np.where(hits[:,0] == currentID)[0]
	print "... found " + str(len(currentHitRows)) + " hits for index " + str(currentID)
	# print currentHitRows
	# print currentHitRows[2]
	currentHits = hits[currentHitRows]
	print currentHits

	#TODO create a histogram for this event

	histFile = open(filenameTracks+"_"+str(i).hist+"OMvsT.hist", 'w')
	
	#TODO get out the histogram for this event

	histFile.close()



times = np.array(hits[:,3], np.int32)
# print times[0:20]
# print "minimum = " + str(np.amin(times))
# print "maximum = " + str(np.amax(times))
timesRelative = times - np.amin(times)
# print timesRelative[0:20]

# print "minimum = " + str(np.amin(hitsTriggered, dtype=np.float32))

# np.histogram2d()





