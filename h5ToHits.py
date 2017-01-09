import pandas as pd
import numpy as np
import sys

if len(sys.argv) < 2 or str(sys.argv[1]) == "-h":
	print "Usage: python " + str(sys.argv[0]) + " file.h5"
	sys.exit(1)

filename = str(sys.argv[1])
print "Extracting hits and tracks from hdf5 file " + filename

# the separator used in output files between entries (e.g. whitespace, comma, tab, ...)
s = " "	# s = "\t" s = ", "

tracksPlain = pd.read_hdf(filename, 'mc_tracks')
tracks = np.array(tracksPlain)

f = open(filename+"_tracks.txt", 'w')
for track in tracks:
	# only for primary particles, bjorkeny != 0:
	if track[0] != 0.0: # TODO: maybe this just compares to the first character (track might be a string, track[0] a character) and is useless this way!
		# write dir_x dir_y dir_z energy (for the moment)
		f.write(str(track[1]) + s + str(track[2]) + s + str(track[3]) + s + str(track[4]) + "\n")
f.close()

hitsPlain = pd.read_hdf(filename, 'hits')
hits = np.array(hitsPlain)
f = open(filename+"_hits.txt", 'w')
fTrig = open(filename+"_hitsTriggered.txt", 'w')
for hit in hits:
	# f.write(str(hit[7]) + " " + str(hit[0]) + " " + str(hit[1]) + " " + str(hit[4]) + " " + str(hit[6]) + "\n")
	# f.write(str(hit[7]) + s + str(hit[0]) + s + str(hit[1]) + s + str(hit[4]) + "\n")

	# write: event_id dom_id channel_id time
	infoString = str(hit[7]) + s + str(hit[1]) + s + str(hit[0]) + s + str(hit[4]) + "\n"
	f.write(infoString)
	# extract all triggered hits only:
	if (hit[6] == True):
		fTrig.write(infoString)
f.close()
fTrig.close()

print "Done."
