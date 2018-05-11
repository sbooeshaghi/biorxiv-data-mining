"""
Created on Sat Feb 10 2018

@author: alisina (Sina Booeshaghi)

main.py
---
This is the main file which calls scrape. TBH idk if it was necessary to even 
have this sort of file structure breakdown but whatevs. Note: df is the dataframe
that is returned from scrape which contains all of the info you could ever want.
"""

'''
List of dependencies:
pdfminer: 		pdf to text converter
timeit: 		timing the python program
selenium: 		to run the webdriver
beautifulSoup: 	to grab html from website
os: 			for getting pwd etc
sys: 			for error exiting
numpy:			dataframe manipulation
pandas: 		for constructing the dataframe
requests: 		to scrape DOI links quickly and easily
urllib2:		to download the pdfs
re: 			to do regex stuff
html5lib:		to run BS4


'''
# TODO: write a seprate script to parse through dataframe and convert pdf to txt
# using 
#text = convert(download_path + '/'+new_file_name)
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import os
import sys
#import textract
import numpy as np
import pandas as pd
import re
from lib.scrape import scrape

links = pd.read_csv('doi_links.csv')
links = links.values.ravel()
links = links.tolist()
data = scrape(links)