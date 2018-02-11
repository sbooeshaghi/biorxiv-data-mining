## ml-main.py, doing basic word2vec on abstracts

# first iterate through the folder with all of the files
import os
from gensim.models import word2vec
import json
#from pymongo import MongoClient
from nltk.corpus import stopwords
from string import ascii_lowercase
import string
import pandas as pd
import os
from cleanData import clean
#import gensim, os, re, pymongo, itertools, nltk, snowballstemmer



data_path = os.getcwd() + '/downloads/data'
data = pd.read_csv(data_path)

ab = clean(data, 'Abstract')
text = clean(data, 'Text')