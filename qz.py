import sys 
import csv 
import numpy as np
import pandas as pd

if __name__ == '__main__':

	train = pd.read_csv(sys.argv[1])

	for index,row in train.iterrows():

		#add q to  query
		words = str(row['query']).split(" ")
		for i,word in enumerate(words):
			words[i] = 'q'+word
		train['query'][index] = " ".join(words)

		#add z to product_title
		words = str(row['product_title']).split(" ")
		for i,word in enumerate(words):
			words[i] = 'z'+word
		train['product_title'][index] = " ".join(words)

	train.to_csv(sys.argv[2],index = False, mode = 'w')