# Takes in list of sailfish parsed output files [file of files (fof)] (the ones cut to just have gene names)
# and organizes the total counts into space separated (gene ' ' count ' ' list of files)
# The list of files is also space separated

import re, sys
import random

fof = sys.argv[1] #File of files of Sailfish/Salmon output
queryfile = sys.argv[2] #Salmon query file. The first word .
outFile = sys.argv[3] #Writes the compiled information to this file.
outFile += "_safe"

lc=0
out_count={}
out_list={}
outp1=0.0
outp2=0.0

with open(fof) as bigf:
	for fileName in bigf:
		fileName = fileName.strip()
		with open(fileName) as f:
			for line in f:
				line = line.strip()
				parsedLine = line.split(" ")
				gene_id = parsedLine[0]
				if gene_id in out_count:
					out_count[gene_id]=out_count[gene_id]+1
					out_list[gene_id].append(fileName);
				else:
					out_count[gene_id]=1
					out_list[gene_id]=[fileName]

print len(out_count.keys())

subset=[]
with open(queryfile) as qf:
    for line in qf:
        line = line.strip()
        parsedLine = line.split(" ")
        gene_id = parsedLine[0]
        if gene_id in out_count.keys():
            subset.append(gene_id)
        #else:
        #    print "Error: " + gene_id + " does not appear in sailfish estimates"
            #quit() 
#subset=random.sample(out_count.keys(), randsize)
out=open(outFile,'w')

for k in subset:
    stringFiles=""
    if k not in out_list:
        out.write(k + " 0 \n")
    else:
        for k2 in out_list[k]:
                stringFiles = stringFiles + k2 + " "
        out.write(k + " " + str(out_count[k]) + " " + stringFiles + "\n")
