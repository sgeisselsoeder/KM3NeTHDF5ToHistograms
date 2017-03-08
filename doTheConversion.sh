HDFFOLDER=./hdf5files

time python h5ToHistograms.py ${HDFFOLDER}/km3_v4_numuNC_37.JTE_r2356.root.h5

#for f in ${HDFFOLDER}/*.h5; do 
#	python h5ToHistograms.py $f
#done
#cd results && ./collect.sh ; cd ..

