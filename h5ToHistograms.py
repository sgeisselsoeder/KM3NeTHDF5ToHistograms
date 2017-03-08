import pandas as pd
import numpy as np
import sys
from hitsToHistograms import *
from histogramsToFiles import *

def filterPrimaryTracks(tracksFull):
        # only keep tracks from primary particles, implemented as only those with bjorken-y != 0.0
        return tracksFull[ np.where( tracksFull[:,0] != 0.0)[0] ]

def extractRelevantTrackInfo(tracks):
        # keep the relevant info from the track: event_id particle_type dir_x dir_y dir_z energy isCC 
        return np.array( np.concatenate( [tracks[:,14:15],tracks[:,13:14],tracks[:,1:5],tracks[:,7:8]], axis=1), np.float32 )

def filterTriggeredHits(hits):
        # only keep triggered hits
        return hits[ np.where( hits[:,13] == True)[0] ]
        # return hits[ np.where( hits[:,6] == True)[0] ]        # old numbering

def extractRelevantHitInfo(hits):
        # keep the relevant info from each hit: event_id dom_id channel_id time 
        return np.array( np.concatenate( [hits[:,14:15],hits[:,4:5],hits[:,0:1],hits[:,11:12]], axis=1), np.float32 )
        # return np.array( np.concatenate( [hits[:,7:8],hits[:,1:2],hits[:,0:1],hits[:,4:5]], axis=1), np.float32 ) # old numbering

def convertHitsXYZ(hits, geo):
        # write the hits with xyz geometry
        temp = []
        for hit in hits:
                position = geo[int(hit[1])-1]
                temp.append( [int(hit[0]), position[1], position[2], position[3], hit[3], int(hit[1])] )
        return np.array(temp)
        
def getClassUpDown(track):
        # analyze the track info to determine the class number
        zenith = np.float32(track[4])
        classValue = int(np.sign(zenith))
        if classValue == -1:
                classValue = 0
        return classValue

def filterHitsForThisEvent(hits, eventID):
        return hits[ np.where(hits[:,0] == eventID)[0] ]



#### main starts here ######

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
tracksFull = np.array( pd.read_hdf(filename, 'mc_tracks') )
print "Filtering primary tracks"
tracksPrimary = filterPrimaryTracks(tracksFull)
print "Filtering relevant info for each track"
tracks = extractRelevantTrackInfo(tracksPrimary)
#print "Writing tracks"
#np.savetxt(filename+"_tracks.csv.gz", tracks, delimiter=delim)

print "Reading hits"
hits = extractRelevantHitInfo( np.array( pd.read_hdf(filename, 'hits') ) )
#hitsBloated = np.array( pd.read_hdf(filename, 'hits') )
#hits = extractRelevantHitInfo(hitsBloated)
allEventNumbers = set(hits[:,0])

# print "Writing hits omid"
# np.savetxt(filename+"_hits.csv.gz", hits, delimiter=delim)

print "Converting hits omid -> XYZ"
hitsXYZ = convertHitsXYZ(hits, geo)
# print "Writing hits XYZ"
# np.savetxt(filename+"_hitsXYZ.csv.gz", hitsXYZ, delimiter=delim)

# Start output related work here
numberBinsT = 100       # number of bins in time
numberBinsX = 11        # number of bins in x
numberBinsY = 11        # number of bins in y
numberBinsZ = 18        # number of bins in z
# determine the number of bins as the number of OM ids found in the geometry file
numberBinsID = len(set(geo[:,0]))
filenameOutput = filename.replace("/","_").replace(".","_")

print "Done converting."


print "Generating histograms from the hits in XYZT format for files based on " + filename

allClassValues = []
all4dTo2dHistograms = []
all4dTo4dHistograms = []
all4dTo3dHistogramsXYZ = []
all4dTo3dHistogramsXYT = []
all4dTo3dHistogramsXZT = []
all4dTo3dHistogramsYZT = []
all4dTo3dHistogramsRZT = []

# Evaluate one event at a time
#for eventID in [1,2]:
for eventID in allEventNumbers:
        # Determine the class of this event
        allClassValues.append(getClassUpDown( tracks[int(eventID)] ))

        # filter all hits belonging to this event
        curHits = filterHitsForThisEvent(hitsXYZ, eventID)

        # do the 2d histograms 
        # compute4dTo2dHistograms(curHits, numberBinsX, numberBinsY, numberBinsZ, numberBinsT)
        
        # do the 3d histograms
        compute4dTo3dHistograms(curHits, numberBinsX, numberBinsY, numberBinsZ, numberBinsT)

        # do the 4d and 3d time series histograms 
        # works but produces giant output files and is not required for now
        # compute4dTo4dHistograms(curHits, numberBinsX, numberBinsY, numberBinsZ, numberBinsT)

"""
print "Storing 2d histograms from xyzt hits to results/4dTo2d/*/hist_"+filenameOutput+"_*.csv"
store2dHistogramsAsCSV(allClassValues, np.array(all4dTo2dHistograms)[:,0], "results/4dTo2d/xt/hist_"+filenameOutput+"_xt.csv")
store2dHistogramsAsCSV(allClassValues, np.array(all4dTo2dHistograms)[:,1], "results/4dTo2d/yt/hist_"+filenameOutput+"_yt.csv")
store2dHistogramsAsCSV(allClassValues, np.array(all4dTo2dHistograms)[:,2], "results/4dTo2d/zt/hist_"+filenameOutput+"_zt.csv")
store2dHistogramsAsCSV(allClassValues, np.array(all4dTo2dHistograms)[:,3], "results/4dTo2d/xy/hist_"+filenameOutput+"_xy.csv")
store2dHistogramsAsCSV(allClassValues, np.array(all4dTo2dHistograms)[:,4], "results/4dTo2d/xz/hist_"+filenameOutput+"_xz.csv")
store2dHistogramsAsCSV(allClassValues, np.array(all4dTo2dHistograms)[:,5], "results/4dTo2d/yz/hist_"+filenameOutput+"_yz.csv")
# """

print "Storing 3d histograms from xyzt hits to results/4dTo3d/*/hist_"+filenameOutput+"_*.csv"
store3dHistogramsAsCSV(allClassValues, np.array(all4dTo3dHistogramsXYZ), "results/4dTo3d/xyz/hist_"+filenameOutput+"_xyz.csv")
store3dHistogramsAsCSV(allClassValues, np.array(all4dTo3dHistogramsXYT), "results/4dTo3d/xyt/hist_"+filenameOutput+"_xyt.csv")
store3dHistogramsAsCSV(allClassValues, np.array(all4dTo3dHistogramsXZT), "results/4dTo3d/xzt/hist_"+filenameOutput+"_xzt.csv")
store3dHistogramsAsCSV(allClassValues, np.array(all4dTo3dHistogramsYZT), "results/4dTo3d/yzt/hist_"+filenameOutput+"_yzt.csv")
store3dHistogramsAsCSV(allClassValues, np.array(all4dTo3dHistogramsRZT), "results/4dTo3d/rzt/hist_"+filenameOutput+"_rzt.csv")

"""
print "Storing 4d histograms from xyzt hits to results/4dTo3d/xyzt/hist_"+filenameOutput+"_xyzt.csv"
store4dHistogramsAsCSV(allClassValues, np.array(all4dTo4dHistograms), "results/4dTo4d/xyzt/hist_"+filenameOutput+"_xyzt.csv")
# """



"""
print "Generating histograms from the hits in OMID versus time format for files based on " + filename

allClassValues = []
all2dTo2dHistograms = []

# Evaluate one event at a time
for eventID in allEventNumbers:
        # Determine the class of this event
        allClassValues.append(getClassUpDown( tracks[int(eventID)] ))

        # filter all hits belonging to this event
        curHits = filterHitsForThisEvent(hits, eventID)

        # Do the 2dTo2dHistogram
        compute2dTo2dHistogram(curHits, numberBinsID, numberBinsT)

print "Storing 2d histograms from omidt hits to results/2dTo2d/omIDt/hist_"+filenameOutput+"_omidt.csv"
store2dHistogramsAsCSV(allClassValues, np.array(all2dTo2dHistograms), "results/2dTo2d/omIDt/hist_"+filenameOutput+"_omidt.csv")
"""


