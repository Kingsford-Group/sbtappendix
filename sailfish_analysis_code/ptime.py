# Takes in parsed_timing file (from parse_timing.sh) and averages real time and system time
# Outputs real and system time to terminal

# THIS HAS BEEN CRUDELY REDESIGNED TO LIMIT REAL TIME (AND REAL TIME ALONE) to 4 HOURS AT MOST

import re, sys
import numpy as np

parsed_file = sys.argv[1]

real_list=[]
sys_list=[]
user_list=[]
#realc = 0.0
#sysc = 0.0
realt = 0.0
syst = 0.0
usert = 0.0
max_time=14400 #4 hours in seconds
maxed_count = 0
with open(parsed_file) as bigf:
    for line in bigf:
        line = line.strip()
        if len(line)==0:
            pass
        else:
            parsedLine = line.split("\t")
            if parsedLine[0] == "real":
                temp=parsedLine[1].split("m")
                realt = 60.0 *float(temp[0])
                #realc = realc + 1
                temp2 = temp[1].split("s")
                realt = realt + float(temp2[0])
                if realt > max_time:
                    real_list.append(max_time)
                    maxed_count+=1
                else:
                    real_list.append(realt)
            if parsedLine[0] == "sys":
                temp=parsedLine[1].split("m")
                syst = 60.0 *float(temp[0])
                #sysc = sysc + 1
                temp2 = temp[1].split("s")
                syst = syst + float(temp2[0])
                sys_list.append(syst)
            if parsedLine[0] == "user":
                temp=parsedLine[1].split("m")
                usert = 60.0 *float(temp[0])
                #sysc = sysc + 1
                temp2 = temp[1].split("s")
                usert = usert + float(temp2[0])
                user_list.append(usert)
print maxed_count
#print len(real_list)
print sum(real_list)
print sum(user_list)
#print len(user_list)
#print sum(user_list)
print np.mean(real_list)
print np.std(real_list)

print np.mean(user_list)
print np.std(user_list)
#print len(sys_list)
#print sum(sys_list)

print np.mean(sys_list)
print np.std(sys_list)
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
