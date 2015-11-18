srrbase_list=[]
salmonBases="sail-0.6.3_srr_sizes.txt"

totalBases = 0.0
with open(salmonBases) as myFile:
    for line in myFile:
        line = line.strip()
        line = line.split(" ")
        srrfile = line[0]
        bases = line[1]
        totalBases+=float(bases)/1000000

print totalBases