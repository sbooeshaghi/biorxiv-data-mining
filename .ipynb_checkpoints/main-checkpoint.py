#!/usr/bin/env python
"""
Created on Thu Dec 21 2017

@author: alisina (Sina Booeshaghi)

main.py
---
This is the main file for scraping pdfs from BioArxIv. It calls scrapeDOI
which scrapes the DOI links from all of the pages (specified within scrapeDOI).
Then it goes to the doi link, determines if it was published in a journal, and 
then downloads the pdf to the folder of the journal name
"""
import timeit
start_time = timeit.default_timer()
import dryscrape
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import time
from scrapeDOI import scrapeDOI
import urlparse
import urllib2
import os
import sys
from collections import OrderedDict
import json
import textract
import numpy as np
import pandas as pd
from dloadPDF import download

from sort import sort


# TODO: get Title abstract, date posted, author information and print it to a .txt file
# add file to its own folder
# Abstract, title, affiliation, date posted

#URL = "https://www.biorxiv.org/content/early/2016/05/19/054379" # published
#URL = "https://www.biorxiv.org/content/early/2018/01/03/233700" # not published RETURNS EMPTY STRING
#URL = "https://www.biorxiv.org/content/early/2013/11/11/000265"
try:
	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	driver = webdriver.Chrome(chrome_options=options)

	doiLinks = scrapeDOI()
	# print doiLinks
	download_path = os.getcwd() + '/downloads'
	doJ = {} #{'Pre-print':0, 'Science':0, 'Nature':0, 'Cell':0} # key is the journal name, value is the number of journals

	# create pandas dataframe for storing all of this information
	preload = {'Date Posted': None,
	 			'Title': None, 
	 			'Authors': [None, None],
	 			'Journal': None,
	 			'Link': None,
	 			'Abstract': None,
	 			'Text': None}
	# note to add a dictionary with lists as values, to a dataframe, do 
	# pd.DataFrame([dictionary]) where you use the [.] 
	df = pd.DataFrame([preload])
	## when indexing into the dataframe, the order of the columns will be 
	##  	Abstract 	Authors 	Date 	Posted 	Journal 	Link 	Text 	Title
	##	0	None		[NaN, NaN]	NaN 	NaN 	NaN 		NaN 	NaN 	NaN
	## 
	## to add a row 
	for link in doiLinks:
		# initialize a dictionary to write all of the properties to so that
		# you can use JSON dump
		info2write = {}

		print '[*-----] Connecting to page..'
		driver.get(link)
		innerHTML = driver.execute_script('return document.body.innerHTML')
		soup = BeautifulSoup(innerHTML, 'html5lib')
		print '[**----] Page connected! Grabbing contents, please wait.'
		
		## Find out where it as published (if any) jrnl may be empty
		jrnl = soup.find_all('i')

		## Figure out how to label the jrnl name (this was hard for some reason)
		if jrnl:
			jrnl = jrnl[-1].text
			if not jrnl:
				jrnl = 'Pre-print'
		elif not jrnl:
			jrnl = 'Pre-print'

		## Note that the jrnl you just downloaded needs to be incremented
		if jrnl in doJ:
			doJ[jrnl] += 1
		else:
			doJ[jrnl] = 1

		## Find HTML with first and sur names
		fnames = soup.find_all('span', {'class':'nlm-given-names'})
		snames = soup.find_all('span', {'class':'nlm-surname'})
		
		## Get the names in an array of strings
		fnames = [fir.getText() for fir in fnames]
		snames = [sur.getText() for sur in snames]

		## Remove duplicates, now element snames(i), fnames(i) is Surname, Firstname
		fnames = list(OrderedDict.fromkeys(fnames))
		snames = list(OrderedDict.fromkeys(snames))

		## Put the authors names into a dict
		authors = list(zip(snames, fnames))

		## Find out when the article was posted to the Arxiv
		date_posted = soup.find('li', {'class':'published'}).getText()
		date_posted = date_posted[7:-1]

		## Get the abstract text
		abstract = soup.find('p', {'id' : 'p-2'}).getText()

		## Get the title of the paper
		title = soup.find('h1', {'id' : 'page-title'}).getText()

		print '[***---] Published in: ' + jrnl

		## Download pdf routine
		for tag in soup.find_all('a', href=True): 
			# find <a> tags with href in it 

			# now take all of those links and split them to find which link has .pdf in it
			linkname = os.path.basename(tag['href'])
			linksplit = os.path.splitext(linkname)

			## if the link is a pdf then download it
			if linksplit[1] == '.pdf':
				## open the url
				current = urllib2.urlopen(tag['href'])
				new_file_name = jrnl + str(doJ[jrnl]) + '.pdf'
				print "[****--] Downloading: ", new_file_name
				# download the document
        		with open(download_path + '/' + new_file_name, 'wb') as f:
					f.write(current.read())

        #a = download(soup, download_path, jrnl, doJ)
        
		# print abstract to text file
        ab_file_name = jrnl + str(doJ[jrnl]) + '.txt'
        text = textract.process(download_path + '/'+new_file_name)
        print '[*****-] PDF converted to a text file.'
        
        info = [abstract, authors, date_posted, jrnl, link, text, title]
        
        end = df.shape[0]
        df.loc[end] = info
        print '[******] Relevant paper info written to a text file.\n'
		## 
        print 'Moving on to grab the next paper.'
	## Close the session		
	driver.quit()


except KeyboardInterrupt:
	print "\n[*] Exiting..."
	sys.exit(1)

## swap the data frame columns to an order that makes more sense
# date_posted, title, jrnl, authors, link, abstract, text
columns = ['Date Posted', 'Title', 'Journal', 'Authors', 'Link', 'Abstract', 'Text']
df = df[columns]

# Save the pandas dataframe to a csv
# Get rid of the placeholder with all of the Nones
df.drop(0, inplace=True)
# write the dataframe to a CSV
name_of_csv = 'data.csv'
path_to_save_csv = download_path + '/' + name_of_csv
df.to_csv(path_to_save_csv, encoding='utf-8', index=False)


sort(doJ)
num_downloaded = sum(doJ.values())
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