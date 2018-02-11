## ml-main.py, 

import os
from gensim.models import word2vec
import json
from nltk.corpus import stopwords
from string import ascii_lowercase
import string
import pandas as pd
import os
from cleanData import clean
from sklearn.feature_extraction.text import TfidfVectorizer


data_path = os.getcwd() + '/downloads/data'
data = pd.read_csv(data_path)

col_to_clean = ['Abstract', 'Text']
clean_data = clean(data, col_to_clean)

abstracts = clean_data['Abstract']
text = clean_data['Text']

# Basic word vector comparison of the Abstracts
tfidf1 = TfidfVectorizer().fit_transform(abstracts)
pairwise_sim1 = pd.DataFrame((tfidf1*tfidf1.T).A)

# Basic word vector comparison of the Texts
tfidf2 = TfidfVectorizer().fit_transform(text)
pairwise_sim2 = pd.DataFrame((tfidf2*tfidf2.T).A)
#return clean_data

#if __name__ == '__mlMain__':
#	mlMain()