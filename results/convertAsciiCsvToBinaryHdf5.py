import numpy as np
import h5py
import csv

datatypey = np.float32
datatypex = np.uint8
numx = 11
numy = 11
numz = 18
numt = 50


def splitLineInXAndY(lineAsString):
	lineAsString = lineAsString.strip('\n') # remove newline at the end of the line
        lineSplit = lineAsString.split(',') # split the line into individual numbers
        if lineSplit[len(lineSplit)-1] == "":
            lineSplit = lineSplit[0:len(lineSplit)-1] # remove the last empty entry due to trailing "," in poor csv implementation 
        line = np.array(lineSplit, datatypey)   # store as numpy array
        numMC = int(line[0]+0.001)        # the first number in each line states how many MC related infos are present
	# TODO: encode the actual geometry here
        # x = line[numMC+1:].reshape(1, numx, numy, numz, numt).astype(datatypex)         # everything after the first numMC+1 entries are features
        x = line[numMC+1:].reshape(1, len(line)-numMC-1).astype(datatypex)         # everything after the first numMC+1 entries are features

        # the first numMC+1 entries (but 0 is numMC itself) are information from MC (often labels) and may not be used as input for training! 
        y = line[1:numMC+1]
	return (x, y)


def readDataFromFile(filename):
	xs = []
	ys = []

	f = open(filename)
	for lineAsString in f:
		x, y = splitLineInXAndY(lineAsString)
		xs.append(x)
		ys.append(y)
	f.close()
	xsnp = np.array(xs, datatypex)
	ysnp = np.array(ys, datatypey)
	return (xsnp, ysnp)

import sys

filename = ""
if len(sys.argv) > 1:
    filename = sys.argv[1]
if filename == "":
    print "Please specify a csv file to convert. Usage " + sys.argv[0] + " ./path/to/test.csv"
    exit(-1)

x, y = readDataFromFile(filename)

#Create HDF5 file
f = h5py.File(filename+".h5", 'w')
f.create_dataset('x', data=x)
f.create_dataset('y', data=y)
f.close()

