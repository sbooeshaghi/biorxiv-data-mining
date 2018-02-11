#!/usr/bin/env python
"""
Created on Thu Jan 4 2018

@author: alisina (Sina Booeshaghi)

sort.py
---
Sorts downloaded pdfs into their respective journal folders for better management.
"""

import os
import os.path
import shutil
import pdb

def sort(dictOfJournals):
	current_directory = os.getcwd()
	pdf_directory = current_directory + '/downloads'

	directory_files = os.listdir(pdf_directory)

	for journal_name in dictOfJournals:
		try:
			if journal_name not in os.listdir(pdf_directory):
				os.makedirs(pdf_directory + '/'+ journal_name)
				#pdb.set_trace()
			else:
				print journal_name + ' already has a directory.'
		except:
			continue
	#pdb.set_trace()
	for file in directory_files[1:]:
		fname = file[:-4]
		jrnl = fname.rstrip('0123456789')
		source = pdf_directory + '/' + file
		#print 'Source is : ' + source
		destination = pdf_directory + '/'+ jrnl
		#print 'Destination is : ' + destination
		#pdb.set_trace()
		try:
			if os.path.isfile(pdf_directory + '/' + file):
				shutil.move(source, destination)
				#pdb.set_trace()
			else:
				#pdb.set_trace()
				print 'No file to move.'
				continue
		except:
			continue
