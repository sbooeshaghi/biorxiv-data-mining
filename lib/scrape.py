"""
Created on Thu Dec 21 2017

@author: alisina (Sina Booeshaghi)

scrape.py
---
This is the scrape file for scraping pdfs from biorxiv. It calls scrapeDOI
which scrapes the DOI links from all of the pages (specified within scrapeDOI).
Then it goes to the doi link, determines if it was published in a journal, and 
then downloads the pdf to the folder of the journal name
"""

import timeit
start_time = timeit.default_timer()

from selenium import webdriver
from bs4 import BeautifulSoup
import time
import os
import sys
#import textract
import numpy as np
import pandas as pd
import re

# sina's functions
from dloadPDF import download
from getInfo import getInfo
from scrapeDOI import scrapeDOI
from pdfchanger import convert
#from mlMain import mlMain
from sort import sort
#TODO the webdriver gets stuck and will "hang" for some reason. check it out
import json


def scrape(doiLinks):
	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	driver = webdriver.Chrome(chrome_options=options)

	#doiLinks = scrapeDOI()
	download_path = os.getcwd() + '/downloads'
	data_path = os.getcwd() + '/data'
	doJ = {} #{'Pre-print':0, 'Science':0, 'Nature':0, 'Cell':0} # key is the journal name, value is the number of journals
	num_data = 1
	# create pandas dataframe for storing all of this information
	preload = {'Date Posted': None,
	 			'Title': None, 
	 			'Authors': [None, None],
	 			'Journal': None,
	 			'Link': [None, None],
	 			'Abstract': None,
	 			'Text': None,
	 			'Twitter': [None, None]}
	# note to add a dictionary with lists as values, to a dataframe, do 
	# pd.DataFrame([dictionary]) where you use the [.] 
	#df = pd.DataFrame([preload])
	storage = {}
	storage['papers'] = []
	## when indexing into the dataframe, the order of the columns will be 
	##  	Abstract 	Authors 	Date 	Posted 	Journal 	Link 	Text 	Title 	Twitter
	##	0	None		[NaN, NaN]	NaN 	NaN 	NaN 		NaN 	NaN 	NaN 	NaN
	## 
	## to add a row 
	total_num = len(doiLinks)
	counter = 1
	for link in doiLinks:
		ind = doiLinks.index(link)
		print 'Number of papers left to download: ' + str(total_num-ind)

		print '[*-----] Connecting to page..'

		## connect to the page
		driver.get(link)
		innerHTML = driver.execute_script('return document.body.innerHTML')
		soup = BeautifulSoup(innerHTML, 'html5lib')
		print '[**----] Page connected! Grabbing contents, please wait.'

		# grabbing all relevant data from page
		(jrnl, authors, date_posted, abstract, title, twitter, real_link, doJ) = getInfo(soup, doJ)
		new_file_name = jrnl + str(doJ[jrnl]) + '.pdf'
		print '[***---] Published in: ' + jrnl

		# download the pdf
		if jrnl != 'DOI Not Found':
			download_ok = download(soup, download_path, new_file_name)
		else:
			download_ok = None
		# in case the file is not accessible

		if download_ok != None:
			text_loc = download_ok
		else:
			# get loc for pdf to do pdf to txt later
			text_loc = download_path + '/'+ jrnl + '/' + new_file_name
			print '[*****-] PDF location written.'
		both_links = [link, real_link]
	    # write all of the info to the dataframe
		storage['papers'].append({'date': date_posted,
			'title': title, 
			'authors': authors,
			'journal': jrnl,
			'link': real_link,
			'abstract': abstract,
			'text': text_loc,
			'twitter': twitter})
		#info = [abstract, authors, date_posted, jrnl, both_links, text_loc, title, twitter]
		#end = df.shape[0]
		#df.loc[end] = info
		print '[******] Relevant paper info written to a text file.\n'
		
		print 'Moving on to grab the next paper.\n'

		if counter % 1025 == 0:
			
			#print 'Pausing for 30 sec so we dont look like a DDOS attack..'
			#time.sleep(30)
			#columns = ['Date Posted', 'Title', 'Journal', 'Authors', 'Link', 'Abstract', 'Text', 'Twitter']
			#df = df[columns]

			# Get rid of the Nones placeholder and save the pandas dataframe to a csv 
			#df.drop(0, inplace=True)
			name_of_txt = 'data' + str(num_data) + '.txt'
			path_to_save_txt = data_path + '/' + name_of_txt
			with open(path_to_save_txt, 'w') as outfile:  
				json.dump(storage, outfile)
			#df.to_json(path_to_save_csv, index=False)
			#df = pd.DataFrame([preload])
			num_data += 1
		counter += 1
	    
	## Close the session		
	driver.quit()


	# except KeyboardInterrupt:
	# 	print "\n[*] Exiting..."
	# 	return df
	# 	sys.exit(1)

	# except Exception as ex:
	#     template = "An exception of type {0} occurred. Arguments:\n{1!r}"
	#     message = template.format(type(ex).__name__, ex.args)
	#     print message

	## swap the data frame columns to an order that makes more sense
	# date_posted, title, jrnl, authors, link, abstract, text
	#columns = ['Date Posted', 'Title', 'Journal', 'Authors', 'Link', 'Abstract', 'Text', 'Twitter']
	#df = df[columns]

	# Get rid of the Nones placeholder and save the pandas dataframe to a csv 
	#df.drop(0, inplace=True)
	#name_of_csv = 'data' + str(num_data) + '.csv'
	#path_to_save_csv = data_path + '/' + name_of_csv
	#df.to_json(path_to_save_csv, index=False)

	name_of_txt = 'data' + str(num_data) + '.txt'
	path_to_save_txt = data_path + '/' + name_of_txt
	with open(path_to_save_txt, 'w') as outfile:  
		json.dump(storage, outfile)

	# sort all of the files into folders
	sort(doJ)
	num_downloaded = sum(doJ.values())

	# print out a summary of everything
	with open(download_path + '/'+ 'summary.txt', 'wb') as f:
		f.write('SUMMARY OF PAPERS DOWNLOADED FROM THE BIOARXIV\n\n')
		f.write('Total number of papers downloaded: ' + str(num_downloaded)) 
		f.write('\n\n')
		f.write('NUMBER OF PAPERS PER JOURNAL\n')
		for key, value in doJ.items():
			f.write('%s:%s\n' % (key, value))
		f.write('\n\n')
		elapsed = (timeit.default_timer() - start_time)/60
		f.write('Your session took this long to run [min]: ' + str(elapsed))

	print 'Sorted all files. A summary of your session is available in ../downloads/summary.txt'
	elapsed = (timeit.default_timer() - start_time)/60
	print 'Your session took this long to run [min]: ' + str(elapsed)
	return doJ


#if __name__ == "__main__":
#	scrape()
