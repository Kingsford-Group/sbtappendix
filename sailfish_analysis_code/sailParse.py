#!/usr/bin/python

#Reads in a quant_bias_corr file
# Outputs something?
import re, sys
import numpy

try:
	inputFile = sys.argv[1]
	tpmThresh = float(sys.argv[2])
except:
	exit('Need to supply an input file!')

f = open(inputFile)
lines = f.readlines()
f.close()
#print len(lines)
parsed_file=[]
#print lines[0]

# split every line into its component rows
# Dont forget that 0 is starting index, sailfish index in paren (starts at 1)
# 0(1) = Name,
# 1(2) = Length,
# 2(3) = TPM
# 4(5) = KPKM
for line in lines:
	if line[0]=="#":
		pass
	else:
		par_line = line.split()
		if float(par_line[1]) >= 1000: #Ensure queries are not too small (was 400)
			if float(par_line[2]) >= tpmThresh: #Experimental median of random set of non-expressed files
				parsed_file.append(par_line)
		#print parsed_file
#print parsed_file[100]

for line in parsed_file:
	print " ".join(map(str,line))
