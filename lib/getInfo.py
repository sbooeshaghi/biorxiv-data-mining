from collections import OrderedDict
from collections import Counter
import re


def getInfo(soup, doJ):
## Find out where it as published (if any) jrnl may be empty
	try:
		check_if_real = soup.find('h2').getText()
	except:
		jrnl = 'DOI Not Found'
		authors = ['DOI Not Found']
		date_posted = 'DOI Not Found'
		abstract = 'DOI Not Found'
		title = 'DOI Not Found'
		rt = ['DOI Not Found']
		real_link = ['DOI Not Found']
		category = ['DOI Not Found']
		if jrnl in doJ:
			doJ[jrnl] += 1
		else:
			doJ[jrnl] = 1

		return (jrnl, authors, date_posted, abstract, title, rt, real_link, category, doJ)

	if check_if_real == 'DOI Not Found':
		jrnl = 'DOI Not Found'
		authors = ['DOI Not Found']
		date_posted = 'DOI Not Found'
		abstract = 'DOI Not Found'
		title = 'DOI Not Found'
		rt = ['DOI Not Found']
		real_link = ['DOI Not Found']
		category = ['DOI Not Found']
		if jrnl in doJ:
			doJ[jrnl] += 1
		else:
			doJ[jrnl] = 1

		return (jrnl, authors, date_posted, abstract, title, rt, real_link, category, doJ)

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

	try:
		## Find HTML with first and sur names
		fnames = soup.find_all('span', {'class':'nlm-given-names'})
		snames = soup.find_all('span', {'class':'nlm-surname'})
		
		## Get the names in an array of strings
		fnames = [fir.getText().encode('utf-8') for fir in fnames]
		snames = [sur.getText().encode('utf-8') for sur in snames]

		## Remove duplicates, now element snames(i), fnames(i) is Surname, Firstname
		fnames = list(OrderedDict.fromkeys(fnames))
		snames = list(OrderedDict.fromkeys(snames))

		## Put the authors names into a dict
		aff = soup.find_all('span', {'class':'nlm-aff'})
		aff = [i.getText().encode('utf-8') for i in aff]
		aff = [re.sub(r'[\t\n;]', '', i) for i in aff]

		authors = list(zip(snames, fnames, aff))
		# these are unicode strings, need to use ""
	except AttributeError:
		authors = [('None', 'None', 'None')]
	try:
		## Find out when the article was posted to the Arxiv
		date_posted = soup.find('li', {'class':'published'}).getText()
		date_posted = date_posted[7:-1].encode('utf-8')
	except AttributeError:
		date_posted = 'None'
	try:
		## Get the abstract text
		abstract = soup.find('p', {'id' : 'p-2'}).getText().encode('utf-8')
	except AttributeError:
		abstract = 'None'

	try:
		## Get the title of the paper
		title = soup.find('h1', {'id' : 'page-title'}).getText().encode('utf-8')
	except AttributeError:
		title = 'None'

	if jrnl != 'Pre print':
		try:
			real_link = soup.find('a' ,{'style':'color:#BC2635;'})['href'].encode('utf-8')
		except:
			real_link = 'None'
	else:
		real_link = 'None'
	try:
		date_rt = soup.find_all('time')
		date_rt = [date.getText() for date in date_rt]
		count_dates = Counter(date_rt)
		dates_to_add = [i.encode('utf-8') for i in count_dates.keys()]
		rt = zip(dates_to_add, count_dates.values())
	except AttributeError:
		rt = [('None', 'None')]
	#import ipdb; ipdb.set_trace()
	try:
		categories = soup.find_all('span', {'class':'highwire-article-collection-term'})
		category = []
		for line in categories:
			t = line.getText()
			cat = t.split('\n')[0]
			category.append(cat)
		#category = category.split('\n')[0]
	except AttributeError:
		category = 'None'

	return (jrnl, authors, date_posted, abstract, title, rt, real_link, category, doJ)