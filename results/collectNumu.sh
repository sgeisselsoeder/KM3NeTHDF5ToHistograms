#!/bin/bash
for i in {xt,yt,zt,xy,xz,yz} ; do echo $i && cat 4dTo2d/${i}/*numuCC_*.csv >> numu${i}.ssv ; sed 's/,*$//' numu${i}.ssv > numu${i}.csv ; rm numu${i}.ssv ; done
for i in {xyz,xyt,xzt,yzt,rzt} ; do echo $i && cat 4dTo3d/${i}/*numuCC_*.csv >> numu${i}.ssv ; sed 's/,*$//' numu${i}.ssv > numu${i}.csv ; rm numu${i}.ssv ; done
echo xyzt && cat 4dTo4d/xyzt/*numuCC_*.csv >> numuxyzt.ssv ; sed 's/,*$//' numuxyzt.ssv > numuxyzt.csv ; rm numuxyzt.ssv
