#!/bin/bash

if [ -s $1 ]
then
        bwa mem $1 $2| samtools view -q 60|samclip --ref $3 > $7
else
        touch $4/$5/$6/aln.sam
fi