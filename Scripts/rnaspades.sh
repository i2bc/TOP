#!/bin/bash

if [[ $(wc -l <$1) -ge 21 ]]
then
	rnaspades.py -s $1 -o $2/$3/$4/rnaspades
else 
	touch $2/$3/$4/rnaspades/transcripts.fasta && touch $2/$3/$4/rnaspades/params.txt
fi