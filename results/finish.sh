#!/bin/bash
time ./collect.sh
time ./collectNumu.sh
# split xyzt in bunches
time split -l 100000 --numeric-suffixes=1 --suffix-length=1 xyzt.csv xyztSplit
for f in xyztSplit* ; do time shuf $f > ${f}Shuf ; done
for f in xyztSplit*Shuf ; do time python convertAsciiCsvToBinaryHdf5.py $f ; done
for f in xyztSplit*Shuf ; do mv $i ${f}.csv ; done
time ./zipAll.sh
#time ./clearResults.sh

