import sys 
import re
import csv 
import numpy as np
import pandas as pd
if __name__ == '__main__':
	train = pd.read_csv('data/train.csv')
	test = pd.read_csv('data/test.csv')
	op = test['product_title'].unique()
	op1 = train['product_title'].unique()
	common = []
	for i in op :
		for j in op1 :
			if  i == j :
				common.append(j)
	print len(common)
	"""
	op2 = np.concatenate([op,op1])
	print len(op2)
	print len(op) , len(op1)
	"""
	

