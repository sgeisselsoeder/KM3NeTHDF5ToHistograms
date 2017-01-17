#!/bin/bash
for i in {xt,yt,zt,xy,xz,yz} ; do echo $i && cat $i/*.hist >> ../${i}.csv ; done
