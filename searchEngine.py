from __future__ import unicode_literals
from hazm import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import threading
import multiprocessing

class UniversalSet(set):
    def __and__(self, other):
        return other

    def __rand__(self, other):
        return other

class DocTerm:
# DocTerm = a list of positions def __init__(self, docId, termId):
 def __init__(self,docId,termId):
  self.docId = docId
  self.termId = termId
  self.positions = []

 def insert(self, position):
  self.positions.append(position)
  self.positions = sorted(self.positions)
  #print()

class Term:

 def __init__(self, id):
  # Term = a list of DocTerms def __init__(self, id):
  self.id = id
  self.docTerms = dict()
  self.freq=0

 def insert(self, docId, position):
  self.freq+=1
  if docId not in self.docTerms.keys():
   self.docTerms[docId] = DocTerm(docId, self.id)
  self.docTerms[docId].insert(position=position)

class Index:

 def __init__(self):

  self.index = dict()
  self.termAxis=[]
  self.tokenCount=0
  self.lock = threading.Lock()
  self.termCount=0

 def indexInsert(self,term,docId,position):
     #print()
     self.lock.acquire()
     try:
         self.tokenCount += 1
         if term not in self.index.keys():
             self.index[term] = Term(id=term)
             self.termCount += 1
         self.index[term].insert(docId=docId, position=position)
         self.termAxis.append(self.termCount)
         #print()
     finally:
         self.lock.release()
         #print()

def correctWordDistanceChecker(positions1,positions2,distance):
 correctDistancsefreq=0
 #print()
 for i in range(len(positions1)):
  for j in range(len(positions2)):
   #print()
   if positions2[j]-positions1[i]==distance:
       #print()
       correctDistancsefreq+=1
 #print()
 return correctDistancsefreq

def merge(index,t1,t2,d):
 commonDocs = []
 w1DocIds = sorted(index[t1].docTerms.keys())
 w1Docs=index[t1].docTerms
 w2DocIds = sorted(index[t2].docTerms.keys())
 w2Docs = index[t2].docTerms
 i=0
 j=0
 #print()
 while i<len(w1DocIds) and j<len(w2DocIds):
     #print()
     if w1DocIds[i]!=w2DocIds[j]:
         if w1DocIds[i]<w2DocIds[j]:
             i+=1
             #print()
         else:
             j+=1
             #print()
     else:
          positions1=w1Docs[w1DocIds[i]].positions
          positions2=w2Docs[w2DocIds[j]].positions
          #print()
          checkResult=correctWordDistanceChecker(positions1,positions2,d)
          #print()
          if checkResult:
           commonDocs.append(w1DocIds[i])
          i += 1
          j += 1

 #print()
 return commonDocs

def textQuery(index,terms,mergeCache):
 commonDocs=UniversalSet(set())
 if len(terms)==1:return list(index[terms[0]].docTerms.keys())

 for i in range(len(terms)):
     for j in range(i+1,len(terms)):
      if (terms[i],terms[j]) not in mergeCache.keys():
           mergeResult=set(merge(index,terms[i],terms[j],j-i))
           mergeCache[(terms[i],terms[j])]=mergeResult
           #print()
      #print()
      commonDocs = commonDocs & mergeCache[(terms[i], terms[j])]


 #print()

 return list(commonDocs)

def queryResults(index,query):
 queries=[]
 mergeCache=dict()
 queryTokens=word_tokenize(query)
 terms=preProcessor(query)
 #print()

 for i in range(len(terms),0,-1):
  j=0
  while j+i<=len(terms):
   termsTemp=terms[j:j+i]
   queries.append([tokenMerger(queryTokens[j:j+i]),sorted(textQuery(index,termsTemp,mergeCache))])
   j += 1
   #print()

 return queries

def preProcessor(text,haveStopWords=False):
 stemmer = Stemmer()
 normalizer = Normalizer()
 tokens = word_tokenize(text)
 stopWords=stopwords_list()
 finalTokens=[]

 for i in range(len(tokens)):
     if (tokens[i] not in stopWords) or haveStopWords:
      normalTemp = normalizer.normalize(tokens[i])
      stemTemp=stemmer.stem(normalTemp)
      #print()
      if (stemTemp not in stopWords) or haveStopWords:finalTokens.append(stemTemp)

 return finalTokens

def tokenMerger(tokens):
    mergedToken=''

    for i in range(len(tokens)):
        mergedToken+=" "+tokens[i]

    return mergedToken

def indexer(index,docs,haveStopWords=False):
    for i in range(len(docs)):
        doc = preProcessor(docs[i],haveStopWords)
        #print()

        for j in range(len(doc)):
            term = doc[j]
            index.indexInsert(term,i,j)

    print("done")

if __name__ == '__main__':

 #processorTest='قرآن و اصلاح نويسه ها و استفاده از نیم‌فاصله پردازش را آسان مي كند'
 ##processorTest='ما هم برای وصل کردن آمدیم! ولی برای پردازش، جدا بهتر نیست؟'
 #normalizer=Normalizer()
 #stemmer=Stemmer()
 #lemmatizer=Lemmatizer()
 #tokenTest=word_tokenize(processorTest)
 #normalTest=normalizer.normalize(tokenTest[0])
 #stemTest=stemmer.stem(tokenTest[0])
 #lemtest=lemmatizer.lemmatize(tokenTest[0])
 ##sentTokenTest=sent_tokenize(processorTest)
 ##processorTestResult=preProcessor(processorTest)
 ##print()

 docsDatabaseFileName="IR1_7k_news.xlsx"
 queryTest="مرزبان مربی سپاهان"
 dataSize=100
 cpuNumber=multiprocessing.cpu_count()
 multiThreaded=True
 haveStopWords=False

 table = pd.read_excel(docsDatabaseFileName)
 docs=list(table['content'][0:dataSize])
 titles=list(table['title'])
 stepSize=int(dataSize/cpuNumber)

 fileIndex = Index()

 steps=0
 threads=[]
 if multiThreaded:

  for steps in range(cpuNumber):
      t = threading.Thread(target=indexer, args=(fileIndex,docs[steps*stepSize:(steps+1)*stepSize],haveStopWords))
      threads.append(t)
      t.start()
  if steps*stepSize!=len(docs):
      t = threading.Thread(target=indexer, args=(fileIndex, docs[steps * stepSize:len(docs)],haveStopWords))
      threads.append(t)
      t.start()

  for i in range(len(threads)):
      threads[i].join()


 else:indexer(fileIndex,docs,haveStopWords)

 tokenAxis = np.arange(0, fileIndex.tokenCount)
 tokenAxisLog = np.log(tokenAxis)
 termAxis = np.asarray(fileIndex.termAxis)
 termAxisLog = np.log(termAxis)
 results = queryResults(fileIndex.index, queryTest)
 #print()

 for i in range(len(results)):
     for j in range(len(results[i])):
         if j==0:
          print("the query is")
          print(results[i][j])
          print("the amount of returend docs are")
          print(len(results[i][1]))
         else:
          for k in range(len(results[i][j])):
              print("doc id is")
              print(results[i][j][k])
              print("title is")
              print(titles[results[i][j][k]])
          print("---------------------------------------------------------------------------------")

 #print()
 plt.plot(tokenAxis,termAxis,label="normal rep")
 plt.show()
 plt.plot(tokenAxisLog,termAxisLog,label="log rep")
 plt.show()