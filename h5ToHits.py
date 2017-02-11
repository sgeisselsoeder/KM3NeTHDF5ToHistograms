import pandas as pd
import numpy as np
import sys

def writeTracksCSV(tracks, filename, s):
	f = open(filename+"_tracks.txt", 'w')
	for track in tracks:
		bjorkeny = track[0]
		# only output for primary particles (they have bjorkeny != 0.0):
		if bjorkeny != 0.0: 		
			# write event_id particle_type dir_x dir_y dir_z energy isCC
			f.write(str(track[14]) + s + str(track[13]) + s + str(track[1]) + s + str(track[2]) + s + str(track[3]) + s + str(track[4]) + s + str(int(track[7])) + "\n")
	f.close()

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

def writeHitsXYZCSV(hits, geo, filename, s):
	f = open(filename+"_hitsXYZ.txt" , 'w')
        # write the hits with xyz geometry
        for hit in hits:
		print hit
		print geo
		print hit[1]
		print geo[int(hit[1])-1]
                position = geo[int(hit[1])-1]
                # write event_id x y z time # add the original omID to allow artificially failing oms dynamically in histogram step
                f.write(str(int(hit[0])) + s + str(position[1]) + s + str(position[2]) + s + str(position[3]) + s + str(hit[3]) + s + str(int(hit[1])) + "\n")
        f.close()

if len(sys.argv) < 2 or str(sys.argv[1]) == "-h":
	print "Usage: python " + str(sys.argv[0]) + " file.h5"
	sys.exit(1)

filename = str(sys.argv[1])
print "Extracting hits and tracks from hdf5 file " + filename

# the separator used in output files between entries (e.g. whitespace, comma, tab, ...)
s = " "

tracksPlain = pd.read_hdf(filename, 'mc_tracks')
tracks = np.array(tracksPlain)
writeTracksCSV(tracks, filename, s)

#f = open(filename+"_tracks.txt", 'w')
#for track in tracks:
#	bjorkeny = track[0]
#	# only output for primary particles (they have bjorkeny != 0.0):
#	if bjorkeny != 0.0: 		
#		# write event_id particle_type dir_x dir_y dir_z energy isCC
#		f.write(str(track[14]) + s + str(track[13]) + s + str(track[1]) + s + str(track[2]) + s + str(track[3]) + s + str(track[4]) + s + str(int(track[7])) + "\n")
#f.close()

hitsPlain = pd.read_hdf(filename, 'hits')
hits = np.array(hitsPlain)
print hits.shape
print hits
writeHitsCSV(hits, filename, s)

#f = open(filename+"_hits.txt", 'w')
#fTrig = open(filename+"_hitsTriggered.txt", 'w')
#for hit in hits:
#	# write: event_id dom_id channel_id time
#	infoString = str(hit[7]) + s + str(hit[1]) + s + str(hit[0]) + s + str(hit[4]) + "\n"
#	f.write(infoString)
#	# triggered hits only:
#	if (hit[6] == True):
#		fTrig.write(infoString)
#f.close()
#fTrig.close()

# geo = np.loadtxt("km3GeoOm.txt")
# writeHitsXYZCSV(hits, geo, filename, s)

print "Done."
