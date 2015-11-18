import glob, os, sys, subprocess

# transcript_file contains a list of fasta files to be queried.
# rna_file contains a list of rnaseq files. They can be input as fasta.gz and paired end files must be on the same line
# timing information is written to out_file.

transcript_file = sys.argv[1]
rna_file = sys.argv[2]
out_file = sys.argv[3]

nmismatch=10

with open(transcript_file) as transF:
    for line in transF:
        line = line.strip()
        trans_line = os.path.basename(line)
        outName = "{}_{}".format(out_file, trans_line)
        print "Query " + trans_line
        with open(rna_file) as rnaF:
            for l2 in rnaF:
                l2 = l2.strip()
                split_l2 = l2.split(" ")
                if len(split_l2)==1:
                    pcall = "./run_ribomap.sh --transcript_fa {} --rnaseq_fq {}  --nmismatch {} --timing_file {}".format(line, split_l2[0], nmismatch, outName)
                elif len(split_l2)==2:
                   pcall = "./run_ribomap.sh --transcript_fa {} --rnaseq_fq {} --rnaseq_fq2 {} --nmismatch {} --timing_file {}".format(line, split_l2[0], split_l2[1], nmismatch, outName) 
                proc = subprocess.call([pcall], shell=True)
                proc = subprocess.call(["sh -c 'echo 1 > /proc/sys/vm/drop_caches'"], shell=True)
