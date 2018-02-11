## cleans a column of strings given pandas object
from nltk.corpus import stopwords
from string import ascii_lowercase
import string
import re

def clean(clean_data, col_to_clean):
    for column in col_to_clean:
        # column you are working on
        col = clean_data[column]

        stopword_set = set(stopwords.words("english"))

        # convert to lower case
        col = col.str.lower()
        
        # remove punctuation ## TODO: remove numebers
        regex_pat = re.compile(r'[^a-zA-Z\s]', flags=re.IGNORECASE)
        col = col.str.replace(regex_pat, " ")
        
        # now split it up into words
        col = col.str.split()

        # and remove stopwords
        col = col.apply(lambda x: [item for item in x if item not in stopword_set])

        # join the cleaned words back into single string
        col = col.str.join(" ")
        clean_data[column] = col
    
    return clean_data

if __name__ == '__main__':
    clean()