#!/bin/bash
#for i in {xt,yt,zt,xy,xz,yz} ; do echo $i && cat 4dTo2d/${i}/*numuCC_*.csv >> numu${i}.ssv ; sed 's/,*$//' numu${i}.ssv > numu${i}.csv ; rm numu${i}.ssv ; done
#for i in {xyz,xyt,xzt,yzt,rzt} ; do echo $i && cat 4dTo3d/${i}/*numuCC_*.csv >> numu${i}.ssv ; sed 's/,*$//' numu${i}.ssv > numu${i}.csv ; rm numu${i}.ssv ; done
echo xyzt && rm -f numuxyzt.ssv && for i in {1..100}; do echo $i && ls 4dTo4d/xyzt/hist___hdf5files_km3_v4_*numuCC_${i}_JTE_r2356_root_h5_xyzt.csv && cat 4dTo4d/xyzt/hist___hdf5files_km3_v4_*numuCC_${i}_JTE_r2356_root_h5_xyzt.csv >> numuxyzt.ssv ; done ; sed 's/,*$//' numuxyzt.ssv > numuxyzt.csv ; rm numuxyzt.ssv


