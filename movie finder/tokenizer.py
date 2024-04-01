import os
import string
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import nltk
import math
from assistant import *

def load_data(directory):
    data_list = []
    filenames = []
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), "r", encoding= "utf-8") as f:
            data = f.read()
        data_list.append(data)
        filenames.append(filename)
    return data_list, filenames

corpus, filenames = load_data("MovieScriptsList")

cleaned_corpus = [data_clean(doc) for doc in corpus]

#must be inputed
query = "luke, I am your father"

#cleaning query
tokenized_query = data_clean(query)
print(tokenized_query)


# Unify words in cleaned_corpus
union_set = set()
for document in cleaned_corpus:
    union_set.update(document)

# Convert set to list
terms = list(union_set)

# Calculate Number of appearances of each term in each document
cleaned_corpus_terms = []
for i in range(len(cleaned_corpus)):
    dictionary = dict.fromkeys(terms, 0)
    for j in cleaned_corpus[i]:
        dictionary[j] += 1
    cleaned_corpus_terms.append(dictionary)

# Calculate TF
tf_list = []
for i in range(len(cleaned_corpus)):
    tf_list.append(calcul_TF(cleaned_corpus_terms[i], cleaned_corpus[i]))

# Calculate IDF
idf = calcul_IDF(*cleaned_corpus_terms)

# Calculate TFIDF
tfidf_list = []
for i in range(len(cleaned_corpus)):
    tfidf_list.append(calcul_TFIDF(tf_list[i], idf))

# Represent query as vector
query_vector = []
for term in terms:
    if term in query:
        query_vector.append(1)
    else:
        query_vector.append(0)

# Represent documents as vectors
documents_vectors = []
for i in range(len(cleaned_corpus)):
    documents_vectors.append(list(tfidf_list[i].values()))

# Calculate correspondance between query and documents
correspondance = []
for i in range(len(cleaned_corpus)):
    correspondance.append(calcul_correspondance(documents_vectors[i], query_vector))
    
results = sorted(range(len(correspondance)), key=lambda i: correspondance[i], reverse=True)[:10]
results = list(filter(lambda i: correspondance[i] != 0, results))

final_result = filenames[results[0]]
