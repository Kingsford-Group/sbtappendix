#!/bin/bash

#takes in a directory and finds every "_timing_t.${num}.txt" file
#Parses with tail -n 3 the relevant timing information and puts them all into the same temporary file
#Calls parse_time.py on the temporary file and 

inputDir="$1"
tempFile="$2"
#"$HOME/algae/bloomtree/src/sail_suite/sum_timing.txt"
#outputFile="$2"

#".5" ".6" ".7" ".8" ".9" "1"
	for file in $(find $inputDir -maxdepth 1 -type f -name "*_timing.txt"); do
        echo $file >> "${tempFile}"
		tail -n 3 $file >> "${tempFile}"
		#bname="$(basename $query)"
		#echo "$inputTree $query ${outDir}${bname}"
		#./loop_bt $inputTree $query "${outDir}${bname}"
	done
