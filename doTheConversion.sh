# dump hdf5 files to ASCII hits
# data.h5 used to be km3_v4_numuCC_100.JTE_r2356.root.h5
python h5ToHits.py data.h5

# create histograms from the hits, resolved for IDs (line, OM, and pot. PMT) and time
python hitsIDsToHists.py data.h5

# create histograms from the hits, resolved for XYZ and time
# python hitsToXYZHits.py data.h5
# python hitsXYZTToHists.py km3_v4_numuCC_100.JTE_r2356.root.h5

