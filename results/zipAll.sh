#!/bin/bash
for i in *.csv ; do echo $i && rm -f $i.tar.gz && tar cfz $i.tar.gz $i ; done
for i in {xt,yt,zt,xy,xz,yz} ; do echo $i && rm -f 4dTo2d/$i.tar.gz && tar cfz 4dTo2d/$i.tar.gz 4dTo2d/${i} ; done
for i in {xyz,xyt,xzt,yzt,rzt} ; do echo $i && rm -f 4dTo3d/$i.tar.gz && tar cfz 4dTo3d/$i.tar.gz 4dTo3d/${i} ; done
echo xyzt && rm -f 4dTo4d/xyzt.tar.gz && tar cfz 4dTo4d/xyzt.tar.gz 4dTo4d/xyzt
# echo omidt && rm -f 2dTo2d/omidt.tar.gz && tar cfz 2dTo2d/omIDt.tar.gz 2dTo2d/omIDt
