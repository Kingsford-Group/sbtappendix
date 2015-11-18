import glob, os, sys

sizeFile = sys.argv[1] #~/algae/full_BT_sizes_3_17.txt
srrFile = sys.argv[2] #~/algae/bloomtree/src/sailSuite/newSailPipe/sail_query_list.txt
outFile = sys.argv[3]

srrlist = []
with open(srrFile) as myFile:
    for line in myFile:
        line=line.strip()
        srrlist.append(line)

with open(sizeFile) as myFile:
    for size in myFile:
        line = size.split(" ")
        if line[0] in srrlist:
           # Apparently I don't need to finish this. 
