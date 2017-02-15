
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
import sys

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


# In[8]:

#### main starts here ;-) ######

if len(sys.argv) < 2 or str(sys.argv[1]) == "-h":
        print "Usage: python " + str(sys.argv[0]) + " file.h5"
        sys.exit(1)

filename = str(sys.argv[1])
#filename = "data.h5"
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

# print "Converting hits omid -> XYZ"
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



# In[3]:

def store2dHistogramAsPGM(hist, filename):
        histFile = open(filename, 'w')
        maximalValueThisHist = np.amax(hist[0])
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
        #test = np.reshape( hist[0], (len(hist[0])*len(hist[0][0]),1) )
        #test2 = np.append(np.array([classValue,]), test)
        #np.savetxt(filename, test2[np.newaxis], delimiter=delim)
        np.savetxt(filename, np.append(np.array([classValue,]), np.reshape( hist[0], (len(hist[0])*len(hist[0][0]),1) ) )[np.newaxis], delimiter=delim, fmt='%d')

#def store2dHistogramAsCSV(hist, classValue, filename, delim = ","):
#        histFile = open(filename, 'w')
#        # write the class label
#        histFile.write(str(int(classValue)) + delim)
#        # write the actual data
#        for row in hist[0]:
#                for entry in row:
#                        # write the actual values
#                        histFile.write(str(int(entry)) + delim)
#        histFile.write("\n")
#        histFile.close()

def store3dHistogramAsCSV(hist, classValue, filename, delim = ","):
        np.savetxt(filename, np.append(np.array([classValue,]), np.reshape( hist[0], (len(hist[0])*len(hist[0][0])*len(hist[0][0][0]),1) ) )[np.newaxis], delimiter=delim, fmt='%d')

def store4dHistogramAsCSV(hist, classValue, filename, delim = ","):
        np.savetxt(filename, np.append(np.array([classValue,]), np.reshape( hist[0], (len(hist[0])*len(hist[0][0])*len(hist[0][0][0])*len(hist[0][0][0][0]),1) ) )[np.newaxis], delimiter=delim, fmt='%d')

def store3dHistogramSpliceAsCSV(hist, classValue, filename, delim = ","):
        np.savetxt(filename, np.append(np.array([classValue,]), np.reshape( hist, (len(hist)*len(hist[0])*len(hist[0][0]),1) ) )[np.newaxis], delimiter=delim, fmt='%d')

def store4dHistogramAsTimeSeriesOf3dHists(hist, classValue, filenameBase, delim = ","):
        # len(hist[0][0][0][0]) = time bins     len(hist[0][0][0]) = z bins     len(hist[0][0]) = y bins        len(hist[0]) = x bins
        numberOfTimeBins = len(hist[0][0][0][0])
        for time in range(0,numberOfTimeBins):
                filenameCurrent=filenameBase+"_"+str(time)+".csv"
                store3dHistogramSpliceAsCSV(hist[0][:,:,:,time], classValue, filenameCurrent, delim)

                
def compute4dTo2dHistograms(curHits, numberBinsX, numberBinsY, numberBinsZ, numberBinsT):
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
        
        all4dTo2dHistograms.append([histXvsT[0], histYvsT[0], histZvsT[0], histXvsY[0], histXvsZ[0], histYvsZ[0]])
        
        # store the histograms to images   # commented out by default to not double the output
        """
        store2dHistogramAsPGM(histXvsT, "results/4dTo2d/xt/hist_"+filenameOutput+"_event"+str(eventID)+"_TvsX.pgm")
        store2dHistogramAsPGM(histYvsT, "results/4dTo2d/yt/hist_"+filenameOutput+"_event"+str(eventID)+"_TvsY.pgm")
        store2dHistogramAsPGM(histZvsT, "results/4dTo2d/zt/hist_"+filenameOutput+"_event"+str(eventID)+"_TvsZ.pgm")
        store2dHistogramAsPGM(histXvsY, "results/4dTo2d/xy/hist_"+filenameOutput+"_event"+str(eventID)+"_XvsY.pgm")
        store2dHistogramAsPGM(histXvsZ, "results/4dTo2d/xz/hist_"+filenameOutput+"_event"+str(eventID)+"_XvsZ.pgm")
        store2dHistogramAsPGM(histYvsZ, "results/4dTo2d/yz/hist_"+filenameOutput+"_event"+str(eventID)+"_YvsZ.pgm")
        #"""

"""        
def computeAndStore4dTo2dHistograms(eventID, curHits, numberBinsX, numberBinsY, numberBinsZ, numberBinsT, filenameOutput, classValue, delim = ","):
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
        store2dHistogramAsCSV(histXvsT, classValue, "results/4dTo2d/xt/hist_"+filenameOutput+"_event"+str(eventID)+"_TvsX.csv", delim)
        store2dHistogramAsCSV(histYvsT, classValue, "results/4dTo2d/yt/hist_"+filenameOutput+"_event"+str(eventID)+"_TvsY.csv", delim)
        store2dHistogramAsCSV(histZvsT, classValue, "results/4dTo2d/zt/hist_"+filenameOutput+"_event"+str(eventID)+"_TvsZ.csv", delim)
        store2dHistogramAsCSV(histXvsY, classValue, "results/4dTo2d/xy/hist_"+filenameOutput+"_event"+str(eventID)+"_YvsX.csv", delim)
        store2dHistogramAsCSV(histXvsZ, classValue, "results/4dTo2d/xz/hist_"+filenameOutput+"_event"+str(eventID)+"_ZvsX.csv", delim)
        store2dHistogramAsCSV(histYvsZ, classValue, "results/4dTo2d/yz/hist_"+filenameOutput+"_event"+str(eventID)+"_ZvsY.csv", delim)

        # store the histograms to images   # commented out by default to not double the output
        " ""
        store2dHistogramAsPGM(histXvsT, "results/4dTo2d/xt/hist_"+filenameOutput+"_event"+str(eventID)+"_TvsX.pgm")
        store2dHistogramAsPGM(histYvsT, "results/4dTo2d/yt/hist_"+filenameOutput+"_event"+str(eventID)+"_TvsY.pgm")
        store2dHistogramAsPGM(histZvsT, "results/4dTo2d/zt/hist_"+filenameOutput+"_event"+str(eventID)+"_TvsZ.pgm")
        store2dHistogramAsPGM(histXvsY, "results/4dTo2d/xy/hist_"+filenameOutput+"_event"+str(eventID)+"_XvsY.pgm")
        store2dHistogramAsPGM(histXvsZ, "results/4dTo2d/xz/hist_"+filenameOutput+"_event"+str(eventID)+"_XvsZ.pgm")
        store2dHistogramAsPGM(histYvsZ, "results/4dTo2d/yz/hist_"+filenameOutput+"_event"+str(eventID)+"_YvsZ.pgm")
        #" ""
"""

def compute4dTo3dHistograms(curHits, numberBinsX, numberBinsY, numberBinsZ, numberBinsT):
        histXYZ = np.histogramdd( np.array(curHits[:,1:4], np.float32), [numberBinsX, numberBinsY, numberBinsZ])
        histXYT = np.histogramdd( np.array(np.concatenate([curHits[:,1:3],curHits[:,4:5]], axis=1), np.float32), [numberBinsX, numberBinsY, numberBinsT])
        histXZT = np.histogramdd( np.array(np.concatenate([curHits[:,1:2],curHits[:,3:5]], axis=1), np.float32), [numberBinsX, numberBinsZ, numberBinsT])
        histYZT = np.histogramdd( np.array(curHits[:,2:5], np.float32), [numberBinsY, numberBinsZ, numberBinsT])

        # add a rotation-symmetric 3d hist
        x = np.array(curHits[:,1:2], np.float32)
        y = np.array(curHits[:,2:3], np.float32)
        r = np.sqrt(x*x + y*y)
        zt = np.array(curHits[:,3:5], np.float32)
        rzt = np.array(np.concatenate([r, zt], axis=1), np.float32)
        histRZT = np.histogramdd(rzt, [numberBinsX, numberBinsZ, numberBinsT])

        #all4dTo3dHistograms.append( [histXYZ[0], histXYT[0], histXZT[0], histYZT[0], histRZT[0]] )
        all4dTo3dHistogramsXYZ.append( histXYZ[0] )
        all4dTo3dHistogramsXYT.append( histXYT[0] )
        all4dTo3dHistogramsXZT.append( histXZT[0] )
        all4dTo3dHistogramsYZT.append( histYZT[0] )
        all4dTo3dHistogramsRZT.append( histRZT[0] )

"""        
def computeAndStore4dTo3dHistograms(curHits, numberBinsX, numberBinsY, numberBinsZ, numberBinsT, filenameOutput, classValue, delim = ","):
        histXYZ = np.histogramdd( np.array(curHits[:,1:4], np.float32), [numberBinsX, numberBinsY, numberBinsZ])
        histXYT = np.histogramdd( np.array(np.concatenate([curHits[:,1:3],curHits[:,4:5]], axis=1), np.float32), [numberBinsX, numberBinsY, numberBinsT])
        histXZT = np.histogramdd( np.array(np.concatenate([curHits[:,1:2],curHits[:,3:5]], axis=1), np.float32), [numberBinsX, numberBinsZ, numberBinsT])
        histYZT = np.histogramdd( np.array(curHits[:,2:5], np.float32), [numberBinsY, numberBinsZ, numberBinsT])

        # store the 3 dimensional histograms to file
        store3dHistogramAsCSV( histXYZ, classValue, "results/4dTo3d/xyz/hist_"+filenameOutput+"_event"+str(eventID)+"_XYZ.csv", delim)
        store3dHistogramAsCSV( histXYT, classValue, "results/4dTo3d/xyt/hist_"+filenameOutput+"_event"+str(eventID)+"_XYT.csv", delim)
        store3dHistogramAsCSV( histXZT, classValue, "results/4dTo3d/xzt/hist_"+filenameOutput+"_event"+str(eventID)+"_XZT.csv", delim)
        store3dHistogramAsCSV( histYZT, classValue, "results/4dTo3d/yzt/hist_"+filenameOutput+"_event"+str(eventID)+"_YZT.csv", delim)

        # add a rotation-symmetric 3d hist
        x = np.array(curHits[:,1:2], np.float32)
        y = np.array(curHits[:,2:3], np.float32)
        r = np.sqrt(x*x + y*y)
        zt = np.array(curHits[:,3:5], np.float32)
        rzt = np.array(np.concatenate([r, zt], axis=1), np.float32)
        histRZT = np.histogramdd(rzt, [numberBinsX, numberBinsZ, numberBinsT])
        store3dHistogramAsCSV( histRZT, classValue, "results/4dTo3d/rzt/hist_"+filenameOutput+"_event"+str(eventID)+"_RZT.csv", delim)
"""

def compute4dTo4dHistograms(curHits, numberBinsX, numberBinsY, numberBinsZ, numberBinsT):
        curHitsWithoutEventID = np.array(curHits[:,1:5], np.float32)
        histXYZT = np.histogramdd(curHitsWithoutEventID, [numberBinsX, numberBinsY, numberBinsZ, numberBinsT])

        all4dTo4dHistograms.append(histXYZT[0])
        # TODO: also save all the 3d time series ... or do this at output level ...       
        # store4dHistogramAsTimeSeriesOf3dHists( histXYZT, classValue, "results/4dTo3dTimeSeries/xyzTimeSeries/hist_"+filenameOutput+"_event"+str(eventID)+"_XYZ", delim)

"""
def computeAndStore4dTo4dHistograms(curHits, numberBinsX, numberBinsY, numberBinsZ, numberBinsT, filenameOutput, classValue, delim = ","):
        curHitsWithoutEventID = np.array(curHits[:,1:5], np.float32)
        histXYZT = np.histogramdd(curHitsWithoutEventID, [numberBinsX, numberBinsY, numberBinsZ, numberBinsT])

        # store the 4 dimensional histogram to file
        store4dHistogramAsCSV( histXYZT, classValue, "results/4dTo4d/xyzt/hist_"+filenameOutput+"_event"+str(eventID)+"_XYZT.csv", delim)
        store4dHistogramAsTimeSeriesOf3dHists( histXYZT, classValue, "results/4dTo3dTimeSeries/xyzTimeSeries/hist_"+filenameOutput+"_event"+str(eventID)+"_XYZ", delim)
"""

def compute2dTo2dHistogram(curHits, numberBinsID, numberBinsT):
        # slice out the OM ids of the current hits
        ids = np.array(curHits[:,1], np.int32)

        # slice out the times of the current hits
        times = np.array(curHits[:,3], np.int32)

        # create a histogram for this event
        histIDvsT = np.histogram2d(times, ids, [numberBinsT, numberBinsID])
        # histIDvsT = np.histogram2d(times, ids, [numberBinsT, numberBinsID], [[consideredStart, consideredEnd],])
        
        all2dTo2dHistograms.append(histIDvsT[0])
        #store2dHistogramAsPGM(histIDvsT, "results/2dTo2d/omIDt/hist_"+filenameOutput+"_event"+str(eventID)+"_TvsOMID.pgm")
        
"""     
def computeAndStore2dTo2dHistogram(curHits, numberBinsID, numberBinsT, filenameOutput, classValue, delim = ","):
        # slice out the OM ids of the current hits
        ids = np.array(curHits[:,1], np.int32)

        # slice out the times of the current hits
        times = np.array(curHits[:,3], np.int32)

        # create a histogram for this event
        histIDvsT = np.histogram2d(times, ids, [numberBinsT, numberBinsID])
        # histIDvsT = np.histogram2d(times, ids, [numberBinsT, numberBinsID], [[consideredStart, consideredEnd],])

        # store the histogram to file
        #store2dHistogramAsPGM(histIDvsT,             "results/2dTo2d/omIDt/hist_"+filenameOutput+"_event"+str(eventID)+"_TvsOMID.pgm")
        store2dHistogramAsCSV(histIDvsT, classValue, "results/2dTo2d/omIDt/hist_"+filenameOutput+"_event"+str(eventID)+"_TvsOMID.csv", delim)
"""
        
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


# In[4]:

def store2dHistogramsAsCSV(classValues, hists, filename, delim = ","):
        # TODO: convert this to more efficient savetxt version
        histFile = open(filename, 'w')
        # loop over all histograms (= events)
        #for hist,classVal in hists,classValues:
        for i in range(0,len(hists)):
            # write out one line per event
            # write the class of this event first
            histFile.write(str(int(classValues[i])) + delim)
            # then write the data of this event
            for row in hists[i]:
                for entry in row:
                    # write the actual values
                    histFile.write(str(int(entry)) + delim)
            histFile.write("\n")
        histFile.close()
        
def store3dHistogramsAsCSV(classValues, hists, filename, delim = ","):
        # TODO: convert this to more efficient savetxt version
        histFile = open(filename, 'w')
        # loop over all histograms (= events)
        #for hist,classVal in hists,classValues:
        for i in range(0,len(hists)):
            # write out one line per event
            # write the class of this event first
            histFile.write(str(int(classValues[i])) + delim)
            # then write the data of this event
            for row in hists[i]:
                for row2 in row:
                    for entry in row2:
                        # write the actual values
                        histFile.write(str(int(entry)) + delim)
            histFile.write("\n")
        histFile.close()
        
def store4dHistogramsAsCSV(classValues, hists, filename, delim = ","):
        # TODO: convert this to more efficient savetxt version
        histFile = open(filename, 'w')
        # loop over all histograms (= events)
        #for hist,classVal in hists,classValues:
        for i in range(0,len(hists)):
            # write out one line per event
            # write the class of this event first
            histFile.write(str(int(classValues[i])) + delim)
            # then write the data of this event
            for row in hists[i]:
                for row2 in row:
                    for row3 in row2:
                        for entry in row3:
                            # write the actual values
                            histFile.write(str(int(entry)) + delim)
            histFile.write("\n")
        histFile.close()


# In[5]:

print "Generating histograms from the hits in XYZT format for files based on " + filename

allClassValues = []
all4dTo2dHistograms = []
#all4dTo3dHistograms = []
all4dTo4dHistograms = []
all4dTo3dHistogramsXYZ = []
all4dTo3dHistogramsXYT = []
all4dTo3dHistogramsXZT = []
all4dTo3dHistogramsYZT = []
all4dTo3dHistogramsRZT = []

# Evaluate one event at a time
for eventID in [1,2]:
#for eventID in allEventNumbers:
        # Determine the class of this event
        allClassValues.append(getClassUpDown( tracks[int(eventID)] ))

        # filter all hits belonging to this event
        curHits = filterHitsForThisEvent(hitsXYZ, eventID)

        # do the 2d histograms 
        #computeAndStore4dTo2dHistograms(int(eventID), curHits, numberBinsX, numberBinsY, numberBinsZ, numberBinsT, filenameOutput, classValue, delim)
        compute4dTo2dHistograms(curHits, numberBinsX, numberBinsY, numberBinsZ, numberBinsT)
        
        # do the 3d histograms
        # computeAndStore4dTo3dHistograms(curHits, numberBinsX, numberBinsY, numberBinsZ, numberBinsT, filenameOutput, classValue, delim)
        compute4dTo3dHistograms(curHits, numberBinsX, numberBinsY, numberBinsZ, numberBinsT)

        # do the 4d and 3d time series histograms 
        # works but produces giant output files and is not required for now
        #computeAndStore4dTo4dHistograms(curHits, numberBinsX, numberBinsY, numberBinsZ, numberBinsT, filenameOutput, classValue, delim)
        compute4dTo4dHistograms(curHits, numberBinsX, numberBinsY, numberBinsZ, numberBinsT)

store2dHistogramsAsCSV(allClassValues, np.array(all4dTo2dHistograms)[:,0], "results/4dTo2d/xt/hist_"+filenameOutput+"_xt.csv")
store2dHistogramsAsCSV(allClassValues, np.array(all4dTo2dHistograms)[:,1], "results/4dTo2d/yt/hist_"+filenameOutput+"_yt.csv")
store2dHistogramsAsCSV(allClassValues, np.array(all4dTo2dHistograms)[:,2], "results/4dTo2d/zt/hist_"+filenameOutput+"_zt.csv")
store2dHistogramsAsCSV(allClassValues, np.array(all4dTo2dHistograms)[:,3], "results/4dTo2d/xy/hist_"+filenameOutput+"_xy.csv")
store2dHistogramsAsCSV(allClassValues, np.array(all4dTo2dHistograms)[:,4], "results/4dTo2d/xz/hist_"+filenameOutput+"_xz.csv")
store2dHistogramsAsCSV(allClassValues, np.array(all4dTo2dHistograms)[:,5], "results/4dTo2d/yz/hist_"+filenameOutput+"_yz.csv")

store3dHistogramsAsCSV(allClassValues, np.array(all4dTo3dHistogramsXYZ), "results/4dTo3d/xyz/hist_"+filenameOutput+"_xyz.csv")
store3dHistogramsAsCSV(allClassValues, np.array(all4dTo3dHistogramsXYT), "results/4dTo3d/xyt/hist_"+filenameOutput+"_xyt.csv")
store3dHistogramsAsCSV(allClassValues, np.array(all4dTo3dHistogramsXZT), "results/4dTo3d/xzt/hist_"+filenameOutput+"_xzt.csv")
store3dHistogramsAsCSV(allClassValues, np.array(all4dTo3dHistogramsYZT), "results/4dTo3d/yzt/hist_"+filenameOutput+"_yzt.csv")
store3dHistogramsAsCSV(allClassValues, np.array(all4dTo3dHistogramsRZT), "results/4dTo3d/rzt/hist_"+filenameOutput+"_rzt.csv")
#"""
store3dHistogramsAsCSV(allClassValues, np.array(all4dTo3dHistograms)[:,0], "results/4dTo3d/xyz/hist_"+filenameOutput+"_xyz.csv")
store3dHistogramsAsCSV(allClassValues, np.array(all4dTo3dHistograms)[:,1], "results/4dTo3d/xyt/hist_"+filenameOutput+"_xyt.csv")
store3dHistogramsAsCSV(allClassValues, np.array(all4dTo3dHistograms)[:,2], "results/4dTo3d/xzt/hist_"+filenameOutput+"_xzt.csv")
store3dHistogramsAsCSV(allClassValues, np.array(all4dTo3dHistograms)[:,3], "results/4dTo3d/yzt/hist_"+filenameOutput+"_yzt.csv")
store3dHistogramsAsCSV(allClassValues, np.array(all4dTo3dHistograms)[:,4], "results/4dTo3d/rzt/hist_"+filenameOutput+"_rzt.csv")
#"""

#store4dHistogramsAsCSV(allClassValues, np.array(all4dTo4dHistograms), "results/4dTo4d/xyzt/hist_"+filenameOutput+"_xyzt.csv")


# In[8]:

print "Generating histograms from the hits in OMID versus time format for files based on " + filename

allClassValues = []
all2dTo2dHistograms = []

# Evaluate one event at a time
#for eventID in [1,1]:
for eventID in allEventNumbers:
        # Determine the class of this event
        allClassValues.append(getClassUpDown( tracks[int(eventID)] ))

        # filter all hits belonging to this event
        curHits = filterHitsForThisEvent(hits, eventID)

        # Do the 2dTo2dHistogram
        #computeAndStore2dTo2dHistogram(curHits, numberBinsID, numberBinsT, filenameOutput, classValue, delim)
        compute2dTo2dHistogram(curHits, numberBinsID, numberBinsT)

store2dHistogramsAsCSV(allClassValues, np.array(all2dTo2dHistograms), "results/2dTo2d/omIDt/hist_"+filenameOutput+"_omidt.csv")


# In[ ]:



