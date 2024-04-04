import os
from assistant import *
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


def load_data(directory):
    data_list = []
    filenames = []
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), "r", encoding= "utf-8") as f:
            data = f.read()
        data_list.append(data)
        filenames.append(filename)
    return data_list, filenames

src = r'movie finder\MovieScriptsList'
corpus, filenames = load_data(src)

cleaned_corpus = [data_clean(doc) for doc in corpus]

def querytomovies(cleaned_corpus,query):
    # Cleaning query
    tokenized_query = data_clean(query)
    query = ' '.join(tokenized_query)

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
    cleaned_corpus = [' '.join(doc) for doc in cleaned_corpus]
    # Create a TfidfVectorizer object
    vectorizer = TfidfVectorizer()

    # Fit the vectorizer to the cleaned_corpus and transform the cleaned_corpus into a TF-IDF matrix
    tfidf_matrix = vectorizer.fit_transform(cleaned_corpus)

    # Transform the query into a TF-IDF vector
    query_vector = vectorizer.transform([query])

    # Calculate the cosine similarity between the query vector and each document vector
    correspondance = cosine_similarity(query_vector, tfidf_matrix)

    # Get the indices of the documents sorted by their similarity to the query
    results = correspondance.argsort()[0][::-1][:10]
    #print(results)

    # Store movie details in a list after filtering the name.
    movies = []
    for i in results[:10]:
        movies.append(moviename(filenames[i]))

    return movies



def moviename(filename):
    # Remove '-' characters from the filename
    filename = filename.replace('-', ' ').replace('_',' ')
    
    # Remove the file extension
    name = filename.split('.')[0]
    
    # Split the name by spaces and capitalize each word
    name_parts = name.split(' ')
    capitalized_name = ' '.join([part.capitalize() for part in name_parts])
    
    # Append 'Trailer' to the capitalized name
    movie_name = capitalized_name + ' Trailer'
    
    return movie_name