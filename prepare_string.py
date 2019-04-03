
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from autocorrect import spell

import gensim
import numpy as np

from general_easyness import lprint, remove_special


from tqdm import tqdm
import stopit

import time
from tqdm import tqdm

spelling_dict = dict()

@stopit.threading_timeoutable(default='timoutspell')
def speel_corrector(word):
    return spell(word)

model = gensim.models.KeyedVectors.load_word2vec_format('./model.bin', binary=True)
stop_words = set(stopwords.words('english'))

def multiplicative(list_of_words):
    "returns multiplicative value of word embeddings"
    datavalue = get_word_vec(list_of_words, 0)
    rest = list_of_words[1:]
    for i, word in enumerate(rest):
        datavalue = np.multiply(datavalue, get_word_vec(rest, i))
    return datavalue

def additive(list_of_words):
    "returns additive value of word embeddings"
    datavalue = get_word_vec(list_of_words, 0)
    rest = list_of_words[1:]
    for i, word in enumerate(rest):
        datavalue = datavalue + get_word_vec(rest, i)
    return datavalue

def get_word_vec(list_of_words, i):
    try:
        if not list_of_words[i]:
            print("print because ''", i)
            raise ValueError("invalid input for word vec")
        datavalue = model.word_vec(list_of_words[0])
    except:
        datavalue = np.zeros((300,))
    return datavalue

def cleaned_to_chosen(cleaned_words, with_pbar=False):
    words = []
    not_stop = []
    in_vocab = []
    for w in cleaned_words:
        spelled = spelling_dict.get(w, False)
        if not spelled:
            maybe_spelled = speel_corrector(w, timeout=1)
            if maybe_spelled == 'timoutspell':
                maybe_spelled = w
                spelled = maybe_spelled
            spelling_dict[w] = maybe_spelled
            spelled = maybe_spelled
        if spelled:
            if (not spelled in stop_words):
                not_stop.append(spelled)
                if spelled in model.wv.vocab:
                    words.append(spelled)
            if spelled in model.wv.vocab:
                in_vocab.append(spelled)
        if with_pbar:
            with_pbar.update(1)
    return words


def prep(datastring, verbose=True):
    """ prepares post or comment content for the word2vec model.

    corrects misspelled words, removes unwanted textsigns,
        unicode (unsure (test needed)) and words not included in the word2vec model

    : datastring : content of a comment or title + post
    """
    s = remove_special(datastring)
    cleaned_words = ''.join(s).lower().split(" ")
    if verbose:
        with tqdm(total=len(cleaned_words), desc="processing and selecting useful words", bar_format="{l_bar}{bar} [ time left: {remaining} ]") as pbar:
            return cleaned_to_chosen(cleaned_words, pbar)
    else:
        return cleaned_to_chosen(cleaned_words)

if __name__ == "__main__":

    testW = ["reasoning"]
    testQ = "can a neural network simulate reasoning".split(" ")
    testA = "a neural network cannot simulate".split(" ")
    model.word_vec(testW[0])
