HDFFOLDER=./hdf5files

# time python h5ToHistograms.py ${HDFFOLDER}/km3_v4_numuNC_37.JTE_r2356.root.h5

for i in {1..1};
do
	time python h5ToHistograms.py ${HDFFOLDER}/km3_v4_anumuNC_${i}.JTE_r2356.root.h5
	time python h5ToHistograms.py ${HDFFOLDER}/km3_v4_anumuCC_${i}.JTE_r2356.root.h5
	time python h5ToHistograms.py ${HDFFOLDER}/km3_v4_numuNC_${i}.JTE_r2356.root.h5
	time python h5ToHistograms.py ${HDFFOLDER}/km3_v4_numuCC_${i}.JTE_r2356.root.h5
	time python h5ToHistograms.py ${HDFFOLDER}/km3_v4_anueNC_${i}.JTE_r2356.root.h5
	time python h5ToHistograms.py ${HDFFOLDER}/km3_v4_anueCC_${i}.JTE_r2356.root.h5
	time python h5ToHistograms.py ${HDFFOLDER}/km3_v4_nueNC_${i}.JTE_r2356.root.h5
	time python h5ToHistograms.py ${HDFFOLDER}/km3_v4_nueCC_${i}.JTE_r2356.root.h5
done


