from collections import OrderedDict
from collections import Counter
import re

def getInfo(soup, doJ):
## Find out where it as published (if any) jrnl may be empty
	check_if_real = soup.find('h2').getText()

	if check_if_real == 'DOI Not Found':
		jrnl = 'DOI Not Found'
		authors = ['DOI Not Found']
		date_posted = 'DOI Not Found'
		abstract = 'DOI Not Found'
		title = 'DOI Not Found'
		rt = ['DOI Not Found']
		if jrnl in doJ:
			doJ[jrnl] += 1
		else:
			doJ[jrnl] = 1

		return jrnl, authors, date_posted, abstract, title, rt, doJ

	jrnl = soup.find_all('i')



	## Figure out how to label the jrnl name (this was hard for some reason)
	if jrnl:
		jrnl = jrnl[-1].text
		if not jrnl:
			jrnl = 'Pre print'
	elif not jrnl:
		jrnl = 'Pre print'

	if '/' in jrnl:
		jrnl =  re.sub(r'[^\w ]', '-', jrnl)

	## Note that the jrnl you just downloaded needs to be incremented
	if jrnl in doJ:
		doJ[jrnl] += 1
	else:
		doJ[jrnl] = 1

	check_if_real = soup.find('h2')

	if check_if_real == 'DOI Not Found':
		jrnl = 'DOI Not Found'
		authors = ['DOI Not Found']
		date_posted = 'DOI Not Found'
		abstract = 'DOI Not Found'
		title = 'DOI Not Found'
		rt = 'DOI Not Found'
		return jrnl, authors, date_posted, abstract, title, rt, doJ
	try:
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
		aff = soup.find_all('span', {'class':'nlm-aff'})
		aff = [i.getText() for i in aff]
		aff = [re.sub(r'[\t\n;]', '', i) for i in aff]

		authors = list(zip(snames, fnames, aff))
	except AttrubuteError:
		authors = [(None, None, None)]
	try:
		## Find out when the article was posted to the Arxiv
		date_posted = soup.find('li', {'class':'published'}).getText()
		date_posted = date_posted[7:-1]
	except AttrubuteError:
		date_posted = 'None'
	try:
		## Get the abstract text
		abstract = soup.find('p', {'id' : 'p-2'}).getText()
	except AttrubuteError:
		abstract = 'None'

	try:
		## Get the title of the paper
		title = soup.find('h1', {'id' : 'page-title'}).getText()
	except AttrubuteError:
		title = 'None'

	try:
		date_rt = soup.find_all('time')
		date_rt = [date.getText() for date in date_rt]
		count_dates = Counter(date_rt)
		rt = zip(count_dates.keys(), count_dates.values())
	except AttrubuteError:
		rt = [(None, None)]

	return jrnl, authors, date_posted, abstract, title, rt, doJ