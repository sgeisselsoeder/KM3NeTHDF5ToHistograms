#!/bin/bash
for i in {xt,yt,zt,xy,xz,yz} ; do echo $i && cat 4dTo2d/${i}/*numuCC_*.csv >> numu${i}.ssv ; sed 's/,*$//' numu${i}.ssv > numu${i}.csv ; rm numu${i}.ssv ; done
# echo omidt && cat 2dTo2d/omIDt/*numuCC_*.csv >> numuomidt.ssv ; sed 's/,*$//' numuomidt.ssv > numuomidt.csv ; rm numuomidt.ssv
