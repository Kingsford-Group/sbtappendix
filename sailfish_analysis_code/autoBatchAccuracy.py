# Gets the total query set from first argument (a file representing the total query set.)
# - The total query set is currently parsed in as a file which contains a list of files (one per SRR in the set)
# - Each SRR's file contains a different list of all the expressed transcripts output by Salmon / Sailfish
# - Both files are cut to contain only the list and only the transcript names.
# Gets the actual results from second argument (a file representing the analyzeSail.py output from the total query set)
# - This file represents the compiled output (using analyzeSail.py) of the Sailfish / Salmon analysis
# - Queries are represented by the query transcript name followed by the # of hits (and then a space separated list of individual hits)
# Gets the expected results from third argument (a file representing the specific query output from autoQuery) [This tells us query and results]
# - This file is the literal output from the bloom tree with no additional processing.
# - The formatting (for record) is *SEQUENCE COUNT (with the exact vector hits beneath the count)
# Query sequence file was added to convert these sequence outputs to the query transcript's name [to match the SRR hits to the BT hits]
# - It is currently formatted as the path to the query transcript one one line followed by the full sequence on the next
# - This is used to build a dictionary relating transcript and sequence

# The usefulness of salmonBases is questionable. Probably save this as old version and remove.
# As far as I can recall the point was to determine a megabase value for what was correct / what was missed.
# Perhaps just more statistics too
# SalmoBases needed to normalize query like the other parts!
import re, sys
import numpy as np

tqs_f = sys.argv[1]
act_r_f = sys.argv[2]
exp_r_f = sys.argv[3]
querySequenceFile = sys.argv[4]
salmonBases = sys.argv[5]

#Gets the SRRs corresponding to each member of the query set
srr_list=[]
with open(tqs_f) as myFile:
    for line in myFile:
        pl = re.search('/SRR\d*/',line)
        pline=pl.group(0)
        pline=pline[1:len(pline)-1]
        srr_list.append(pline)
temp = set(srr_list)
srr_list = temp

#Initialize the SRR->megabases dictionary
srrbase_list={}
with open(salmonBases) as myFile:
    for line in myFile:
        line = line.strip()
        line = line.split(" ")
        srrfile = line[0]
        bases = line[1]
        if srrfile in srr_list:
            srrbase_list[srrfile]=float(bases)/1000000 #megabases
        else:
            srrbase_list[srrfile]=float(bases)/1000000

#Initialize expected and actual dictionaries
#These have to be dictionaries of dictionaries now? map[query]map[SRRfile]count
exp_r = {}
act_r = {}

#Build query dictionary
# dictionary searches sequence and 'replaces' with transcript file
queryDic = {}
genelist = []
with open(querySequenceFile) as myFile:
    line = "notblank"
    while line:
        line = myFile.readline()
        line = line.strip()
        if len(line) > 0 and line[0]=="/":
            spline = line.split("/")
            temp = spline[-1]
            spline = temp.split(".")
            temp = spline[0]
            
            sequence = myFile.readline()
            sequence = sequence.strip()
            if sequence in queryDic: #Checks for duplicate queries
                #print temp
                #print queryDic[sequence]
                pass
            else:
                queryDic[sequence]=temp 
                genelist.append(temp)

totalHits=0
totalBases=0
realTotalBases=0
realTotalCount=0

with open(exp_r_f) as myFile:
    query=""
    for line in myFile:
        line = line.strip()
        if line[0]=="*":
            sequence = line[1:]
            sequence = sequence.split(" ")
            hitcount = int(sequence[-1])
            totalHits += int(sequence[-1])
            sequence = sequence[0]
            if sequence in queryDic:
                query=queryDic[sequence]
                exp_r[query]={}
                act_r[query]={}
                for afile in srr_list: #initialize moved to here because its based on query
                    exp_r[query][afile]=0
                    act_r[query][afile]=0
        else: #Calculate the megabase size of query set 
            for srrFile in srrbase_list.keys(): #estimate size of remaining search space
                if srrFile in line:
                    realTotalBases+=srrbase_list[srrFile]
                    realTotalCount+=1
                    break
            for afile in srr_list: #calculate the megabase size of what was found (but only within the query set)
                if afile in line:
                    exp_r[query][afile]=1
                    totalBases+=srrbase_list[afile] #Only account for hits if they exist within our set.    

# Build the 'ground truth' set from Salmon / Sailfish processed output.
numHits={}
with open(act_r_f) as myFile:
    for line in myFile:
        line = line.strip()
        for gene in genelist:
            if gene in act_r:
                if gene in line: 
                    split_line = line.split(" ")
                    if len(split_line) > 2:
                        for fn in split_line[2:]:
                            numHits[gene]=int(split_line[1])
                            for afile in srr_list:
                                if afile in fn:
                                    act_r[gene][afile]=1
                    else:
                        numHits[gene]=0

sum_r=0
total=0

numzeros=0
tsum=[]
fsum=[]

otsum=[]
ofsum=[]

testlength=[]
fn_bsize = []
fp_bsize = []
# Build statistics
for gene in genelist:
    total=total+1
    tp_c=0.0
    tp_t=0.0
    tn_c=0.0    
    tn_t=0.0
    fn_c=0.0
    fp_c=0.0

    for afile in srr_list:
        if exp_r[gene][afile]==act_r[gene][afile]:
            sum_r=sum_r+1

        if act_r[gene][afile]==1:
            tp_t+=1
            if exp_r[gene][afile]==act_r[gene][afile]:
                tp_c+=1
            else:
                fn_c+=1
                fn_bsize.append(srrbase_list[afile])
        elif act_r[gene][afile]==0:
            tn_t+=1
            if exp_r[gene][afile]==act_r[gene][afile]:
                tn_c+=1
            else:
                fp_c+=1
                fp_bsize.append(srrbase_list[afile])
    
    if tp_t > 0:
        tsum.append( tp_c / tp_t)
    if tn_t > 0:
        fsum.append(fp_c / tn_t)

    if tp_c == 0:
        for k,v in queryDic.iteritems():
            if v == gene:
                testlength.append(len(k))
        if numHits[gene]==1:
            numzeros+=1
        else:
            numzeros+=1
    else:
        otsum.append(tp_c / (tp_t))
        ofsum.append(fp_c / (tn_t))

tsum = np.array(tsum)
fsum = np.array(fsum)
otsum = np.array(otsum)
ofsum = np.array(ofsum)

nptl = np.array(testlength)

print "fnbasesize: " + str(np.mean(fn_bsize))
print "fpbasesize: " + str(np.mean(fp_bsize))

totalbasemean = 0
count = 0
for k in srrbase_list.keys():
    totalbasemean+=srrbase_list[k]
    count +=1
totalbasemean = totalbasemean/count
print 'totalbasemean: ' + str(totalbasemean) #total bases in the dataset
print "RealTotalBases: " + str(realTotalBases) #total bases BT returns
print "DOUBLECHECK: " + str(realTotalCount) 
print "TotalBases: " + str(totalBases)
print "TotalHits: " + str(totalHits)
print "TP_mean: " + str(np.mean(tsum))
print "TP_std: " + str(np.std(tsum))
print "TP_0quart: " + str(np.percentile(tsum,0))
print "TP_25quart: " + str(np.percentile(tsum,25))
print "TP_75quart: " + str(np.percentile(tsum,75))
print "TP_100quart: " + str(np.percentile(tsum,100))
print "TP_median: " + str(np.median(tsum))

print "FP_mean: " + str(np.mean(fsum))
print "FP_std: " + str(np.std(fsum))
print "FP_0quart: " + str(np.percentile(fsum,0))
print "FP_25quart: " + str(np.percentile(fsum,25))
print "FP_75quart: " + str(np.percentile(fsum,75))
print "FP_100quart: " + str(np.percentile(fsum,100))
print "FP_median: " + str(np.median(fsum))


print "numzeros: " + str(numzeros)
print "nz_TP_mean: " + str(np.mean(otsum))
print "nz_TP_std: " + str(np.std(otsum))
print "nz_FP_mean: " + str(np.mean(ofsum))
print "nz_FP_std: " + str(np.std(ofsum))
