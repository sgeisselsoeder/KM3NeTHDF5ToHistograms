#!/bin/bash
time ./collect.sh
time ./collechtNumu.sh
# split xyzt in bunches
time split -l 200000 --numeric-suffixes=1 --suffix-length=1 xyzt.csv xyztSplit
for f in xyztSplit* ; do time shuf $f > ${f}Shuf.csv ; done
time ./zipAll.sh
time ./clearResults.sh

