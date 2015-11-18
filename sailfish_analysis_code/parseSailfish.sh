#!/bin/bash

#Batch processes (non parallel) a directory of sailfish outputs (bias corrected).
inputDir="$1"
tpmThresh="$2"
outputLocation="$3"
outlist="$4"

midfix="s1000_t${tpmThresh}"

# Takes in the directory storing the salmon output data and formats them appropriately
# Will only format when the file doesnt already exist (though will rewrite cut each time)
for srr_dir in $(find $inputDir -maxdepth 1 -name "*SRR*" -type d)
do
	my_file="${srr_dir}/quant.sf"
	out_file="${srr_dir}/quant_${midfix}.sf" #s1000_t${tpmThresh}.sf"
	cut_out="${srr_dir}/cut_quant_${midfix}.sf" #s1000_t${tpmThresh}.sf"
	if [ -f $my_file ]; then
		if [ -f $out_file ]; then
			echo "File ${out_file} already exists"
		else
		    python sailParse.py $my_file $tpmThresh > $out_file
		fi
		cat ${out_file} | cut -d' ' -f1 > $cut_out
		echo ${cut_out} >> $outlist
		size=$(wc -l $out_file)
		echo "$size" >> $outputLocation	
	else
		echo "Error: Could not find ${my_file}"
# ${srr_dir}sorted_quant_bias_corr.sf
	fi
done

# Compiles the 'true' expression patterns output by Salmon for provided query set
# (Takes in what we already queried)
queryFile="/mnt/scratch1/salmonAnalyzed/sail-0.6.3/oldnew_${midfix}_sailfishQueries.txt"
oldqueryFile="/mnt/scratch1/salmonAnalyzed/sail-0.6.3/old_salmon_queries/old_${midfix}_sailfishQueries.txt"
# This is the old file and we are going to parse out just the random query set already used
salmonQueries="/mnt/scratch1/salmonAnalyzed/${midfix}_salmonQueries.txt"
if [ -f $queryFile ]; then
	echo "Error: $queryFile already exists"
else
    #print "Pass!"
    #python buildExisting.py ${outlist} ${salmonQueries} ${oldqueryFile}
	python analyzeSail.py ${outlist} 100 ${queryFile}
fi

# Builds sailfish queries using the index provided from /data/common/all_human_transcripts.fa
queryFolder="/mnt/scratch1/salmonQueries/salmon_3_17/sail-0.6.3/${midfix}/"
if [ -d $queryFolder ]; then
	echo "$queryFolder already exists"
else
    #print "ugh\n"
	mkdir -p $queryFolder
	python buildQuerySet.py $queryFile /data/common/all_human_transcripts.fa $queryFolder
fi

mergedqueryFile="/mnt/scratch1/salmonQueries/salmon_3_17/sail-0.6.3/merged_salmonQueries_${midfix}.txt"
mergedkeyFile="/mnt/scratch1/salmonQueries/salmon_3_17/sail-0.6.3/merged_salmonQueries_${midfix}_key.txt"
if [ -f $mergedqueryFile ]; then
	echo "$mergedqueryFile already exists"
else
    #print "Passed"
	./mergeQuerySet.sh $queryFolder $mergedqueryFile $mergedkeyFile
fi

#outprefix="/mnt/scratch1/salmonResults/merged_salmonQueries_${midfix}"
#cd ..
#./loop_bt.sh /mnt/scratch2/full_BT_12_19_compressed_out.txt $mergedqueryFile $outprefix 0
