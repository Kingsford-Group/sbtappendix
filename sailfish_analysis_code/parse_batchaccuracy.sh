#!/bin/bash

#takes in a directory and finds every "_timing_t.${num}.txt" file
#Parses with tail -n 3 the relevant timing information and puts them all into the same temporary file
#Calls parse_time.py on the temporary file and 

cutlist="$1"
querylist="$2"
resultBase="$3"
keyFile="$4"
baseFile="$5"
tempFile="$6"
#"$HOME/algae/bloomtree/src/sail_suite/sum_timing.txt"
#outputFile="$2"
rm $tempFile
for num in ".5" ".6" ".7" ".8" ".9" "1"
do
	python autoBatchAccuracy.py $cutlist $querylist  "${resultBase}${num}.txt" $keyFile $baseFile >> $tempFile
done
python buildArrays.py $tempFile
