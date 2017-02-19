for i in *.pgm; do convert -negate $i ${i}_inv.pgm ; done
for i in *.pgm_inv.pgm ; do mv $i ${i/.pgm_inv.pgm/_inv.pgm} ; done
for i in *.0*.pgm ; do mv $i ${i/.0/} ; done
for i in *.pgm; do convert $i ${i/.pgm/}.png ; done
