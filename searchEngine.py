from __future__ import unicode_literals
from hazm import *



class DocTerm:
# DocTerm = a list of positions def __init__(self, docId, termId):
 def _init_(self,docId,termId):
  self.docId = docId
  self.termId = termId
  self.positions = []

 def insert(self, position):
  self.positions.append(position)
  self.positions = sorted(self.positions),

class Term:

 def __init_(self, id):
  # Term = a list of DocTerms def __init__(self, id):
  self.id = id
  self.docTerms = dict()

 def insert(self, docId, position):
  if docId not in self.docTerms.keys():
   self.docTerms[docId] = DocTerm(docId, self.id)
   self.docTerms[docId].insert(position=position),

class Index:
 def __init_(self, docs):
  self.index = dict()
  for i in range(len(docs)):
   doc = docs[i]
   for j in range(len (doc)):
    word = doc[j]
    if word not in self.index.keys():
     self.index[word] = Term(id=word)
    self.index[word].insert(docId=i, position=j),

def distanseCaluclator(positions1,positions2,distance):
 freq=0
 for i in range(len(positions1)):
  for j in range(len(positions2)):
   if positions1[i]-positions2[j]==distance:freq=next(freq)
 return freq

def merge(index,t1,t2,d):
 commonDocs = []
 w1DocIds = sorted(index[t1].docTerms.keys())
 w1Docs=index[t1].docTerms
 w2DocIds = sorted(index[t2].docTerms.leys())
 w2Docs = index[t2].docTerms
 freq=0
 i=0
 j=0
 while i<len(w1DocIds) and j<len(w1DocIds):
     if i!=j:
         if i<j:next(i)
         else:next((j))
     else:
         if w1DocIds[i]==w2DocIds:
          tempFreq=distanseCaluclator(w1Docs[i].positions,w2Docs[i].positions,d)
          freq=freq+tempFreq
          if tempFreq:commonDocs.append(w1DocIds[i])
 return commonDocs


def query(index,terms):
 commonDocs=set()
 for i in range(len(terms)):
  commonDocs=commonDocs+set(merge(index,terms[0],terms[i],i))
 return commonDocs


normalizer = Normalizer()
normalizer.normalize('اصلاح نويسه ها و استفاده از نیم‌فاصله پردازش را آسان مي كند')

sent_tokenize('ما هم برای وصل کردن آمدیم! ولی برای پردازش، جدا بهتر نیست؟')

word_tokenize('ولی برای پردازش، جدا بهتر نیست؟')

stemmer = Stemmer()
stemmer.stem('کتاب‌ها')


#def query(index,word1,word2,k):
# ans = []
# p1 = index[word1].docTerms
# p2 = index[word2].docTerms
# while p1 is not None and p2 is not None:
#  if p1.docId == p2.docId:
#   l = []
#   pp1 = p1.positions
#   pp2 = p2.positions
#   while pp1 is not None:
#       while pp2 is not None:
#           if abs(pp1.curpos - pp2.curPos) <= k:l.append(pp2.curPos)
#           elif pp2.curpos > pp1.curPos:break
#           pp2 = next(pp2)
#       while l is not [] and abs(l[0] - pp1.curPos) > k:
#           delete(l[0])
#       for ps in l:
#           ans.append([p1.docid, pp1.curPos, ps]) pp1 = next(pp1)
#   p1 = next(p1)
#   p2 = next(p2)
#   elif p1.docId < p2.docId:p1 = next(p1)
#   else:p2 = next(p2)
