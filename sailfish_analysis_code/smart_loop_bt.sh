#!/bin/bash

# Loops over all threshold values and queries the bloom tree for the given query and query type
# Currently will not query if the same file already exists

TREE="$1"
INFILE="$2"
OUT_PREFIX="$3"
THRESHOLD="$4"
#trap 'worker=`expr $worker - 1`' USR1
#".7" ".8" ".9"
#".5" ".6" ".7" ".8" ".9" "1"
# ".9" ".8" ".7" ".6" ".5"
#".5" ".6" ".7" ".8" ".9" "1"
	if [ -f "${OUT_PREFIX}_out_t${THRESHOLD}.txt" ]; then
		echo "Error: ${OUT_PREFIX}_out_t${THRESHOLD}.txt already exists"
	else
		(time ./bt query -t $THRESHOLD $TREE $INFILE "${OUT_PREFIX}_out_t${THRESHOLD}.txt") > "${OUT_PREFIX}_visited_t${THRESHOLD}.txt" 2> "${OUT_PREFIX}_timing_t${THRESHOLD}.txt"
		sh -c 'echo 1 > /proc/sys/vm/drop_caches' #potentially need to sudo this
	fi
