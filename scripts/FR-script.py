#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import urllib
import codecs
import sys
import collections
import string
from string import maketrans,find

accents = u"éèçêàôûùîâ°".encode('latin1')
ascii = "eeceaouuiaO"
conversion = maketrans(accents, ascii)

urllib.urlretrieve("https://raw.githubusercontent.com/openfoodfacts/eu-food-data/master/fr/urls-fr.txt", "urls-fr.txt")

filelist=[]
f = open('urls-fr.txt', 'r')
for i in f.readlines():
	if i.find("txt")<>-1 and i.find("pdf")==-1:
		filelist.append(i.rstrip('\n'))
f.close()

# pass in column names for each CSV
all=[]  
for f in filelist:
	print f
	df = pd.read_csv(f, sep=';')
	df.rename(columns=lambda x:x.translate(conversion).upper(),inplace=True)
	df.rename(columns={u'NO /AGREMENT':u'NUMERO AGREMENT/APPROVAL NUMBER'}, inplace=True)
	df.rename(columns={u'NO DE/DEPARTEMENT':u'NUMERO DE DEPARTEMENT'}, inplace=True)
	df['SECTION']=f
	all.append(df)

#merge file
f=pd.concat(all)
f.to_csv('merge.csv',sep=';')
