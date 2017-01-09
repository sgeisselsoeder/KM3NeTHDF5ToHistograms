import pandas as pd
import numpy as np
import sys

if len(sys.argv) < 2 or str(sys.argv[1]) == "-h":
	print "Usage: python " + str(sys.argv[0]) + " file.h5"
	# print "Usage: python " + str(sys.argv[0]) + " file.h5.txt"
	# print "Usage: python " + str(sys.argv[0]) + " file.h5_tracks.txt"
	sys.exit(1)

filenameBase = str(sys.argv[1])
print filenameBase
filenameTracks = filenameBase + "_tracks.txt"
filenameHits = filenameBase + "_hitsXYZ.txt"
filenameHitsTriggered = filenameBase + "_hitsXYZTriggered.txt"

# the separator used in output files between entries (e.g. whitespace, comma, tab, ...)
s = " "	# s = "\t" s = ", "

geoFile = open("km3GeoOm.txt", 'r')
geo = geoFile.read()
print geo

trackFile = open(filenameTracks, 'r')
tracksPlain = trackFile.read()
tracks = np.array(tracksPlain)

hitFile = open(filenameHits, 'r')
hitsPlain = hitFile.read()
hits = np.array(hitsPlain)




"""
f = open(filename+"_tracks.txt", 'w')
for track in tracks:
	# only for primary particles, bjorkeny != 0:
	if track[0] != 0.0:
		# write dir_x dir_y dir_z energy (for the moment)
		f.write(str(track[1]) + s + str(track[2]) + s + str(track[3]) + s + str(track[4]) + "\n")
f.close()
"""


hitTriggeredFile = open(filenameHits, 'r')
hitsTriggeredPlain = hitTriggeredFile.read()
hitsTriggered = np.array(hitsTriggeredPlain)








trackFile.close()
hitFile.close()
hitTriggeredFile.close()

