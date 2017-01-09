import pandas as pd
import numpy as np
import sys

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

hits = np.loadtxt(filenameHits)
f = open(filenameBase+"_hitsXYZ.txt", 'w')
for hit in hits:
	position = geo[int(hit[1])-1]
	# print hit[1], position
	# write event_id x y z time
	f.write(str(int(hit[0])) + s + str(position[1]) + s + str(position[2]) + s + str(position[3]) + s + str(hit[3]) + "\n")
f.close()

hitsTriggered = np.loadtxt(filenameHitsTriggered)
f = open(filenameBase+"_hitsTriggeredXYZ.txt", 'w')
for hit in hits:
	position = geo[int(hit[1])-1]
	# print hit[1], position
	# write event_id x y z time
	f.write(str(int(hit[0])) + s + str(position[1]) + s + str(position[2]) + s + str(position[3]) + s + str(hit[3]) + "\n")
f.close()

print "Done."
