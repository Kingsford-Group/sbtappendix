import os, glob
import re, sys

# SalmonBeta-v0.2.2_ubuntu-14.04/bin/
# salmon quant -i transcripts_index -r reads.fa -o transcripts_quant
# Checking all files to determine orientation, if not obvous, default to IU
# salmon quant -i transcripts_index -l IU -1 reads1.fa -2 reads2.fa -o transcripts_quant

srrdir = sys.argv[1]
outhead =sys.argv[2]
#print srrdir
#print os.path.dirname(srrdir) +"/SRR*.gz"
unique_srr =  set([f.split(".")[0].split("_")[0] for f in glob.glob(os.path.dirname(srrdir) +"/SRR*.gz")])
#print unique_srr
for srr in unique_srr:
    outname = outhead +os.path.basename(srr)
    print srr
    files = sorted(glob.glob("{}*".format(srr)))
    print files
    if len(files) == 1:
        #print files[0]
        #print "Skipping single files!"
        os.system("./script-run-sailfish-single.sh {} {}".format(files[0], outname))
    elif len(files) == 2:
        #print files[0]
        #print files[1]
        #print outname
        os.system("./script-run-sailfish-pair.sh {} {} {}".format(files[0], files[1], outname))
    else:
        print "This should not happen"
        exit(1)

