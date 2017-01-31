for f in ../data/km3netHDF5Files/*.h5; do 
# for f in ../data/km3netHDF5Files/km3_v4_anueCC_100.JTE_r2356.root.h5; do 
	echo $f
	time python h5ToHits.py $f
	time python hitsToXYZHits.py $f
	time python hitsToHistograms.py $f
done
cd results && time ./collect.sh ; cd ..

## data.h5 used to be km3_v4_numuCC_100.JTE_r2356.root.h5
## dump hdf5 files to ASCII hits
#time python h5ToHits.py data.h5
## extend the hits based on OM ID to XYZ coordinates
#time python hitsToXYZHits.py data.h5
## create the different types of histograms from the hits (OM-IDs and XYZ)
#time python hitsToHistograms.py data.h5
#cd results && time collect.sh ; cd ..

