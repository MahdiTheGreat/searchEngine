from __future__ import unicode_literals
from hazm import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class UniversalSet(set):
    def __and__(self, other):
        return other

    def __rand__(self, other):
        return other

class DocTerm:

 def __init__(self,docId,termId):
  self.docId = docId
  self.termId = termId
  self.positions = []
  self.freq=0

 def insert(self, position):
  self.positions.append(position)
  self.positions = sorted(self.positions)
  self.freq+=1

  #print()

class Term:

 def __init__(self, id):

  self.id = id
  self.docTerms = dict()
  self.freq=0

 def insert(self, docId, position):
  self.freq+=1
  if docId not in self.docTerms.keys():
   self.docTerms[docId] = DocTerm(docId, self.id)
  self.docTerms[docId].insert(position=position)

 def __eq__(self, other):
     return self.freq==other.freq

 def __lt__(self, other):
     if self.freq<other.freq:return True
     else:return False

 def __gt__(self, other):
     if self.freq > other.freq:
         return True
     else:
         return False


class Index:

 def __init__(self):
  self.index = dict()
  self.termAxis=[]
  self.tokenCount=0
  self.termCount=0

 def indexInsert(self,term,docId,position):
     self.tokenCount += 1
     if term not in self.index.keys():
         self.index[term] = Term(id=term)
         self.termCount += 1
     self.index[term].insert(docId=docId, position=position)
     self.termAxis.append(self.termCount)
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

def preProcessor(text,haveStopWords=False,haveStemming=True):
 stemmer = Stemmer()
 normalizer = Normalizer()
 tokens = word_tokenize(text)
 stopWords=stopwords_list()
 finalTokens=[]

 for i in range(len(tokens)):
     if (tokens[i] not in stopWords) or haveStopWords:
      normalTemp = normalizer.normalize(tokens[i])
      if haveStemming:stemTemp=stemmer.stem(normalTemp)
      else:stemTemp=normalTemp
      finalTokens.append(stemTemp)

 return finalTokens

def tokenMerger(tokens):
    mergedToken=''

    for i in range(len(tokens)):
        mergedToken+=" "+tokens[i]

    return mergedToken

def indexer(index,docs,ids,haveStopWords=False,haveStemming=True):

    for i in range(len(docs)):
        doc = preProcessor(docs[i],haveStopWords=haveStopWords,haveStemming=haveStemming)
        #print()
        for j in range(len(doc)):
            term = doc[j]
            index.indexInsert(term,ids[i],j)

    print("done")

def getOrderedFreqsOfTerms(Index):
    freqs=[]
    rankedTerms = sorted(Index.index.values())
    print()
    for i in range(len(rankedTerms)):
        freqs.append(rankedTerms[i].freq)
    return freqs

def idMaker(urls):
    ids=[]
    for i in range(len(urls)):
        ids.append(int(urls[i].split("/")[4]))
    return ids

def idTransDictMaker(ids):
    idTransDict=dict()
    for i in range(len(ids)):
        idTransDict[ids[i]]=i
    return idTransDict




docsDatabaseFileName="IR1_7k_news.xlsx"
maxSize=8000
query="دانشگاه صنعتی امیرکبیر"

#tokens=word_tokenize(query)
#normalizer=Normalizer()
#stemmer=Stemmer()
#print()
#for i in range(len(tokens)):
#    tokens[i]=normalizer.normalize(tokens[i])
#print()
#for i in range(len(tokens)):
#    tokens[i]=stemmer.stem(tokens[i])
#print()


dataSize=maxSize
haveStopWords=False
haveStemming=True

table = pd.read_excel(docsDatabaseFileName,)
docs=list(table['content'][0:dataSize])
titles=list(table['title'][0:dataSize])
urls=list(table['url'][0:dataSize])
ids=idMaker(urls)
idTransDict=idTransDictMaker(ids)
print()
fileIndex = Index()

indexer(fileIndex,docs,ids,haveStopWords=haveStopWords,haveStemming=haveStemming)
print()

results = queryResults(fileIndex.index, query)

for i in range(len(results)):
    for j in range(len(results[i])):
        if j==0:
         print("پرسمان هست:")
         print(results[i][j])
         print("تعداد اسناد بازیابی شده برابر است با:")
         print(len(results[i][1]))
        else:
         for k in range(len(results[i][j])):
             print("شناسه سند:")
             print(results[i][j][k])
             print("تیتر:")
             print(titles[idTransDict[results[i][j][k]]])
         print("---------------------------------------------------------------------------------")



orderedFreqs=np.asarray(getOrderedFreqsOfTerms(fileIndex)[::-1])
logOrderedFreqs=np.log10(orderedFreqs)
ranks=np.arange(1,len(orderedFreqs)+1)
logRanks=np.log10(ranks)

#A = np.vstack([logRanks, np.ones(len(logRanks))]).T
#m, c = np.linalg.lstsq(A, logOrderedFreqs, rcond=None)[0]
#k=pow(c,10)
k=np.average(np.multiply(orderedFreqs,ranks))

zipsLaw=(1/ranks)*k
logZipsLaw=np.log10(zipsLaw)

plt.plot(logRanks,logOrderedFreqs,label="(log r,log cf)")
plt.plot(logRanks,logZipsLaw,label="(log r,log(k/r))")
plt.legend()
plt.show()

plt.plot(ranks,orderedFreqs,label="(r,cf)")
plt.plot(ranks,zipsLaw,label="(r,k/r)")
plt.legend()
plt.show()

#print("slope or b in zipfs law is")
#print(m)
print("k in zipfs law is")
print(k)

tokenAxis = np.arange(1, fileIndex.tokenCount+1)
tokenAxisLog=np.log10(tokenAxis)
termAxis = np.asarray(fileIndex.termAxis)
termAxisLog=np.log10(termAxis)

A = np.vstack([tokenAxisLog, np.ones(len(tokenAxisLog))]).T
m, c = np.linalg.lstsq(A, termAxisLog, rcond=None)[0]
k=pow(10,c)

heapsLaw=k*np.power(tokenAxis,m)
logHeapsLaw=np.log10(heapsLaw)

plt.plot(tokenAxisLog,termAxisLog,label="(log T,Log M",)
plt.plot(tokenAxisLog,logHeapsLaw,label="(log T,Log(kT^b))",)
plt.legend()
plt.show()

plt.plot(tokenAxis,termAxis,label="(tokens,terms)")
plt.plot(tokenAxis,heapsLaw,label="heaps law")
plt.legend()
plt.show()

print("slope or b in heaps law is")
print(m)
print("k in heaps law is")
print(k)

print("avg error between heaps law approximation and actual dictionary size is")
print(np.average(np.abs(termAxis-heapsLaw)))
print(" the final approximation of the heaps law is")
print(heapsLaw[len(heapsLaw)-1])
print("but the final size of the dictionary is")
print(termAxis[len(termAxis)-1])







