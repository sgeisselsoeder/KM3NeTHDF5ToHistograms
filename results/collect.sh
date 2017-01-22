#!/bin/bash
for i in {xt,yt,zt,xy,xz,yz} ; do echo $i && cat 4dTo2d/${i}/*.csv >> ${i}wWS.csv ; sed 's/ *$//' ${i}wWS.csv > ${i}.csv ; rm ${i}wWS.csv ; done
# head -n 793 zt.csv > ztTrain.csv
# tail -n 793 zt.csv > ztTest.csv
