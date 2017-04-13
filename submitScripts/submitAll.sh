#!/bin/bash
mv convert*to*.[eo]* logs/
for i in {1..4}
do
echo $i
qsub submit${i}
done
qstat -Q
qstat
