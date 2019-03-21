
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from autocorrect import spell

import gensim
import numpy as np

from general_easyness import lprint

model = gensim.models.KeyedVectors.load_word2vec_format('./GoogleNews-vectors-negative300.bin', binary=True)
stop_words = set(stopwords.words('english'))

def multiplicative(list_of_words):
    "returns multiplicative value of word embeddings"
    datavalue = model.word_vec(list_of_words[0])
    for word in list_of_words[1:]:
        datavalue = np.multiply(wordvalue, model.word_vec(word))
    return datavalue

def additive(list_of_words):
    "returns additive value of word embeddings"
    datavalue = model.word_vec(list_of_words[0])
    for word in list_of_words[1:]:
        datavalue = wordvalue + model.word_vec(word)
    return datavalue



def prep(datastring):
    """ prepares post or comment content for the word2vec model.

    corrects misspelled words, removes unwanted textsigns,
        unicode (unsure (test needed)) and words not included in the word2vec model

    : datastring : content of a comment
    """
    cleaned_words = ''.join(e for e in datastring if e.isalnum() or e.isspace()).lower().split(" ")
    potential_words = [spell(elem) for elem in cleaned_words]
    return [w for w in potential_words if (w not in stop_words) and (w in model)]

if __name__ == "__main__":

    testW = ["reasoning"]
    testQ = "can a neural network simulate reasoning".split(" ")
    testA = "a neural network cannot simulate".split(" ")
    model.word_vec(testW[0])

    additive(testA)
    multiplicative(testA)

    wack_shiet = u"scheme://username:password @subdoman .domain. tld :port /path/file-name .suffix?query-string#hash"

    lprint(prep(wack_shiet))

    print(spell("2poieu3yi?"))