#!/bin/bash
#for i in {xt,yt,zt,xy,xz,yz} ; do echo $i && cat 4dTo2d/${i}/*.csv >> ${i}.ssv ; sed 's/,*$//' ${i}.ssv > ${i}.csv ; rm ${i}.ssv ; done
#for i in {xyz,xyt,xzt,yzt,rzt} ; do echo $i && cat 4dTo3d/${i}/*.csv >> ${i}.ssv ; sed 's/,*$//' ${i}.ssv > ${i}.csv ; rm ${i}.ssv ; done
#echo xyzt && rm -f xyzt.ssv && cat 4dTo4d/xyzt/*.csv >> xyzt.ssv ; sed 's/,*$//' xyzt.ssv > xyzt.csv ; rm xyzt.ssv
echo xyzt && rm -f xyzt.ssv && for i in {1..100}; do echo $i && ls 4dTo4d/xyzt/hist___hdf5files_km3_v4_*_${i}_JTE_r2356_root_h5_xyzt.csv && cat 4dTo4d/xyzt/hist___hdf5files_km3_v4_*_${i}_JTE_r2356_root_h5_xyzt.csv >> xyzt.ssv ; done ; sed 's/,*$//' xyzt.ssv > xyzt.csv ; rm xyzt.ssv
# echo omidt && cat 2dTo2d/omIDt/*.csv >> omidt.ssv ; sed 's/,*$//' omidt.ssv > omidt.csv ; rm omidt.ssv
