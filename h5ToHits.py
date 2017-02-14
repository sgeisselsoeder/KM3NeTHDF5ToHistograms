import pandas as pd
import numpy as np
import sys

def store2dHistogramAsPGM(hist, filename):
        histFile = open(filename, 'w')
        maximalValueThisHist = np.amax(hist[0])
        # maximalValueThisHist = 2      # just to see better
        # write a valid header for a pgm image file
        histFile.write("P2\n"+str(hist[0].shape[1])+" "+str(hist[0].shape[0])+"\n"+str(int(maximalValueThisHist))+"\n")
        # write the actual data
        for row in hist[0]:
                for entry in row:
                        # write the actual values
                        histFile.write(str(int(entry)) + " ")
                histFile.write("\n")
        histFile.close()

def store2dHistogramAsCSV(hist, classValue, filename, delim = ","):
	# TODO: replace by concat and savetxt
        histFile = open(filename, 'w')
        # write the class label
        histFile.write(str(int(classValue)) + delim)
        # write the actual data
        for row in hist[0]:
                for entry in row:
                        # write the actual values
                        histFile.write(str(int(entry)) + delim)
        histFile.write("\n")
        histFile.close()

def store4dHistogramAsCSV(hist, classValue, filename, delim = ","):
        histFile = open(filename, 'w')
        # write the class label
        histFile.write(str(int(classValue)) + delim)
        # write the actual data
        for row in hist[0]:
                for secondRow in row:
                        for thirdRow in secondRow:
                                for entry in thirdRow:
                                        # write the actual values
                                        histFile.write(str(int(entry)) + delim)
        histFile.write("\n")
        histFile.close()

def store3dHistogramAsCSV(hist, classValue, filename, delim = ","):
        histFile = open(filename, 'w')
        # write the class label
        histFile.write(str(int(classValue)) + delim)
        # write the actual data
        for row in hist[0]:
                for secondRow in row:
                        for entry in secondRow:
                                # write the actual values
                                histFile.write(str(int(entry)) + delim)
        histFile.write("\n")
        histFile.close()

def store4dHistogramAsTimeSeriesOf3dHists(hist, classValue, filenameBase, delim = ","):
        # len(hist[0][0][0][0]) = time bins     len(hist[0][0][0]) = z bins     len(hist[0][0]) = y bins        len(hist[0]) = x bins
        numberOfTimeBins = len(hist[0][0][0][0])
        for time in range(0,numberOfTimeBins):
                histFile = open(filenameBase+str(time)+".csv", 'w')
                # write the class label
                histFile.write(str(int(classValue)) + delim)
                # write the actual data
                for xDim in hist[0]:
                        for yDim in xDim:
                                for zDim in yDim:
                                        entry = zDim[time]
                                        # write the actual value
                                        histFile.write(str(int(entry)) + delim)
                histFile.close()


def computeAndStore4dTo2dHistograms(curHits, numberBinsX, numberBinsY, numberBinsZ, numberBinsT, filenameOutput, classValue, delimiter = ","):
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

        # store the histograms to csv files, resulting in one file per event and histogram/projection
        store2dHistogramAsCSV(histXvsT, classValue, "results/4dTo2d/xt/hist_"+filenameOutput+"_event"+str(eventID)+"_TvsX.csv", delimiter)
        store2dHistogramAsCSV(histYvsT, classValue, "results/4dTo2d/yt/hist_"+filenameOutput+"_event"+str(eventID)+"_TvsY.csv", delimiter)
        store2dHistogramAsCSV(histZvsT, classValue, "results/4dTo2d/zt/hist_"+filenameOutput+"_event"+str(eventID)+"_TvsZ.csv", delimiter)
        store2dHistogramAsCSV(histXvsY, classValue, "results/4dTo2d/xy/hist_"+filenameOutput+"_event"+str(eventID)+"_YvsX.csv", delimiter)
        store2dHistogramAsCSV(histXvsZ, classValue, "results/4dTo2d/xz/hist_"+filenameOutput+"_event"+str(eventID)+"_ZvsX.csv", delimiter)
	store2dHistogramAsCSV(histXvsZ, classValue, "results/4dTo2d/xz/hist_"+filenameOutput+"_event"+str(eventID)+"_ZvsX.csv", delimiter)
        store2dHistogramAsCSV(histYvsZ, classValue, "results/4dTo2d/yz/hist_"+filenameOutput+"_event"+str(eventID)+"_ZvsY.csv", delimiter)

        # store the histograms to images
        #"""
        # maybe do not double the output
        store2dHistogramAsPGM(histXvsT, "results/4dTo2d/xt/hist_"+filenameOutput+"_event"+str(eventID)+"_TvsX.pgm")
        store2dHistogramAsPGM(histYvsT, "results/4dTo2d/yt/hist_"+filenameOutput+"_event"+str(eventID)+"_TvsY.pgm")
        store2dHistogramAsPGM(histZvsT, "results/4dTo2d/zt/hist_"+filenameOutput+"_event"+str(eventID)+"_TvsZ.pgm")
        store2dHistogramAsPGM(histXvsY, "results/4dTo2d/xy/hist_"+filenameOutput+"_event"+str(eventID)+"_XvsY.pgm")
        store2dHistogramAsPGM(histXvsZ, "results/4dTo2d/xz/hist_"+filenameOutput+"_event"+str(eventID)+"_XvsZ.pgm")
        store2dHistogramAsPGM(histYvsZ, "results/4dTo2d/yz/hist_"+filenameOutput+"_event"+str(eventID)+"_YvsZ.pgm")
        #"""

def computeAndStore4dTo3dHistograms(curHits, numberBinsX, numberBinsY, numberBinsZ, numberBinsT, filenameOutput, classValue, delimiter = ","):
        histXYZ = np.histogramdd( np.array(curHits[:,1:4], np.float32), [numberBinsX, numberBinsY, numberBinsZ])
        histXYT = np.histogramdd( np.array(np.concatenate([curHits[:,1:3],curHits[:,4:5]], axis=1), np.float32), [numberBinsX, numberBinsY, numberBinsT])
        histXZT = np.histogramdd( np.array(np.concatenate([curHits[:,1:2],curHits[:,3:5]], axis=1), np.float32), [numberBinsX, numberBinsZ, numberBinsT])
        histYZT = np.histogramdd( np.array(curHits[:,2:5], np.float32), [numberBinsY, numberBinsZ, numberBinsT])

        # store the 3 dimensional histograms to file
        store3dHistogramAsCSV( histXYZ, classValue, "results/4dTo3d/xyz/hist_"+filenameOutput+"_event"+str(eventID)+"_XYZ.csv", delimiter)
        store3dHistogramAsCSV( histXYT, classValue, "results/4dTo3d/xyt/hist_"+filenameOutput+"_event"+str(eventID)+"_XYT.csv", delimiter)
	store3dHistogramAsCSV( histXYT, classValue, "results/4dTo3d/xyt/hist_"+filenameOutput+"_event"+str(eventID)+"_XYT.csv", delimiter)
        store3dHistogramAsCSV( histXZT, classValue, "results/4dTo3d/xzt/hist_"+filenameOutput+"_event"+str(eventID)+"_XZT.csv", delimiter)
        store3dHistogramAsCSV( histYZT, classValue, "results/4dTo3d/yzt/hist_"+filenameOutput+"_event"+str(eventID)+"_YZT.csv", delimiter)

        # add a rotation-symmetric 3d hist
        x = np.array(curHits[:,1:2], np.float32)
        y = np.array(curHits[:,2:3], np.float32)
        r = np.sqrt(x*x + y*y)
        zt = np.array(curHits[:,3:5], np.float32)
        rzt = np.array(np.concatenate([r, zt], axis=1), np.float32)
        histRZT = np.histogramdd(rzt, [numberBinsX, numberBinsZ, numberBinsT])
        store3dHistogramAsCSV( histRZT, classValue, "results/4dTo3d/rzt/hist_"+filenameOutput+"_event"+str(eventID)+"_RZT.csv", delimiter)


def computeAndStore4dTo4dHistograms(curHits, numberBinsX, numberBinsY, numberBinsZ, numberBinsT, filenameOutput, classValue, delimiter = ","):
        curHitsWithoutEventID = np.array(curHits[:,1:5], np.float32)
        histXYZT = np.histogramdd(curHitsWithoutEventID, [numberBinsX, numberBinsY, numberBinsZ, numberBinsT])

        # store the 4 dimensional histogram to file
        store4dHistogramAsCSV( histXYZT, classValue, "results/4dTo4d/xyzt/hist_"+filenameOutput+"_event"+str(eventID)+"_XYZT.csv", delimiter)
        store4dHistogramAsTimeSeriesOf3dHists( histXYZT, classValue, "results/4dTo3dTimeSeries/xyzTimeSeries/hist_"+filenameOutput+"_event"+str(eventID)+"_XYZ", delimiter)


def computeAndStore2dTo2dHistogram(curHits, numberBinsID, numberBinsT, filenameOutput, classValue, delimiter = ","):
        # slice out the OM ids of the current hits
        ids = np.array(curHits[:,1], np.int32)

        # slice out the times of the current hits
        times = np.array(curHits[:,3], np.int32)

        # create a histogram for this event
        histIDvsT = np.histogram2d(times, ids, [numberBinsT, numberBinsID])
        # histIDvsT = np.histogram2d(times, ids, [numberBinsT, numberBinsID], [[consideredStart, consideredEnd],])

        # store the histogram to file
        #store2dHistogramAsPGM(histIDvsT,             "results/2dTo2d/omIDt/hist_"+filenameOutput+"_event"+str(eventID)+"_TvsOMID.pgm")
        store2dHistogramAsCSV(histIDvsT, classValue, "results/2dTo2d/omIDt/hist_"+filenameOutput+"_event"+str(eventID)+"_TvsOMID.csv", delimiter)

def getClassUpDown(track):
        # analyze the track info to determine the class number
        zenith = np.float32(track[4])
        classValue = int(np.sign(zenith))
        if classValue == -1:
                classValue = 0
        return classValue

def filterHitsForThisEvent(hits, eventID):
        # currentHitRows = np.where(hits[:,0] == eventID)[0]
        # print "... found " + str(len(currentHitRows)) + " hits for event " + str(eventID)
        # return hits[currentHitRows]
        return hits[ np.where(hits[:,0] == eventID)[0] ]

######### End of functions for hits to histograms ###########

def filterPrimaryTracks(tracksFull):
	# only keep tracks from primary particles, implemented as only those with bjorken-y != 0.0
	return tracksFull[ np.where( tracksFull[:,0] != 0.0)[0] ]

def extractRelevantTrackInfo(tracks):
	# keep the relevant info from the track: event_id particle_type dir_x dir_y dir_z energy isCC 
	return np.array( np.concatenate( [tracks[:,14:15],tracks[:,13:14],tracks[:,1:5],tracks[:,7:8]], axis=1), np.float32 )

def writeTracksCSV(tracksFull, filename, delim=","):
	tracksPrimary = filterPrimaryTracks(tracksFull)
	tracks = extractRelevantTrackInfo(tracksPrimary)
	np.savetxt(filename, tracks, delimiter=delim)

def filterTriggeredHits(hits):
	# only keep triggered hits
	return hits[ np.where( hits[:,13] == True)[0] ]
	# return hits[ np.where( hits[:,6] == True)[0] ]	# old numbering

def extractRelevantHitInfo(hits):
	# keep the relevant info from each hit: event_id dom_id channel_id time 
	return np.array( np.concatenate( [hits[:,14:15],hits[:,4:5],hits[:,0:1],hits[:,11:12]], axis=1), np.float32 )
	# return np.array( np.concatenate( [hits[:,7:8],hits[:,1:2],hits[:,0:1],hits[:,4:5]], axis=1), np.float32 ) # old numbering


def writeHitsCSV2(hitsBloated, filename, delim):
	hits = extractRelevantHitInfo(hitsBloated)
	np.savetxt(filename, hits, delimiter=delim)

def writeHitsCSV(hits, filename, s):
	f = open(filename+"_hits.txt", 'w')
	#fTrig = open(filename+"_hitsTriggered.txt", 'w')
	for hit in hits:
		# write: event_id dom_id channel_id time
		infoString = str(hit[7]) + s + str(hit[1]) + s + str(hit[0]) + s + str(hit[4]) + "\n"
		f.write(infoString)
		# triggered hits only:
		#if (hit[6] == True):
		#	fTrig.write(infoString)
	f.close()
	#fTrig.close()

def convertHitsXYZ(hits, geo):
        # write the hits with xyz geometry
	temp = []
        for hit in hits:
                position = geo[int(hit[1])-1]
		temp.append( [int(hit[0]), position[1], position[2], position[3], hit[3], int(hit[1])] )
	return np.array(temp)

def convertHitsXYZAndWriteCSV(hits, geo, filename, delimiter=","):
	hitsXYZ = convertHitsXYZ(hits, geo)
	np.savetxt(filename, hitsXYZ, delimiter)

def writeHitsXYZCSV(hits, geo, filename, s):
	f = open(filename+"_hitsXYZ.txt" , 'w')
        # write the hits with xyz geometry
        for hit in hits:
                position = geo[int(hit[1])-1]
                # write event_id x y z time # add the original omID to allow artificially failing oms dynamically in histogram step
                f.write(str(int(hit[0])) + s + str(position[1]) + s + str(position[2]) + s + str(position[3]) + s + str(hit[3]) + s + str(int(hit[1])) + "\n")
        f.close()







#### main start here ;-) ######



if len(sys.argv) < 2 or str(sys.argv[1]) == "-h":
	print "Usage: python " + str(sys.argv[0]) + " file.h5"
	sys.exit(1)

filename = str(sys.argv[1])
print "Extracting hits and tracks from hdf5 file " + filename
filenameGeometry = "km3GeoOm.txt"
print "Reading detector geometry from file " + filenameGeometry
geo = np.loadtxt(filenameGeometry)

# the separator used in output files between entries (e.g. whitespace, comma, tab, ...)
delim = ","

print "Reading tracks"
tracks = np.array( pd.read_hdf(filename, 'mc_tracks') )
#print "Writing tracks"
#writeTracksCSV(tracks, filename+"_tracks.csv.gz", delim)

print "Reading hits"
hits = extractRelevantHitInfo( np.array( pd.read_hdf(filename, 'hits') ) )
#hitsBloated = np.array( pd.read_hdf(filename, 'hits') )
#hits = extractRelevantHitInfo(hitsBloated)
allEventNumbers = set(hits[:,0])

# print "Writing hits omid"
# np.savetxt(filename+"_hits.csv.gz", hits, delimiter=delim)

# print "Converting hits omid -> XYZ"
hitsXYZ = convertHitsXYZ(hits, geo)
# print "Writing hits XYZ"
# np.savetxt(filename+"_hitsXYZ.csv.gz", hitsXYZ, delimiter=delim)


# not working yet
"""
# optionally: determine artificially failing oms
faultProbability = 0.1
numOMs = len(geo)
offlineOMs = []
for i in range(0,int(numOMs*faultProbability)):
        offlineOMs.append(randint(0,numOMs))
#print faultProbability
#print offlineOMs
#"""
"""
# only required if artificial om failures are desired:
temp = np.where(not hits[:,5] in offlineOMs)
print temp

survivingHitRows = np.where(not hits[:,5] in offlineOMs)[0]
print survivingHitRows
survivingHits = hits[survivingHitRows]
print len(hits), len(survivingHits)

# survivingHits = hits[ np.where(not hits[:,5] in offlineOMs)[0] ]
# print len(hits), len(survivingHits)
sys.exit()
"""

# the number of bins could partially also be deduced from the geometry
numberBinsT = 100       # number of bins in time
numberBinsX = 11        # number of bins in x
numberBinsY = 11        # number of bins in y
numberBinsZ = 18        # number of bins in z
# determine the number of bins as the number of OM ids found in the geometry file
numberBinsID = len(set(geo[:,0]))
filenameOutput = filename.replace("/","_").replace(".","_")


print "Generating histograms from the hits in OMID versus time format for files based on " + filename
# Evaluate one event at a time
for eventID in allEventNumbers:
        # Determine the class of this event
        classValue = getClassUpDown( tracks[int(eventID)] )

        # filter all hits belonging to this event
        curHits = filterHitsForThisEvent(hits, eventID)

        # Do the 2dTo2dHistogram
        computeAndStore2dTo2dHistogram(curHits, numberBinsID, numberBinsT, filenameOutput, classValue, delimiter)


print "Generating histograms from the hits in XYZT format for files based on " + filename
# Evaluate one event at a time
for eventID in allEventNumbers:
        # Determine the class of this event
        classValue = getClassUpDown( tracks[int(eventID)] )

        # filter all hits belonging to this event
        curHits = filterHitsForThisEvent(hitsXYZ, eventID)

        # do the 2d histograms 
        computeAndStore4dTo2dHistograms(curHits, numberBinsX, numberBinsY, numberBinsZ, numberBinsT, filenameOutput, classValue, delim)

        # do the 3d histograms
        computeAndStore4dTo3dHistograms(curHits, numberBinsX, numberBinsY, numberBinsZ, numberBinsT, filenameOutput, classValue, delim)

        # do the 4d and 3d time series histograms 
        # works but produces giant output files and is not required for now
        computeAndStore4dTo4dHistograms(curHits, numberBinsX, numberBinsY, numberBinsZ, numberBinsT, filenameOutput, classValue, delim)




