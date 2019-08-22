#!/bin/bash

if [ -e $3 ]
then
        python3 $1 $2 $3 $7
else
        touch $4/$5/$6/CRISPR_contigs.fasta
fi