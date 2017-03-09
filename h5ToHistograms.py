import pandas as pd
import numpy as np
import sys
from fileToHits import *
from hitsToHistograms import *
from histogramsToFiles import *

def getClassUpDown(track):
        # analyze the track info to determine the class number
        zenith = np.float32(track[4])
        classValue = int(np.sign(zenith))
        if classValue == -1:
                classValue = 0
        return classValue

def filterHitsForThisEvent(hits, eventID):
        return hits[ np.where(hits[:,0] == eventID)[0] ]


if len(sys.argv) < 2 or str(sys.argv[1]) == "-h":
        print "Usage: python " + str(sys.argv[0]) + " file.h5"
        sys.exit(1)

filename = str(sys.argv[1])
filenameOutput = filename.replace("/","_").replace(".","_")
filenameGeometry = "km3GeoOm.txt"

track, hits, hitsXYZ = parseFile(filename, filenameGeometry)
# trackInfo contains the relevant info on the events: event_id particle_type dir_x dir_y dir_z energy isCC 
allEventNumbers = set(hits[:,0])

# Start output related work here
numberBinsT = 100       # number of bins in time
numberBinsX = 11        # number of bins in x
numberBinsY = 11        # number of bins in y
numberBinsZ = 18        # number of bins in z
numberBinsID = 2070	# number of optical modules

# Determine the class(es) for each event, also keep the MC info for regression
mcinfos = []
for eventID in allEventNumbers:
	mcinfo = np.reshape( track[int(eventID)], len( track[int(eventID)] ), 1 )	# usually this is sorted, but we go for the indices to make sure
	updown = np.reshape( np.array(getClassUpDown(mcinfo)), 1,1)	# also add up/down binary class info (redundant with zenith, but simplifies later work)
	allmcinfo = np.concatenate( [mcinfo, updown]) 
	numEntries = np.reshape( np.array(len(allmcinfo)), 1,1 )	# count the number of mcinfo-related entries, make this the first number
									# - cannot be mistaken for class number (all the same)
									# - allows to parse a file without exact knowledge
	mcinfos.append( np.concatenate( [numEntries, allmcinfo]) )

print "Generating histograms from the hits in XYZT format for files based on " + filename
all4dTo2dHistograms = []
# all4dTo3dHistograms = [] # doesn't work # TODO make it work
all4dTo4dHistograms = []
all4dTo3dHistogramsXYZ = []
all4dTo3dHistogramsXYT = []
all4dTo3dHistogramsXZT = []
all4dTo3dHistogramsYZT = []
all4dTo3dHistogramsRZT = []

# Evaluate one event at a time
# for eventID in [1,2]:
for eventID in allEventNumbers:
        # filter all hits belonging to this event
        curHits = filterHitsForThisEvent(hitsXYZ, eventID)

        # do the 2d histograms 
        compute4dTo2dHistograms(curHits, numberBinsX, numberBinsY, numberBinsZ, numberBinsT, all4dTo2dHistograms)
        
        # do the 3d histograms
        compute4dTo3dHistograms(curHits, numberBinsX, numberBinsY, numberBinsZ, numberBinsT, all4dTo3dHistogramsXYZ, all4dTo3dHistogramsXYT, all4dTo3dHistogramsXZT, all4dTo3dHistogramsYZT, all4dTo3dHistogramsRZT)

        # do the 4d (same info as time series of 3d) histograms 
        # works but produces giant output files
        compute4dTo4dHistograms(curHits, numberBinsX, numberBinsY, numberBinsZ, numberBinsT, all4dTo4dHistograms)

# """
print "Storing 2d histograms from xyzt hits to results/4dTo2d/*/hist_"+filenameOutput+"_*.csv"
store2dHistogramsAsCSV(mcinfos, np.array(all4dTo2dHistograms)[:,0], "results/4dTo2d/xt/hist_"+filenameOutput+"_xt.csv")
store2dHistogramsAsCSV(mcinfos, np.array(all4dTo2dHistograms)[:,1], "results/4dTo2d/yt/hist_"+filenameOutput+"_yt.csv")
store2dHistogramsAsCSV(mcinfos, np.array(all4dTo2dHistograms)[:,2], "results/4dTo2d/zt/hist_"+filenameOutput+"_zt.csv")
store2dHistogramsAsCSV(mcinfos, np.array(all4dTo2dHistograms)[:,3], "results/4dTo2d/xy/hist_"+filenameOutput+"_xy.csv")
store2dHistogramsAsCSV(mcinfos, np.array(all4dTo2dHistograms)[:,4], "results/4dTo2d/xz/hist_"+filenameOutput+"_xz.csv")
store2dHistogramsAsCSV(mcinfos, np.array(all4dTo2dHistograms)[:,5], "results/4dTo2d/yz/hist_"+filenameOutput+"_yz.csv")
#store2dHistogramsAsBinary(mcinfos, np.array(all4dTo2dHistograms)[:,3], "results/4dTo2d/xy/hist_"+filenameOutput+"_xy.csv")
# """
#"""
print "Storing 3d histograms from xyzt hits to results/4dTo3d/*/hist_"+filenameOutput+"_*.csv"
store3dHistogramsAsCSV(mcinfos, np.array(all4dTo3dHistogramsXYZ), "results/4dTo3d/xyz/hist_"+filenameOutput+"_xyz.csv")
store3dHistogramsAsCSV(mcinfos, np.array(all4dTo3dHistogramsXYT), "results/4dTo3d/xyt/hist_"+filenameOutput+"_xyt.csv")
store3dHistogramsAsCSV(mcinfos, np.array(all4dTo3dHistogramsXZT), "results/4dTo3d/xzt/hist_"+filenameOutput+"_xzt.csv")
store3dHistogramsAsCSV(mcinfos, np.array(all4dTo3dHistogramsYZT), "results/4dTo3d/yzt/hist_"+filenameOutput+"_yzt.csv")
store3dHistogramsAsCSV(mcinfos, np.array(all4dTo3dHistogramsRZT), "results/4dTo3d/rzt/hist_"+filenameOutput+"_rzt.csv")
# """
#"""
print "Storing 4d histograms from xyzt hits to results/4dTo3d/xyzt/hist_"+filenameOutput+"_xyzt.csv"
store4dHistogramsAsCSV(mcinfos, np.array(all4dTo4dHistograms), "results/4dTo4d/xyzt/hist_"+filenameOutput+"_xyzt.csv")
# """


"""
print "Generating histograms from the hits in OMID versus time format for files based on " + filename
all2dTo2dHistograms = []

# Evaluate one event at a time
for eventID in allEventNumbers:
        # filter all hits belonging to this event
        curHits = filterHitsForThisEvent(hits, eventID)

        # Do the 2dTo2dHistogram
        compute2dTo2dHistogram(curHits, numberBinsID, numberBinsT, all2dTo2dHistograms)

print "Storing 2d histograms from omidt hits to results/2dTo2d/omIDt/hist_"+filenameOutput+"_omidt.csv"
store2dHistogramsAsCSV(mcinfos, np.array(all2dTo2dHistograms), "results/2dTo2d/omIDt/hist_"+filenameOutput+"_omidt.csv")
# """


