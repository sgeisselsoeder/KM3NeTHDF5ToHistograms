#!/bin/bash
./collect.sh
./collechtNumu.sh
# split xyzt in bunches of approx 120k
split -l 123020 --numeric-suffixes=1 --suffix-length=1 xyzt.csv xyztSplit
for f in xyztSplit* ; do shuf $f > ${f}Shuf.csv ; done
./zipAll.sh
./clearResults.sh

