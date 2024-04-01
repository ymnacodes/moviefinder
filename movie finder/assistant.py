from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import string
import nltk
import math

def data_clean(data):
    # Convert to lowercase
    data = data.lower()

    # Remove punctuation
    data = data.translate(str.maketrans('', '', string.punctuation))

    # Tokenize text into words
    words = nltk.word_tokenize(data)

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]

    # Lemmatize words
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(w) for w in words]

    return words

def calcul_TF(terms, doc):
    tfDict = {}
    docCount = len(doc)
    for term, count in terms.items():
        tfDict[term] = count/float(docCount)
    return tfDict

def calcul_IDF(*args):
    idfDict = {}
    N = len(args)
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
    quotiont = sum(documents_vectors[i]*query_vector[i] for i in range(len(documents_vectors)))
    dom1 = sum(pow(documents_vectors[i], 2) for i in range(len(documents_vectors)))
    dom2 = sum(pow(query_vector[i], 2) for i in range(len(query_vector)))
    if dom1 == 0 or dom2 == 0:
        return 0
    result = quotiont/math.sqrt(dom1*dom2)
    return result