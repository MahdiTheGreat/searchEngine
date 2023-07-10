# searchEngine
The purpose of this project is to create a search engine for retrieving text documents in such a way that the user asks his question or query and the system returns the relevant documents. we want to create a simple information retrieval model and to do that, it is necessary to index the documents and at the time of receiving the request, the inverted index should be used to retrieve related documents. In short, we do the following steps:
	Document preprocessing
	Creating an inverted index
	Answering the user's query

# Document preprocessing
Before creating an inverted index, it is necessary to preprocess the texts. The necessary steps in this section are as follows:
	Token extraction
	Text normalization
	Removing repeat words
	finding roots of tokens or rooting
we do the above steps via hazm library.
At the beginning, we extract the tokens from the user's query, in a way that each separate word is converted to a token. After that, the Tokens are checked and if they are among the list of stop words, they are removed. The reason for this is to avoid wasting computer resources and memory. Next, the tokens are normalized e.g. several forms of one word are converted into one form. Finally, we obtain the root of the tokens to reduce memory usage and store the cleaned tokens as terms in the dictionary.
# Creating an inverted index
We build the inverted index using the preprocessed documents in the previous step. In the created inverted index, in addition to the position of the words in the documents, for each word from the dictionary, the number of repetitions of that word in total documents must be specified as also how many times a specific word is repeated in each document. Full details of this part can be seen in section 2.4.2 of the course reference book, "An Introduction To Information Retrieval" by Christopher D. Manning, Prabhakar Raghavan, and Hinrich Schütze.
# Answering the user's question
In this section, upon receiving the user's question, the relevant documents in a binary form should be returned. This could be done via too methods below:
	Single word: it is enough to retrieve the list of related documents from the dictionary.
	A few words: In this section, the list of files should be sorted based on the degree of connection. The most relevant document is a document that has all the words in the same order as in the query. (For example, if the query contained 3 words, the most relevant document is the one that contains all three words, then the relevant document that contains two of the query words.)
# Data sets
The dataset used in this project is a collection of news collected from several Persian news websites, which will be
provided to you in the form of an Excel file. It is necessary to process only the "content " column as the content of the
document. Consider the number of each news as the ID of that document (news) and when answering the question, display the title of the news related to the retrieved document so that it is possible to check the correctness of the system.

# Zipf's law
According to Zipf’s law The rth most frequent term has frequency proportional to 1/r or:
 cfi∝1/r --> cfi= k/r --> log cf=log k - log r
where k is a normalizing constant and cf is collection frequency: the number of occurrences of the term t in the collection.
 
As can be seen, the Zipf rule applies with k equal to 72563, with repeated words removed.
 
Zipf rule also applies with k equal to 80430 while repeated words are not removed. However, in the second case, more normalization is needed with a higher k, and in the first case, this rule is more applicable. It should be noted that k is obtained by the average of the set of dot multiplication or element-wise of the rank set of words (according to the frequency of their appearance in the documents).
# The validity of Heap's law 
Heaps’ law: 
M = kT^b --> log M=log k + b × log T 
Where M is the size of the vocabulary, T is the number of tokens in the collection, 0.4<b<0.6, and 30 > k < 100. In a log-log plot of vocabulary size M vs. T, Heaps’
law predicts a line with a slope of about 1/2. Both Heap's law and Zipf's law are empirical.
We use the least squares method to calculate the parameters of Heap's law.

![image](https://github.com/MahdiTheGreat/searchEngine/assets/47212121/694a3183-a57a-4688-830f-6dc264e16405)


As you can see, with different numbers of documents, in both cases with rooting and without rooting, Heap's law applies, but since the number of tokens and words increases without rooting, it is natural to see more errors and there is a greater distance between the predicted value and the actual size of the dictionary, and as a result, the law of heaps is less applicable. In other words, due to the side effects of not using rooting, which is equal to increasing the number of tokens, the law of heaps is less applicable in this case, and rooting by itself does not have much effect. Below are Diagrams related to Heap's law in both cases with rooting and without rooting for the number of documents equal to 500, 1000, 1500, and 2000. These diagrams are shown in the specified order.

![image](https://github.com/MahdiTheGreat/searchEngine/assets/47212121/5764dbaf-d4a0-44b9-9c95-beeefe63aaaa)

![image](https://github.com/MahdiTheGreat/searchEngine/assets/47212121/f5a47f15-6c1f-4ff9-b704-4e1a282cfb0b)

![image](https://github.com/MahdiTheGreat/searchEngine/assets/47212121/803de3b2-074b-4afd-80ca-69544215d7c6)

![image](https://github.com/MahdiTheGreat/searchEngine/assets/47212121/bd3e52a4-6a00-4fed-be80-0c619a6605d6)

![image](https://github.com/MahdiTheGreat/searchEngine/assets/47212121/388d9bd9-b9a3-463b-a913-261df27873f4)

![image](https://github.com/MahdiTheGreat/searchEngine/assets/47212121/f7b80832-581f-4351-8c46-b2890ea2c310)

![image](https://github.com/MahdiTheGreat/searchEngine/assets/47212121/15e4fdb4-e68d-4954-a6a5-cd88b107571d)

![image](https://github.com/MahdiTheGreat/searchEngine/assets/47212121/a8588723-668e-4f0c-9513-cd12b43cbb04)








 
 
 
 
 
 
 
 


 
 
 
 
 
 
 
 




