import numpy as np

#from histogramsToFiles import store2dHistogramAsPGM

tstart = 0.15
tend = tstart

def compute4dTo2dHistograms(curHits, numberBinsX, numberBinsY, numberBinsZ, numberBinsT, all4dTo2dHistograms):
        # slice out the times of the current hits
        times = np.array(curHits[:,4], np.float32)

        # analyze time
        tmin = min(times)
        tmax = max(times)
	tdiff = tmax - tmin
	tmean = tmin+0.5*tdiff
        #print "min time: " + str(tmin) + "  max time: " + str(tmax) + "  covered time " + str(tdiff)
         
        # slice out the coordinates of the current hits
        x = np.array(curHits[:,1], np.float32)
        y = np.array(curHits[:,2], np.float32)
        z = np.array(curHits[:,3], np.float32)

        # create histograms for this event
	histXvsT = np.histogram2d(times, x, [numberBinsT, numberBinsX], range=((tmean-tstart*tdiff, tmean+tend*tdiff),(min(x), max(x)) ))
        histYvsT = np.histogram2d(times, y, [numberBinsT, numberBinsY], range=((tmean-tstart*tdiff, tmean+tend*tdiff),(min(y), max(y)) ))
        histZvsT = np.histogram2d(times, z, [numberBinsT, numberBinsZ], range=((tmean-tstart*tdiff, tmean+tend*tdiff),(min(z), max(z)) ))
        histXvsY = np.histogram2d(y, x, [numberBinsY, numberBinsX])
        histXvsZ = np.histogram2d(z, x, [numberBinsZ, numberBinsX])
        histYvsZ = np.histogram2d(z, y, [numberBinsZ, numberBinsY])
       
	all4dTo2dHistograms.append([histXvsT[0], histYvsT[0], histZvsT[0], histXvsY[0], histXvsZ[0], histYvsZ[0]])
        
        # store the histograms to images   # commented out by default to not double the output
        """
        #store2dHistogramAsPGM(histXvsT, "results/4dTo2d/xt/hist_"+filenameOutput+"_event"+str(eventID)+"_TvsX.pgm")
        #store2dHistogramAsPGM(histYvsT, "results/4dTo2d/yt/hist_"+filenameOutput+"_event"+str(eventID)+"_TvsY.pgm")
        store2dHistogramAsPGM(histZvsT, "results/4dTo2d/zt/hist_TvsZ.pgm")
        store2dHistogramAsPGM(histZvsT2, "results/4dTo2d/zt/hist_TvsZ2.pgm")
        #store2dHistogramAsPGM(histXvsY, "results/4dTo2d/xy/hist_"+filenameOutput+"_event"+str(eventID)+"_XvsY.pgm")
        #store2dHistogramAsPGM(histXvsZ, "results/4dTo2d/xz/hist_"+filenameOutput+"_event"+str(eventID)+"_XvsZ.pgm")
        #store2dHistogramAsPGM(histYvsZ, "results/4dTo2d/yz/hist_"+filenameOutput+"_event"+str(eventID)+"_YvsZ.pgm")
        #"""

def compute4dTo3dHistograms(curHits, numberBinsX, numberBinsY, numberBinsZ, numberBinsT, all4dTo3dHistogramsXYZ, all4dTo3dHistogramsXYT, all4dTo3dHistogramsXZT, all4dTo3dHistogramsYZT, all4dTo3dHistogramsRZT):
	x = curHits[:,1:2]
	y = curHits[:,2:3]
	z = curHits[:,3:4]
	t = curHits[:,4:5]
	tmin = min(t)
        tmax = max(t)
	tdiff = tmax - tmin
	tmean = tmin+0.5*tdiff

	
        histXYZ = np.histogramdd( np.array(curHits[:,1:4], np.float32), [numberBinsX, numberBinsY, numberBinsZ])
        histXYT = np.histogramdd( np.array(np.concatenate([curHits[:,1:3],t], axis=1), np.float32), [numberBinsX, numberBinsY, numberBinsT], \
	range=( (min(x),max(x)),(min(y),max(y)),(tmean-tstart*tdiff, tmean+tend*tdiff)) )
        histXZT = np.histogramdd( np.array(np.concatenate([x,curHits[:,3:5]], axis=1), np.float32), [numberBinsX, numberBinsZ, numberBinsT], \
	range=( (min(x),max(x)),(min(z),max(z)),(tmean-tstart*tdiff, tmean+tend*tdiff)) )
        histYZT = np.histogramdd( np.array(curHits[:,2:5], np.float32), [numberBinsY, numberBinsZ, numberBinsT], \
	range=( (min(y),max(y)),(min(z),max(z)),(tmean-tstart*tdiff, tmean+tend*tdiff)) )

        # add a rotation-symmetric 3d hist
        x = np.array(curHits[:,1:2], np.float32)
        y = np.array(curHits[:,2:3], np.float32)
        r = np.sqrt(x*x + y*y)
        zt = np.array(curHits[:,3:5], np.float32)
        rzt = np.array(np.concatenate([r, zt], axis=1), np.float32)
        histRZT = np.histogramdd(rzt, [numberBinsX, numberBinsZ, numberBinsT], \
	range=( (min(r),max(r)),(min(z),max(z)),(tmean-tstart*tdiff, tmean+tend*tdiff)) )

        #all4dTo3dHistograms.append( [histXYZ[0], histXYT[0], histXZT[0], histYZT[0], histRZT[0]] )
        all4dTo3dHistogramsXYZ.append( histXYZ[0] )
        all4dTo3dHistogramsXYT.append( histXYT[0] )
        all4dTo3dHistogramsXZT.append( histXZT[0] )
        all4dTo3dHistogramsYZT.append( histYZT[0] )
        all4dTo3dHistogramsRZT.append( histRZT[0] )

def compute4dTo4dHistograms(curHits, numberBinsX, numberBinsY, numberBinsZ, numberBinsT, all4dTo4dHistograms):
	x = curHits[:,1:2]
	y = curHits[:,2:3]
	z = curHits[:,3:4]
	t = curHits[:,4:5]
	tmin = min(t)
        tmax = max(t)
	tdiff = tmax - tmin
	tmean = tmin+0.5*tdiff

        curHitsWithoutEventID = np.array(curHits[:,1:5], np.float32)
        histXYZT = np.histogramdd(curHitsWithoutEventID, [numberBinsX, numberBinsY, numberBinsZ, numberBinsT], \
	range=( (min(x),max(x)),(min(y),max(y)),(min(z),max(z)),(tmean-tstart*tdiff, tmean+tend*tdiff)) )
        all4dTo4dHistograms.append(histXYZT[0])

def compute2dTo2dHistogram(curHits, numberBinsID, numberBinsT, all2dTo2dHistograms):
        # slice out the OM ids of the current hits
        ids = np.array(curHits[:,1], np.int32)

        # slice out the times of the current hits
        times = np.array(curHits[:,3], np.int32)
	tmin = min(times)
        tmax = max(times)
	tdiff = tmax - tmin
	tmean = tmin+0.5*tdiff

        # create a histogram for this event
        histIDvsT = np.histogram2d(times, ids, [numberBinsT, numberBinsID], \
	range=( (min(ids),max(ids)),(tmean-tstart*tdiff, tmean+tend*tdiff)) )
        
        all2dTo2dHistograms.append(histIDvsT[0])
        # store2dHistogramAsPGM(histIDvsT, "results/2dTo2d/omIDt/hist_"+filenameOutput+"_event"+str(eventID)+"_TvsOMID.pgm")

