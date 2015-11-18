#!/usr/bin/env python

import os
import urllib2
import urllib
import requests
import time
import sys
import random

from HTMLParser import HTMLParser

fasta_folder = "/home/bradsol/Desktop/srablast/queries/" #raw_input('Enter Fasta File Location... ').strip()
SRR_list = "full_BT_srr_3_17.txt" #str(raw_input('Enter SRR Databases to search separated by a single space...'))
out_file = 'results/sbt_timing3.txt'
timeout_file = 'results/sbt_failure3.txt'
#fasta_file = 'final_fasta_2.txt'

outf = open(out_file,'w')
toutf = open(timeout_file,'w')
#foutf = open(fasta_file,'w')

fasta_list = []
if os.path.isdir(fasta_folder):
	file_path = fasta_folder
	for filename in os.listdir(fasta_folder):
		fasta_list.append(filename)
		#foutf.write(filename+"\n")
	#print fasta_list
	#file_path = os.path.dirname(fasta_file) + '/'
	#file_name = os.path.basename(fasta_file)
else:
	print "Invalid File Path, File Doesn't exist"
	sys.exit()



srrlist = []
with open(SRR_list) as srrin:
	for line in srrin:
		srrlist.append(line.strip())

for file_name in fasta_list:
	randset = random.sample(srrlist,2)
	for database_num in randset:
		tic = time.time()
		url = ('http://www.ncbi.nlm.nih.gov/blast/Blast.cgi')
		args = {'CMD' : 'Put','DATABASE':database_num,'PROGRAM':'blastn',
					'BLAST_PROGRAMS':'discoMegablast','MATCH_SCORES':'1,-2',
					'BLAST_SPEC':'SRA','FORMAT_TYPE':'XML','FILTER':'L',
					'HITLIST_SIZE':'20000','GAPCOSTS':'5 2','MAX_NUM_SEQ':'20000'}

		#print "stuck during req"
		req = requests.post(url,params=args,files={'QUERY': open(file_path + file_name, 'rb')})


		webpage = req.text

		RID = ''
		RTOE = 0
		status = False
		class NCBIblastStatusParser(HTMLParser):
			def handle_comment(weird,info):
				global RID
				global RTOE
				global status
				infostr = str(info)
				if infostr.startswith('QBlastInfoBegin'):
					ridstr = infostr.find('RID')
					rtoestr = infostr.find('RTOE')
					rtoeend = infostr.find('QBlastInfoEnd')
					if ridstr != -1:
						if infostr[(rtoestr+7):(rtoeend-1)] != '':
							RID = infostr[(ridstr+6):(rtoestr-5)]
							RTOE = int(infostr[(rtoestr+7):(rtoeend-1)])
							print 'RID = ' + RID
							print 'Est Time = ' + str(RTOE)
							
						else:
							print "There was an error."
							sys.exit()
					
		#print "stuck during parser"
		parser = NCBIblastStatusParser()
		for line in webpage:
			parser.feed(line)

		time.sleep(RTOE / 2.0)
		check_count = 0
		sleep_time = 2

		timedout=False
		pot_except=False

		

		#print "stuck waiting for blast to finish"
		while status == False:
			valid_page=False
			getURL = ('http://www.ncbi.nlm.nih.gov/blast/Blast.cgi?'
				'CMD=Get&'
				'RID=' + RID )
			try:
				datapage = requests.get(getURL, timeout=5)
			except Exception as e:
				print e
				status =True
				timedout=True
				break
			except:
				print 'Alternative exception checker'
				status = True
				timedout=True
				break
			
			#print datapage
			for line in datapage:
				if line.find('READY') != -1: #Looks for Status=READY
					#print line
					status = True
					valid_page=True
				elif line.find('STATUS') != -1:
					valid_page = True
				
			if valid_page == False:
				print "Potential exception found. Datapage contains no status and likely finished."
				pot_except=True
				status = True

			#print "Still Blasting"
			check_count += 1
			if check_count == 10:
				sleep_time += 2
				print "Adding 2 seconds to check interval (sleep_time= " + str(sleep_time) + ")"
				check_count = 0
				
				if sleep_time > 30:
					print "Sleep time too long. Breaking."
					timedout=True
					status=True
			time.sleep(sleep_time)

		# used to be here (after status says yes)

		if timedout==False:
			print "Completed BLAST"
			toc = time.time()
			print "Query: " + file_name + " " + database_num +"\n"
			print "Time elapsed: " + str(toc - tic) + " +/- " + str(sleep_time)
			outf.write("Query: " + file_name + " " + database_num +"\n")
			outf.write("Time: " + str(RTOE) + " " + str(toc - tic) + " " + str(sleep_time) + "\n")
		elif pot_except==True:
			print "Hypothesized Exception Occured."
			toc = time.time()
			print "Query: " + file_name + " " + database_num +"\n"
			print "RID: " + RID
			print "Sleep Time: " + str(sleep_time)
			toutf.write("Hypothesized Exception Occured")
			toutf.write("Query: " + file_name + " " + database_num +"\n")
			toutf.write("Time: " + str(toc - tic) + " " + str(sleep_time) + "\n")
			toutf.write("RID: " + RID + "\n")
			toutf.write("Sleep Time: " + str(sleep_time) + "\n")
		else:
			toc = time.time()
			print "Failure, script timed out."
			print "Query: " + file_name + " " + database_num +"\n"
			print "RID: " + RID
			print "Sleep Time: " + str(sleep_time)
			toutf.write("Script Timed Out (5 Second wait). \n")
			toutf.write("Query: " + file_name + " " + database_num +"\n")
			toutf.write("Time: " + str(toc - tic) + " " + str(sleep_time) + "\n")
			toutf.write("RID: " + RID + "\n")
			toutf.write("Sleep Time: " + str(sleep_time) + "\n")
		#print tic
		#print toc


		'''
		getURL = ('http://www.ncbi.nlm.nih.gov/blast/Blast.cgi?'
				'CMD=Get&'
				'FORMAT_TYPE=XML&'
				'MAX_NUM_SEQ=100000&'
				'RESULTS_FILE=yes&'
				'RID=' + RID )

		r = requests.get(getURL, stream=True)
		with open(RID+'.xml', 'wb') as f:
			for chunk in r.iter_content(chunk_size=1024): 
				if chunk: # filter out keep-alive new chunks
					f.write(chunk)
					f.flush()
		'''
