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

filelist=[]
f = open('urls-fr.txt', 'r')
for i in f.readlines():
        columns = i.split(",")
	if columns[0]=="Yes" and columns[4].find("txt")<>-1 and columns[4].find("pdf")==-1:
		filelist.append(columns[4].rstrip('\n'))
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
f.to_csv('FR-all.csv',sep=';')


