#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd 
import glob 
import os 
import gzip
import shutil

def unZipFile(fin, fout):
    with gzip.open(fin, 'rb') as f_in:
        with open(fout, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
            
def mergeAllCsv(path, files, merge):
    files = os.path.join(path, files) 
    files = glob.glob(files) 
    journal_edges = pd.concat([pd.read_csv(f) for f in files ]) 
    journal_edges.to_csv(merge, index=False, encoding='utf-8-sig')
    
def mergeTwoCsv(finA, finB, fout):
    first = pd.read_csv(finA)
    second = pd.read_csv(finB)
    merged = pd.DataFrame.merge(first, second, how='outer')
    merged.to_csv(fout, index=False)

def dropColumn(fin, fout, fieldName):
    data = pd.read_csv(fin)
    filteredData = data.drop(fieldName, inplace=True, axis=1)
    filteredData.to_csv(fout, index=False)
    




