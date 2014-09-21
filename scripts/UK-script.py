#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import urllib
from urllib2 import urlopen, URLError, HTTPError
import codecs
import sys
import collections
import string
from string import maketrans,find
import os

#create output dir
if not os.path.exists('output'):
	    os.makedirs('output')
if not os.path.exists('output/files'):
	    os.makedirs('output/files')

#url de base des fichiers GitHub
url_base='https://github.com/openfoodfacts/eu-food-data/raw/master/uk/'

#get datafile list
def get_datafile(url):
	df=pd.read_csv(url, sep=';',header=0)
	return df

#get method list
def get_methodfile(url):
	df = pd.read_csv(url, sep=';',header=0,index_col=0)
	return df

#download file function
def dlfile(url):
    # Open the url
    try:
	f = urlopen(url)
        print "downloading " + url

        # Open our local file for writing
        with open('output/files/'+os.path.basename(url), "wb") as local_file:
            local_file.write(f.read())

    #handle errors
    except HTTPError, e:
        print "HTTP Error:", e.code, url
    except URLError, e:
        print "URL Error:", e.reason, url


#user input
#country_list=['UK']
#input_OK=False

#while input_OK==False:
#	prompt='Country to update (available countries are '+','.join(country_list)+'): '
#	country = raw_input(prompt)
#	if country in country_list:
#		print 'Processing '+country
#		input_OK=True
#	else:
#		print 'Please enter an available country'

#main
data_file=get_datafile('UK-urls.txt')
method_file=get_methodfile('UK-methods.txt')

all=[]
for m in data_file.iterrows():
	#if m[1]['country'] ==country:	

		url=url_base+m[1]['file']
		method=m[1]['Method']
		columns=int(method_file.loc[method,'nbcols'])
		start_row=int(method_file.loc[method,'start_row'])-1

		dlfile(url)
		df = pd.read_excel('output/files/'+m[1]['file'],sheetname=0,header=None,parse_cols=columns)
		df=df.ix[start_row:]
		df.columns=method_file.loc[method,'colnames'].split(",")
		df = df.dropna(subset=['Name'])
		df['SECTION']=m[1]['file']
		if 'Region' in list(df.columns.values):		
			df.drop('Region', axis=1, inplace=True) #drop existing Region column for UK approved fishermen
		df['REGION']=m[1]['region']
		df['COUNTRY']=m[1]['country']
		all.append(df)

#merge file
df=pd.concat(all)
df.reset_index
df.to_csv('output/merge.csv',sep=';', encoding='utf-8')
