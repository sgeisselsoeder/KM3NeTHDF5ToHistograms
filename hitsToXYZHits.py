import pandas as pd
import numpy as np
import sys
from random import randint

# write the hits in xyz (optional: for a random subset of surviving OMs)
def writeHits(hits, geo, filename, faultProb = 0.0): 
	numOMs = len(geo)
	# print numOMs

	offlineOMs = []
	for i in range(0,int(numOMs*faultProb)):
		offlineOMs.append(randint(0,numOMs))
	print faultProb
	print offlineOMs

	f = open(filename, 'w')
	# write the hits with xyz geometry, ignore "faulty" ones
	for hit in hits:
		if not hit[1] in offlineOMs:
			position = geo[int(hit[1])-1]
			# print hit[1], position
			# write event_id x y z time
			f.write(str(int(hit[0])) + s + str(position[1]) + s + str(position[2]) + s + str(position[3]) + s + str(hit[3]) + "\n")
		#else:
		#	print hit[1]
	f.close()


if len(sys.argv) < 2 or str(sys.argv[1]) == "-h":
	print "Usage: python " + str(sys.argv[0]) + " file.h5"
	# print "Usage: python " + str(sys.argv[0]) + " file.h5_tracks.txt"
	sys.exit(1)

filenameBase = str(sys.argv[1])
print "Converting hit files based on IDs to XYZ-based. Processing files for " + filenameBase
filenameHits = filenameBase + "_hits.txt"
filenameHitsTriggered = filenameBase + "_hitsTriggered.txt"

# the separator used in output files between entries (e.g. whitespace, comma, tab, ...)
s = " " # s = "\t" s = ", "
geo = np.loadtxt("km3GeoOm.txt")

# load the hits
hits = np.loadtxt(filenameHits)

# optional: write the hits in xyz for a random subset of surviving OMs
writeHits(hits, geo, filenameBase+"_hitsXYZ.txt", 0.0) 
faultProbability = 0.1
writeHits(hits, geo, filenameBase+"_hitsXYZFaulty"+str(faultProbability)+".txt", faultProbability) 
faultProbability = 0.2
writeHits(hits, geo, filenameBase+"_hitsXYZFaulty"+str(faultProbability)+".txt", faultProbability) 

# write the triggered hits with xyz geometry
hitsTriggered = np.loadtxt(filenameHitsTriggered)
writeHits(hitsTriggered, geo, filenameBase+"_hitsTriggeredXYZ.txt", 0.0) 


print "Done."
