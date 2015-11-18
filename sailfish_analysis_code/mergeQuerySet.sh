#!/bin/bash


inputDir="$1"
outputFile="$2"
keyFile="$3"

for file in $(find $inputDir -type f -name "*.txt"); do
	cat $file >> $outputFile
	echo "" >> $outputFile
	echo $file >> $keyFile
	cat $file >> $keyFile
	echo "" >> $keyFile
	#tail -n 3 $file >> "${tempFile}_t${num}.txt"
	#bname="$(basename $query)"
	#echo "$inputTree $query ${outDir}${bname}"
	#./loop_bt $inputTree $query "${outDir}${bname}"
done

