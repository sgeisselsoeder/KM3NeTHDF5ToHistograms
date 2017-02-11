HDFFOLDER=~/woodyhome/hdf5files

# for f in ../data/km3netHDF5Files/*.h5; do 
#for f in /home/hpc/capn/mpp460/woodyhome/hdf5files/km3_v4_anueCC_12.JTE_r2356.root.h5 ; do 
for f in ${HDFFOLDER}/*.h5; do 
	time python h5ToHits.py $f
done
#for f in ${HDFFOLDER}/*.h5; do 
#	time python hitsToHistograms.py $f
#done
#cd results && time ./collect.sh ; cd ..

