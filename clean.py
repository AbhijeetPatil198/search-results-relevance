from bs4 import BeautifulSoup 
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import sys 
import re
import csv 
import numpy as np
import pandas as pd

"""
id	query	product_title	product_description	 median_relevance	relevance_variance

"""

rules = [  r'(playstation)([0-9])',r'([0-9]+)([mgt]b)',r'(iphone)([0-9])',r'(xbox)([0-9])' ]

def repl(m):
	return m.group(1) + " " + m.group(2)

def hasNumbers(inputString):
	return bool(re.search(r'\d', inputString))

stopward_exception_query = {'an extremely goofy movie':'an','wreck it ralph':'it','thomas the train':'the','button down shirt':'down','dr who lanyard':'who'}
	
if __name__ == '__main__':

	train = pd.read_csv('data/train.csv')

	#clean urls
	for index,row in train.iterrows():
		train['product_description'][index] = re.sub(r'https?:\/\/.*[\r\n]*', '', str(row['product_description']), flags=re.MULTILINE)

	#html
	for index,row in train.iterrows():
		train['query'][index] =  BeautifulSoup(str(row['query'])).get_text(" ")  
		train['product_title'][index] =  BeautifulSoup(str(row['product_title'])).get_text(" ")
		train['product_description'][index] =  BeautifulSoup(str(row['product_description'])).get_text(" ")

	#punctuation marks
	for index,row in train.iterrows():
		train['query'][index] = re.sub("[^a-zA-Z0-9]"," ",row['query'].encode('utf-8'))
		train['product_title'][index] = re.sub("[^a-zA-Z0-9]"," ",row['product_title'].encode('utf-8'))
		train['product_description'][index] = re.sub("[^a-zA-Z0-9]"," ",row['product_description'].encode('utf-8'))

	#lower case
	for index,row in train.iterrows():
		train['query'][index] = row['query'].encode('utf-8').lower()
		train['product_title'][index] = row['product_title'].encode('utf-8').lower()
		train['product_description'][index] = row['product_description'].encode('utf-8').lower()

	#lemmatize
	lmtzr = WordNetLemmatizer()
	for index,row in train.iterrows():

		#lemmatize query
		words = row['query'].encode('utf-8').split(" ")
		for i,word in enumerate(words):
			words[i] = lmtzr.lemmatize(word)
		train['query'][index] = " ".join(words)

		#lemmatize product_title
		words = row['product_title'].encode('utf-8').split(" ")
		for i,word in enumerate(words):
			words[i] = lmtzr.lemmatize(word)
		train['product_title'][index] = " ".join(words)

		#lemmatize product_description
		words = row['product_description'].encode('utf-8').split(" ")
		for i,word in enumerate(words):
			words[i] = lmtzr.lemmatize(word)
		train['product_description'][index] = " ".join(words)

	#remove extra whitespaces
	for index,row in train.iterrows():
		train['query'][index] = ' '.join( row['query'].encode('utf-8').split() )
		train['product_title'][index] = ' '.join( row['product_title'].encode('utf-8').split() )
		train['product_description'][index] = ' '.join( row['product_description'].encode('utf-8').split() )

	#remove stopwards
	stops = set(stopwords.words("english"))
	for index,row in train.iterrows():
		if row['query'] in stopward_exception_query.keys():

			new_stops = stops - set(stopward_exception_query[row['query']])

			#title
			words = row['product_title'].encode('utf-8').split(' ')
			words[:] = [x for x in words if bool(x not in new_stops)]
			train['product_title'][index] = ' '.join(words)

			#description
			words = row['product_description'].encode('utf-8').split(' ')
			words[:] = [x for x in words if bool(x not in new_stops)]
			train['product_description'][index] = ' '.join(words)

			#query
			words = row['query'].encode('utf-8').split(' ')
			words[:] = [x for x in words if bool(x not in new_stops)]
			train['query'][index] = ' '.join(words)

		else:

			#title
			words = row['product_title'].encode('utf-8').split(' ')
			words[:] = [x for x in words if bool(x not in stops)]
			train['product_title'][index] = ' '.join(words)

			#description
			words = row['product_description'].encode('utf-8').split(' ')
			words[:] = [x for x in words if bool(x not in stops)]
			train['product_description'][index] = ' '.join(words)

			#query
			words = row['query'].encode('utf-8').split(' ')
			words[:] = [x for x in words if bool(x not in stops)]
			train['query'][index] = ' '.join(words)


	train.to_csv('data/new_train.csv',index = False, mode = 'w',encoding='utf-8')