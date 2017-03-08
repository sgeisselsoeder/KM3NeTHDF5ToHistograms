import pandas as pd
import numpy as np
import sys

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
"""
def store2dHistogramAsCSV(hist, classValue, filename, delim = ","):
        #test = np.reshape( hist[0], (len(hist[0])*len(hist[0][0]),1) )
        #test2 = np.append(np.array([classValue,]), test)
        #np.savetxt(filename, test2[np.newaxis], delimiter=delim)
        np.savetxt(filename, np.append(np.array([classValue,]), np.reshape( hist[0], (len(hist[0])*len(hist[0][0]),1) ) )[np.newaxis], delimiter=delim, fmt='%d')

def store3dHistogramAsCSV(hist, classValue, filename, delim = ","):
        np.savetxt(filename, np.append(np.array([classValue,]), np.reshape( hist[0], (len(hist[0])*len(hist[0][0])*len(hist[0][0][0]),1) ) )[np.newaxis], delimiter=delim, fmt='%d')

def store4dHistogramAsCSV(hist, classValue, filename, delim = ","):
        np.savetxt(filename, np.append(np.array([classValue,]), np.reshape( hist[0], (len(hist[0])*len(hist[0][0])*len(hist[0][0][0])*len(hist[0][0][0][0]),1) ) )[np.newaxis], delimiter=delim, fmt='%d')

def store3dHistogramSpliceAsCSV(hist, classValue, filename, delim = ","):
        np.savetxt(filename, np.append(np.array([classValue,]), np.reshape( hist, (len(hist)*len(hist[0])*len(hist[0][0]),1) ) )[np.newaxis], delimiter=delim, fmt='%d')
"""

"""
def store4dHistogramAsTimeSeriesOf3dHists(hist, classValue, filenameBase, delim = ","):
        # len(hist[0][0][0][0]) = time bins     len(hist[0][0][0]) = z bins     len(hist[0][0]) = y bins        len(hist[0]) = x bins
        numberOfTimeBins = len(hist[0][0][0][0])
        for time in range(0,numberOfTimeBins):
                filenameCurrent=filenameBase+"_"+str(time)+".csv"
                store3dHistogramSpliceAsCSV(hist[0][:,:,:,time], classValue, filenameCurrent, delim)
"""

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

