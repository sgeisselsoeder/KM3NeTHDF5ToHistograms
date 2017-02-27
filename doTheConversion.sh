#HDFFOLDER=~/woodyhome/hdf5files
HDFFOLDER=./hdf5files

for f in ${HDFFOLDER}/*.h5; do 
	time python h5ToHistograms.py $f
done
cd results && ./collect.sh ; cd ..

