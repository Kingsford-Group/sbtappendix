import re, sys
import numpy as np
import random

parsed_file = sys.argv[1]
parsed_file2 = sys.argv[2]

real_list=[]
q_list = []
rpmb_list = []
size_list = []

useNext=0
srr_size=0.0
time_limit = 1000000

#Initialize the SRR->megabases dictionary
srrbase_list={}
salmonBases="full_BT_sizes_3_17.txt"
with open(salmonBases) as myFile:
    for line in myFile:
        line = line.strip()
        line = line.split(" ")
        srrfile = line[0]
        bases = line[1]
        srrbase_list[srrfile]=float(bases)/1000000

#We ran more then 100 runs but to be consistent we take the first 100 corresponding to each transcript.
with open(parsed_file) as pf:
	for line in pf:
		line = line.strip()
		if len(line)==0:
			pass
		else:
			if "Query" in line:
				parsedLine = line.split(" ")
				query = parsedLine[1]
				srr_id = parsedLine[2]
				if query in q_list:
					pass
				else:
					q_list.append(query)
					srr_size = srrbase_list[srr_id]
					useNext=1
			if useNext==1 and "Time" in line:
				useNext = 0
				parsedLine = line.split(" ")
				est_time = float(parsedLine[1])
				real_time = float(parsedLine[2])
				plus_minus = float(parsedLine[3])
				fastest_time = real_time - plus_minus
				size_list.append(srr_size)
				if fastest_time > time_limit:
					real_list.append(time_limit)
					rpmb_list.append(time_limit/srr_size)
				else:
					real_list.append(real_time - plus_minus)
					rpmb_list.append((real_time - plus_minus)/srr_size)

with open(parsed_file2) as pf:
	for line in pf:
		line = line.strip()
		if len(line)==0:
			pass
		else:
			if "Query" in line:
				parsedLine = line.split(" ")
				query = parsedLine[1]
				srr_id = parsedLine[2]
				if query in q_list:
					pass
				else:
					q_list.append(query)
					srr_size = srrbase_list[srr_id]
					useNext=1
			if useNext==1 and "Time" in line:
				useNext = 0
				parsedLine = line.split(" ")
				est_time = float(parsedLine[1])
				real_time = float(parsedLine[2])
				plus_minus = float(parsedLine[3])
				size_list.append(srr_size)
				if fastest_time > time_limit:
					real_list.append(time_limit)
					rpmb_list.append(time_limit/srr_size)
				else:
					real_list.append(real_time - plus_minus)
					rpmb_list.append((real_time - plus_minus)/srr_size)


#q_list.sort()

#print rpmb_list 
#print real_list

totalTime = sum(real_list)
totalSize = sum(size_list)

print totalTime/totalSize
#random.shuffle(rpmb_list)

#subset=rpmb_list[0:100]
'''
print len(rpmb_list)
print sum(rpmb_list)
#print len([i for i in rpmb_list if i<=60.0])
#print np.mean([i for i in rpmb_list if i<=60.0])
#print np.mean(rpmb_list[rpmb_list<60])
print np.mean(rpmb_list)
print np.std(rpmb_list)

print len(real_list)
print sum(real_list)
print np.mean(real_list)
print np.std(real_list)'''