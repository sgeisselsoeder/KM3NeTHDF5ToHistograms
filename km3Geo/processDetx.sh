#!/bin/bash

tempGeo="km3netGeoOnePosPerOM.txt"
cat km3net_jul13_90m.detx | grep ".*-0.000 -0.000 -1.000 0.000.*" | cut -d " " -f 3-5 > $tempGeo
len=`wc -l $tempGeo | cut -d " " -f -1`

temp="tempNumberFileForConversion.txt"
rm -f $temp
for (( i=1; i<=$len; i++ )) ; do echo $i >> $temp ; done

paste -d " " $temp $tempGeo > km3GeoOm.txt

rm -f $temp
rm -f $tempGeo
