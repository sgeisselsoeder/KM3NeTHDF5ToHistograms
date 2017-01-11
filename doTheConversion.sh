# dump hdf5 files to ASCII hits
# data.h5 used to be km3_v4_numuCC_100.JTE_r2356.root.h5
python h5ToHits.py data.h5

# extend the hits based on OM ID to XYZ coordinates
# python hitsToXYZHits.py data.h5

# create histograms from the hits resolved for IDs (line, OM, and pot. PMT) and time
python hitsIDsTo2DHist.py data.h5

# create histograms from the hits, resolved for XYZ and time
python hitsXYZTTo2DHists.py data.h5

