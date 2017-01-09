# dump hdf5 files to ASCII hits
python h5ToHits.py km3_v4_numuCC_100.JTE_r2356.root.h5

# create histograms from the hits, resolved for IDs (line, OM, and pot. PMT) and time
python hitsIDsToHists.py km3_v4_numuCC_100.JTE_r2356.root.h5

# create histograms from the hits, resolved for XYZ and time
# python hitsToXYZHits.py km3_v4_numuCC_100.JTE_r2356.root.h5
# python hitsXYZTToHists.py km3_v4_numuCC_100.JTE_r2356.root.h5

