#!/usr/bin/env python
# python 2.7

'''
USAGE:
DESCRIPTION: This script will find common phrases in a text document

'''

# ~~~~ LOAD PACKAGES ~~~~ #
import sys
import os
import re
import string
from collections import defaultdict
# import argparse

# ~~~~ FUNCTIONS ~~~~ #
def groom_line(line):
    # remove weird dashes
    line = line.replace("_", " ")
    line = line.replace("--", " ")
    # remove misc punctuation marks
    line = ' '.join(word.strip(string.punctuation) for word in line.split())
    # remove excess whitespace
    line = re.sub('\s+', ' ', line).strip()
    return(line)

def doc_dict(text_file, chunk_size):
    phrase_dict = defaultdict(int)
    phrase_list = []
    # read in the text
    with open(text_file, 'r') as myfile:
        data=myfile.read()

    # split on sentences
    sentences_list = split_sentences(data)

    # process the entire document
    for sentence in sentences_list:
        sentence = groom_line(sentence)
        sentence_phrases = chunk_comninator(sentence, chunk_size, ' ')
        if len(sentence_phrases) > 0:
            for phrase in sentence_phrases:
                phrase_dict[phrase] += 1
    return phrase_dict

def split_words(sentence):
    # split line into words
    words = groom_line(sentence).split()
    return(words)

def split_sentences(line):
    sentences = line.split('.')
    return sentences

def remove_caps(string):
    string = string.split()
    string[0] = string[0].lower()
    string = ' '.join(word for word in string)
    return string

def make_chunk_list(line, chunk_size, split_char):
    index = 0
    breakpoint = 0
    chunk_list = []
    for m in re.finditer(split_char, line):
        if len(line[breakpoint:].split(split_char)) < chunk_size:
            chunk = remove_caps(line[breakpoint:].strip())
            chunk_list.append(chunk)
            break
        if index < chunk_size:
            index += 1
            continue
        else:
            chunk = remove_caps(line[breakpoint:m.end()].strip())
            chunk_list.append(chunk)
            index = 0
            breakpoint = m.end()
    return chunk_list

def chunk_comninator(line, chunk_size, split_char):
    remainder = len(line.split(split_char)) % chunk_size
    remainder_count = 0
    chunk_list = []
    if int(remainder) != 0:
        tmp_line = line
        while remainder_count < remainder:
            for chunk in make_chunk_list(tmp_line, chunk_size, split_char):
                chunk_list.append(chunk)
            tmp_line = tmp_line.split(split_char)
            tmp_line.pop(0)
            tmp_line = split_char.join(tmp_line)
            remainder_count += 1
    else:
        for chunk in make_chunk_list(line, chunk_size, split_char):
            chunk_list.append(chunk)
    return chunk_list

def sort_dict(doc_dict):
    sorted(doc_dict.items(), key=lambda x: x[1])



def my_debugger():
    # DEBUGGING !!
    # call with my_debugger() anywhere in your script
    import readline # optional, will allow Up/Down/History in the console
    import code
    vars = globals().copy()
    vars.update(locals())
    shell = code.InteractiveConsole(vars)
    shell.interact()

# ~~~~ DO A THING ~~~~ #
text_file="txt/Dracula-Bram_Stoker.txt"

line1 = "So much so that all the rest seemed to take courage as if infected somewhat with her gaiety as a result even I myself felt as if the pall of gloom which weighs us down were somewhat lifted"

line2 = "All day long we seemed to dawdle through a country which was full of beauty of every kind. Sometimes we saw little towns or castles on the top of steep hills such as we see in old missals; sometimes we ran by rivers and streams which seemed from the wide stony margin on each side of them to be subject to great floods. It takes a lot of water, and running strong, to sweep the outside edge of a river clear. At every station there were groups of people, sometimes crowds, and in all sorts of attire."


# my_debugger()
text_dict = doc_dict(text_file, 5)
bad_keys = []
for key, value in text_dict.iteritems():
    if int(value) < 2:
        bad_keys.append(key)
for key in bad_keys:
    del text_dict[key]

for key, value in sorted(text_dict.items(), key=lambda x: x[1], reverse=True):
    print value, '\t', key
