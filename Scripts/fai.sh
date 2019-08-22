#!/bin/bash

if [ -s $1 ]
then
        samtools faidx $1 
else
        touch $2/$3/$4/CRISPR_contigs.fasta.fai
fi