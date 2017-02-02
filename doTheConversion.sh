# for f in ../data/km3netHDF5Files/km3_v4_anueCC_100.JTE_r2356.root.h5; do 
#for f in ../data/km3netHDF5Files/*.h5; do 
#	time python h5ToHits.py $f
#	# time python hitsToXYZHits.py $f
#	# time python hitsToHistograms.py $f
#done

#for f in ../data/km3netHDF5Files/*.h5; do 
#	time python hitsToXYZHits.py $f
#done

for f in ../data/km3netHDF5Files/*.h5; do 
	time python hitsToHistograms.py $f
done
cd results && time ./collect.sh ; cd ..

