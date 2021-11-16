from __future__ import unicode_literals
from hazm import *
import pandas as pd




class DocTerm:
# DocTerm = a list of positions def __init__(self, docId, termId):
 def __init__(self,docId,termId):
  self.docId = docId
  self.termId = termId
  self.positions = []

 def insert(self, position):
  self.positions.append(position)
  self.positions = sorted(self.positions)
  print()

class Term:

 def __init__(self, id):
  # Term = a list of DocTerms def __init__(self, id):
  self.id = id
  self.docTerms = dict()

 def insert(self, docId, position):
  if docId not in self.docTerms.keys():
   self.docTerms[docId] = DocTerm(docId, self.id)
   self.docTerms[docId].insert(position=position),

class Index:

 def __init__(self, docs):

  self.index = dict()
  stopWords=stopwords_list()

  for i in range(len(docs)):
   print()
   doc = preProcessor(docs[i])
   print()

   for j in range(len(doc)):
    word = doc[j]
    if word not in self.index.keys():self.index[word] = Term(id=word)
    self.index[word].insert(docId=i, position=j)

    print()


def correctWordDistanceChecker(positions1,positions2,distance):
 print()
 for i in range(len(positions1)):
  for j in range(len(positions2)):
   print()
   if positions2[j]-positions1[i]==distance:
       print()
       return True
 print()
 return False

def merge(index,t1,t2,d):
 commonDocs = []
 w1DocIds = sorted(index[t1].docTerms.keys())
 w1Docs=index[t1].docTerms
 w2DocIds = sorted(index[t2].docTerms.keys())
 w2Docs = index[t2].docTerms
 i=0
 j=0
 print()
 while i<len(w1DocIds) and j<len(w2DocIds):
     print()
     if w1DocIds[i]!=w2DocIds[j]:
         if w1DocIds[i]<w2DocIds[j]:
             i+=1
             print()
         else:
             j+=1
             print()
     else:
          checkResult=correctWordDistanceChecker(w1Docs[w1DocIds[i]].positions, w2Docs[w2DocIds[j]].positions, d)
          print()
          if checkResult:
           commonDocs.append(w1DocIds[i])
          i += 1
          j += 1

 print()
 return commonDocs


def textQuery(index,terms,mergeCache):
 commonDocs=set()

 if len(terms)==1:return list(index[terms[0]].docTerms.keys())

 for i in range(1,len(terms),1):

  if (terms[0],terms[i]) not in mergeCache.keys():
   mergeResult=set(merge(index,terms[0],terms[i],i))
   mergeCache[(terms[0],terms[i])]=mergeResult
   print()

  commonDocs=set.union(commonDocs,mergeCache[(terms[0],terms[i])])
  print()

 return commonDocs

def queryResults(index,query):
 queries=[]
 mergeCache=dict()
 terms=preProcessor(query)
 print()
 for i in range(len(terms),0,-1):
  j=0
  while j+i<=len(terms):
   termsTemp=terms[j:j+i]
   j+=1
   print()
   queries.append(textQuery(index,termsTemp,mergeCache))
  queries.append('*')
 return queries

def preProcessor(text):
 stemmer = Stemmer()
 normalizer = Normalizer()
 tokens = word_tokenize(text)
 stopWords=stopwords_list()
 finalTokens=[]

 for i in range(len(tokens)):
     if tokens[i] not in stopWords:
      stemTemp=stemmer.stem(tokens[i])
      normalTemp=normalizer.normalize(stemTemp)
      finalTokens.append(normalTemp)

 return finalTokens


docsDatabaseFileName="IR1_7k_news.xlsx"
test='قرآن و اصلاح نويسه ها و استفاده از نیم‌فاصله پردازش را آسان مي كند'
queryTest="مرزبان مربی سپاهان"
#test=preProcessor(test)
docs = pd.read_excel(docsDatabaseFileName)
docs=list(docs['content'])
print()
index=Index(docs).index
results=queryResults(index,queryTest)
print(results)
print()
