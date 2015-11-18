# Takes in parsed_timing file (from parse_timing.sh) and averages real time and system time
# Outputs real and system time to terminal

import re, sys
import numpy as np

parsed_file = sys.argv[1]

tbm = []
size_fn = []
size_fp = []
dbc=[]
rtb = []
totalBases = []
totalHits = []
TP_mean = []
TP_std = []
FP_mean = []
FP_std = []
numzeros = []
nz_TP_mean = []
nz_TP_std = []
nz_FP_mean = []
nz_FP_std = []

TP_0quart = []
TP_25quart = []
TP_75quart = []
TP_100quart = []
TP_median = []

FP_0quart = []
FP_25quart = []
FP_75quart = []
FP_100quart = []
FP_median = []


#realc = 0.0
#sysc = 0.0
realt = 0.0
syst = 0.0
with open(parsed_file) as bigf:
	for line in bigf:
		line = line.strip()
		if len(line)==0:
			pass
		else:
			parsedLine = line.split(": ")
			if parsedLine[0] == "TP_mean":
				TP_mean.append(round(float(parsedLine[-1]),2))
			if parsedLine[0] == "TP_std":
                                TP_std.append(round(float(parsedLine[-1]),2))
			if parsedLine[0] == "FP_mean":
                                FP_mean.append(round(float(parsedLine[-1]),2))
                        if parsedLine[0] == "FP_std":
                                FP_std.append(round(float(parsedLine[-1]),2))
                        if parsedLine[0] == "numzeros":
                                numzeros.append(round(float(parsedLine[-1]),2))
                        if parsedLine[0] == "nz_TP_mean":
                                nz_TP_mean.append(round(float(parsedLine[-1]),2))
                        if parsedLine[0] == "nz_TP_std":
                                nz_TP_std.append(round(float(parsedLine[-1]),2))
                        if parsedLine[0] == "nz_FP_mean":
                                nz_FP_mean.append(round(float(parsedLine[-1]),2))
                        if parsedLine[0] == "nz_FP_std":
                                nz_FP_std.append(round(float(parsedLine[-1]),2))
			if parsedLine[0] == "TotalHits":
                                totalHits.append(int(parsedLine[-1]))
                        if parsedLine[0] == "TP_0quart":
                                TP_0quart.append(round(float(parsedLine[-1]),2))
                        if parsedLine[0] == "TP_25quart":
                                TP_25quart.append(round(float(parsedLine[-1]),2))
                        if parsedLine[0] == "TP_75quart":
                                TP_75quart.append(round(float(parsedLine[-1]),2))
                        if parsedLine[0] == "TP_100quart":
                                TP_100quart.append(round(float(parsedLine[-1]),2))
                        if parsedLine[0] == "TP_median":
                                TP_median.append(round(float(parsedLine[-1]),2))
                        if parsedLine[0] == "FP_0quart":
                                FP_0quart.append(round(float(parsedLine[-1]),2))
                        if parsedLine[0] == "FP_25quart":
                                FP_25quart.append(round(float(parsedLine[-1]),2))
                        if parsedLine[0] == "FP_75quart":
                                FP_75quart.append(round(float(parsedLine[-1]),2))
                        if parsedLine[0] == "FP_100quart":
                                FP_100quart.append(round(float(parsedLine[-1]),2))
                        if parsedLine[0] == "FP_median":
                                FP_median.append(round(float(parsedLine[-1]),2))
                        if parsedLine[0] == "TotalBases":
                                totalBases.append(round(float(parsedLine[-1]),2))
                        if parsedLine[0] == "RealTotalBases":
                                rtb.append(round(float(parsedLine[-1]),2))
                        if parsedLine[0] == "fnbasesize":
                                size_fn.append(round(float(parsedLine[-1]),2))
                        if parsedLine[0] == "fpbasesize":
                                size_fp.append(round(float(parsedLine[-1]),2))
                        if parsedLine[0] == "totalbasemean":
                                tbm.append(round(float(parsedLine[-1]),2))
                        if parsedLine[0] == "DOUBLECHECK":
                                dbc.append(round(float(parsedLine[-1]),2))
print "tbm = " + str(tbm)
print "total_bases= " + str(rtb)
print "size_fn= " + str(size_fn)
print "size_fp= " + str(size_fp)
print "dbc= " + str(dbc)
print "megabases= " + str(totalBases)
print "hits= " + str(totalHits)
print "tp_mean= " + str(TP_mean)
print "tp_std= " + str(TP_std)

print "tp_0quart= " + str(TP_0quart)
print "tp_25quart= " + str(TP_25quart)
print "tp_75quart= " + str(TP_75quart)
print "tp_100quart= " + str(TP_100quart)
print "tp_median= " + str(TP_median)

print "fp_mean= " + str(FP_mean)
print "fp_std= " + str(FP_std)

print "fp_0quart= " + str(FP_0quart)
print "fp_25quart= " + str(FP_25quart)
print "fp_75quart= " + str(FP_75quart)
print "fp_100quart= " + str(FP_100quart)
print "fp_median= " + str(FP_median)

print "nz_tp_mean= " + str(nz_TP_mean)
print "nz_tp_std= " + str(nz_TP_std)
print "nz_fp_mean= " + str(nz_FP_mean)
print "nz_fp_std= " + str(nz_FP_std)


#print (realt / 60.0) / realc
#print (syst / 60.0) / sysc
#print realc
#print sysc

#print out[x_word]
'''
for k in out_count:
	stringFiles=""
	for k2 in out_list[k]:
		stringFiles = stringFiles + k2 + " "
	print k + " " + str(out_count[k]) + " " + stringFiles
'''
