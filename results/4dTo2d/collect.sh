#!/bin/bash
for i in {xt,yt,zt,xy,xz,yz} ; do echo $i && cat $i/*.hist >> ../${i}.csv ; done
echo "I did my job, but remember to remove the last whitespace from every line in every file. Automate that! Then delete this message!"
