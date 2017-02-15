#HDFFOLDER=../data/km3netHDF5Files
#HDFFOLDER=~/woodyhome/hdf5files
HDFFOLDER=./hdf5files

time python h5ToHistograms.py ${HDFFOLDER}/km3_v4_anueCC_12.JTE_r2356.root.h5

#for f in ${HDFFOLDER}/*.h5; do 
#	time python h5ToHits.py $f
#done
#for f in ${HDFFOLDER}/*.h5; do 
#	time python hitsToHistograms.py $f
#done
#cd results && time ./collect.sh ; cd ..

