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

def calcul_IDF(*docs):
    idfDict = {}
    N = len(docs)
    #initializing idf dictionary
    idfDict = dict.fromkeys(docs[0].keys(), 0)
    for terme in idfDict:
        idfDict[terme] = math.log10(N / float(sum(doc[terme] > 0 for doc in docs)))
    return idfDict

def calcul_TFIDF(tf, idf):
    tfidf = {}
    for terme, val in tf.items():
        tfidf[terme] = val*idf[terme]
    return tfidf
