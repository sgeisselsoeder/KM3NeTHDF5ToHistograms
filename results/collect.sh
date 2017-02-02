#!/bin/bash
for i in {xt,yt,zt,xy,xz,yz} ; do echo $i && cat 4dTo2d/${i}/*.csv >> ${i}.ssv ; sed 's/ *$//' ${i}.ssv > ${i}.csv ; rm ${i}.ssv ; done
echo omIDt && cat 2dTo2d/omIDt/*.csv >> omIDt.ssv ; sed 's/ *$//' omIDt.ssv > omIDt.csv ; rm omIDt.ssv
