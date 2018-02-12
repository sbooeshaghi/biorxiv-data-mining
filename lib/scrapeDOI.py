# Python Program to scrape DOI Links from Bioarxiv

import requests
from bs4 import BeautifulSoup

def scrapeDOI():
	doiLinks = []
	n = 3 # number of pages to scrape
	baseURL = "https://www.biorxiv.org/content/early/recent?page="

	# first find out how many pages to iterate through
	page1 = "https://www.biorxiv.org/content/early/recent?page=1"
	r = requests.get(page1)
	soup = BeautifulSoup(r.content, 'html5lib')
	lp = soup.find('li', {'class': 'pager-last last odd'})
	lp_num = int(lp.getText()) # the way they index is from 1:n-1
	r.close()
	# to scrape from end to beginning, run the loop backwards
	# for pageNum in reversed(xrange(1, lp_num)):
	# 	--begin code here--
	start_page = 1000
	for pageNum in reversed(xrange(start_page, lp_num-1)):
	#for pageNum in [lp_num-1]:

		URL = baseURL + str(pageNum)
		print URL
		r = requests.get(URL)

		soup = BeautifulSoup(r.content, 'html5lib')

		table = soup.find_all('span')#, attrs = {'id':'container'})

		titles = soup.find_all('span', attrs={'class':'highwire-cite-title'})
		#fnames = soup.find_all('span', attrs={'class':'nlm-given-names'})
		doi = soup.find_all('span', attrs={'class':'highwire-cite-metadata-doi highwire-cite-metadata'})

		for row in doi:
			doiLink = row.text[5:]

			# the format is like doi: https://doi.org/10.1101/081455
			doiLinks.append(doiLink)

	return doiLinks

#for i in table:
#	print i.prettify()

#print type(table)
#print table.prettify()