import sys 
import re
import csv 
import numpy as np
import pandas as pd
from nltk.corpus import wordnet
from nltk.corpus import words
from nltk.corpus import stopwords

"""
id	query	product_title	product_description	 median_relevance	relevance_variance

"""

"""
bag1 = row['query'].split(" ")
bag2 = row['product_title'].split(" - ")

"""
if __name__ == '__main__':
	train = pd.read_csv('data/train.csv')

	stopward_exception_query = {'an extremely goofy movie':'an','wreck it ralph':'it','thomas the train':'the','button down shirt':'down','dr who lanyard':'who'}

	# find all 261 query 
	all_query = set()
	for index,row in train.iterrows():
		all_query.add(row['query'])

	#convert to lower case
	all_query1 = []
	for query in all_query:
		all_query1.append(query.lower())		
	
	#split in words
	all_query2 = []
	for query in all_query1:
		all_query2.append(query.split())

	#remove stopwards
	for i,query in enumerate(all_query2):
		if " ".join(query) not in stopward_exception_query.keys():
			for word in query:
				if word in stopwords.words('english'):
					all_query2[i].remove(word)

	
