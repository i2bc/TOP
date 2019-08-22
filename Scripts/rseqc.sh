#!/bin/bash

if [[ $(wc -l <$1) -ge 100000 ]]
then
        infer_experiment.py -r $3 -i $2 -s 500000 > $4
else
        touch $5/$6/$7/rseqc_results.txt
fi