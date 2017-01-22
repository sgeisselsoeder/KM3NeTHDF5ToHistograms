# data.h5 used to be km3_v4_numuCC_100.JTE_r2356.root.h5

# dump hdf5 files to ASCII hits
time python h5ToHits.py data.h5

# extend the hits based on OM ID to XYZ coordinates
time python hitsToXYZHits.py data.h5

# create the different types of histograms from the hits (OM-IDs and XYZ)
time python hitsToHistograms.py data.h5

cd results && time collect.sh ; cd ..
