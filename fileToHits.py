import pandas as pd
import numpy as np
import sys

def filterPrimaryTracks(tracksFull):
        # only keep tracks from primary particles, implemented as only those with bjorken-y != 0.0
        return tracksFull[ np.where( tracksFull[:,0] != 0.0)[0] ]

def extractRelevantTrackInfo(tracks):
        # keep the relevant info from the track: event_id particle_type dir_x dir_y dir_z energy isCC bjorkeny
        return np.array( np.concatenate( [ tracks[:,14:15],tracks[:,13:14],tracks[:,1:5],tracks[:,7:8],tracks[:,0:1] ], axis=1), np.float32 )

def filterTriggeredHits(hits):
        # only keep triggered hits
        return hits[ np.where( hits[:,13] == True)[0] ]

def extractRelevantHitInfo(hits):
        # keep the relevant info from each hit: event_id dom_id channel_id time 
        return np.array( np.concatenate( [hits[:,14:15],hits[:,4:5],hits[:,0:1],hits[:,11:12]], axis=1), np.float32 )

def convertHitsXYZ(hits, geo):
        # write the hits with xyz geometry
        temp = []
        for hit in hits:
                position = geo[int(hit[1])-1]
                temp.append( [int(hit[0]), position[1], position[2], position[3], hit[3], int(hit[1])] )
        return np.array(temp)
       
def parseFile(filename, filenameGeometry):
	print "Extracting hits and tracks from hdf5 file " + filename
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

	print "Reading hits"
	hits = extractRelevantHitInfo( np.array( pd.read_hdf(filename, 'hits') ) )
	# np.savetxt(filename+"_hits.csv.gz", hits, delimiter=delim)
	allEventNumbers = set(hits[:,0])

	print "Converting hits omid -> XYZ"
	hitsXYZ = convertHitsXYZ(hits, geo)
	# np.savetxt(filename+"_hitsXYZ.csv.gz", hitsXYZ, delimiter=delim)
	
	print "Done converting."
	return tracks, hits, hitsXYZ


