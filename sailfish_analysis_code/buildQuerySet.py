# Takes in 'analyzed' sailfish output files (or some subset of the overall file) and builds a separate file for each
# using the sailfish query results from /data/common/all_human_transcripts.fa

import re, sys

inputFile = sys.argv[1]
fastaIndex = sys.argv[2]
outputFolder = sys.argv[3]

#Build gene list
geneList=[]
with open(inputFile) as inpf:
	for gene in inpf:
		gene = gene.strip()
		gene = gene.split(" ")
		gene = gene[0]
		gene = gene.strip()
		geneList.append(gene)

#Explore index for everything in genelist. Print when found any element

internal=0
DNA=""
with open(fastaIndex) as index:
	for line in index:
		line = line.strip()
		if len(line) == 0:
			pass
		elif internal==0:
			if line[0] == '>':
				line = line[1:]
				for gene in geneList:
					if line == gene:
						internal=1
						DNA=""
						outName = outputFolder + gene + ".txt"
						outFile = open(outName,'w')
						#outFile.write("MAYBE PUT THE FILES FOUND HERE")
		elif internal==1:
			if line[0] == '>':
				outFile.write(DNA)
				outFile.close()
				internal=0
				line = line[1:]
                                for gene in geneList:
                                        if line == gene:
                                                internal=1
                                                DNA=""
                                                outName = outputFolder + gene + ".txt"
                                                outFile = open(outName,'w')
				
			else:
				DNA = DNA + line
