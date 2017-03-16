#!/bin/bash
for i in {xt,yt,zt,xy,xz,yz} ; do echo $i && cat 4dTo2d/${i}/*.csv >> ${i}.ssv ; sed 's/,*$//' ${i}.ssv > ${i}.csv ; rm ${i}.ssv ; done
for i in {xyz,xyt,xzt,yzt,rzt} ; do echo $i && cat 4dTo3d/${i}/*.csv >> ${i}.ssv ; sed 's/,*$//' ${i}.ssv > ${i}.csv ; rm ${i}.ssv ; done
echo xyzt && cat 4dTo4d/xyzt/*.csv >> xyzt.ssv ; sed 's/,*$//' xyzt.ssv > xyzt.csv ; rm xyzt.ssv
# echo omidt && cat 2dTo2d/omIDt/*.csv >> omidt.ssv ; sed 's/,*$//' omidt.ssv > omidt.csv ; rm omidt.ssv
