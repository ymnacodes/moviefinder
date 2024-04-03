from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import string
import nltk
import math

def data_clean(data):

    # Convert to lowercase
    data = data.lower()

    # Remove punctuation: i.e periods, commas, exclamation marks, etc.
    data = data.translate(str.maketrans('', '', string.punctuation))

    # Tokenize text into words
    words = nltk.word_tokenize(data)

    #Remove StopWords through creating a set of eng StopWords
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]

    # Lemmantize (return to base/root) words only
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(w) for w in words]

    return words

def calcul_TF(terms, doc):
    #Empty dict to store doc descriptor
    tfDict = {}
    #number of terms for loop
    docCount = len(doc)
    for term, count in terms.items():
        tfDict[term] = count/float(docCount)
    return tfDict

def calcul_IDF(*args):
    idfDict = {}
    N = len(args)
    #initializing idf dictionary
    idfDict = dict.fromkeys(args[0].keys(), 0)
    for terme in idfDict:
        idfDict[terme] = math.log10(N / float(sum(arg[terme] > 0 for arg in args)))
    return idfDict

def calcul_TFIDF(tf, idf):
    tfidf = {}
    for terme, val in tf.items():
        tfidf[terme] = val*idf[terme]
    return tfidf

def calcul_correspondance(documents_vectors, query_vector):
    # Calculate dot product
    quotient = sum(doc * query for doc, query in zip(documents_vectors, query_vector))

    # Calculate magnitudes of vectors
    dom1 = sum(pow(doc, 2) for doc in documents_vectors)
    dom2 = sum(pow(query, 2) for query in query_vector)

    # Check for division by zero
    if dom1 == 0 or dom2 == 0:
        return 0
    # Calculate cosine similarity
    result = quotient / (math.sqrt(dom1) * math.sqrt(dom2))
    return result