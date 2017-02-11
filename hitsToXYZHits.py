import numpy as np
import sys

# write the hits in xyz (optional: for a random subset of surviving OMs)
def writeHits(hits, geo, filename): 
       f = open(filename, 'w')
       # write the hits with xyz geometry
       for hit in hits:
               position = geo[int(hit[1])-1]
               # write event_id x y z time # add the original omID to allow artificially failing oms dynamically in histogram step
               f.write(str(int(hit[0])) + s + str(position[1]) + s + str(position[2]) + s + str(position[3]) + s + str(hit[3]) + s + str(int(hit[1])) + "\n")
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
print hits.shape

# write the hits in xyz for a random subset of surviving OMs
print "Writing hits to file " + filenameBase+"_hitsXYZ.txt"
writeHits(hits, geo, filenameBase+"_hitsXYZ.txt") 

# write the triggered hits with xyz geometry
print "Writing only triggered hits"
hitsTriggered = np.loadtxt(filenameHitsTriggered)
writeHits(hitsTriggered, geo, filenameBase+"_hitsTriggeredXYZ.txt") 

print "Done."
