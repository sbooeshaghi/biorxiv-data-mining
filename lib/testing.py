from selenium import webdriver
from bs4 import BeautifulSoup
import time
import os
import sys
#import textract
import numpy as np
import pandas as pd
import re

links = pd.read_csv('doiLinks.csv')
links = links.values.ravel()
links = links.tolist()
#link = 'https://www.biorxiv.org/content/early/2015/11/14/031591'
link = ['https://doi.org/10.1101/066480', 'https://doi.org/10.1101/192047']
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(chrome_options=options)
download_path = os.getcwd() + '/downloads'
doJ = {} 
driver.get(link)
innerHTML = driver.execute_script('return document.body.innerHTML')
soup = BeautifulSoup(innerHTML, 'html5lib')
jrnl, authors, date_posted, abstract, title, twitter, doJ = getInfo(soup, doJ)