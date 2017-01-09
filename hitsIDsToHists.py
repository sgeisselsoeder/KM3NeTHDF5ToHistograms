import pandas as pd
import numpy as np
import sys
import json
import pickle

def singleStringTo2dNumpyArray(dataAsSingleString):
	# print dataAsSingleString
	dataAsList = dataAsSingleString.split("\n")
	numEntries = len(dataAsList)-1

	# print dataAsList
	dataAsListList = dataAsList[0:numEntries]       # TODO investigate why the last entry of the read in list is empty
	for i in range(0,numEntries):
		dataAsListList[i] = dataAsList[i].split(" ")
	# print dataAsListList

	dataAsNpArray = np.array(dataAsListList)
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
# the separator used in output files between entries (e.g. whitespace, comma, tab, ...)
s = " "	# s = "\t" s = ", "


geoFile = open(filenameGeometry, 'r')
geoPlain = geoFile.read()
geoFile.close()
geo = singleStringTo2dNumpyArray(geoPlain)
# print geo

for position in geo:
	print "Position is " + str(position) + "\n"
print geo.shape
dom_ids = geo[0]
print dom_ids
number_of_dom_ids = len(set(dom_ids))
print number_of_dom_ids

"""
trackFile = open(filenameTracks, 'r')
tracksPlain = trackFile.read()
trackFile.close()
tracks = np.array(tracksPlain)
"""

hitTriggeredFile = open(filenameHitsTriggered, 'r')
hitsTriggeredPlain = hitTriggeredFile.read() # TODO investigate why the last entry of the read in list is empty
hitTriggeredFile.close()
hitsTriggered = singleStringTo2dNumpyArray(hitsTriggeredPlain)

# print hitsTriggeredPlain
hitsAsList = hitsTriggeredPlain.split("\n")
numEntries = len(hitsAsList)-1

# print hitsAsList
hitsAsListList = hitsAsList[0:numEntries]	# TODO investigate why the last entry of the read in list is empty
for i in range(0,numEntries):
	hitsAsListList[i] = hitsAsList[i].split(" ")
# print hitsAsListList

hitsTriggered = np.array(hitsAsListList)
# print hitsTriggered.size
# print hitsTriggered.shape
# print hitsTriggered
# print hitsTriggered[:,2]
print hitsTriggered[0:5,:]

# assuming the format to be: event_id dom_id channel_id time

# np.histogram2d()





