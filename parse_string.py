""" This is a file which demonstrates function calls for the sentence/post/comment vectors

"""

from general_easyness import lprint
from prepare_string import additive, multiplicative, prep
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def cosine_sym_single(wv1, wv2):
    """ wrapper function for cosine similarity

    created for the usecase of comparing a single pair of vectors

    : single :  meaning-vector, received from either additive or multiplicative
    : other :   vectors like single
    """
    return cosine_similarity(wv1.reshape(1,-1), wv2.reshape(1,-1))

def cosine_sym_multi(wvs1, wvs2):
    """
    : single :  meaning-vector, received from either additive or multiplicative
    : others :  multiple vectors like single, added together using numpy.vstack([...])
    """
    try:
        return cosine_similarity(wvs1, wvs2)
    except:
        return cosine_similarity(wvs1.reshape(1,-1), wvs2)

def difference_vector(post, comment):
    """ computes the difference in meaning space between two vectors
    """
    return comment - post

testQ = "John Sato, a 95 year old WWII Veteran, takes FOUR busses to attend rally in support of Christchurch massacre victims. Sato is pictured here gripping a police officer and stranger for support."
testAs = ["""The NZ police drove him back home afterwards. He had an interview on the news tonight, a real bro

                Edit :

                ”A policeman took me all the way home and waited down there until he saw me get up the stairs,” Sato said. “He was very kind.”""",
        """That's what Protect & Serve stands for. Amazing.""",
        """New Zealand police always come across as kind.""",
        """Kiwis are such wholesome people. IRL Hobbits if you ask me (in the best way possible).""",
        """Link to SBS Article""",
        """A true bro. I hope someone drove him home""",
        """Read this thinking he paid for four buses of people to go to the rally.

        Which is a pretty broesome thing to do.

        Then felt confused on why he needed a ride home. Then figured it out and thought that guys really wholesome in a completely different way.""",
        "Dude on the right there looks like every Kiwi I’ve ever met in a bar while on holiday.",
        "Dude has AMAZING hair Sincerely, a balding young guy"
        ]

testAs = [prep(a) for a in testAs]
d = difference_vector(additive(testAs[0]), additive(testAs[0]))
newQ = "who is John Sato?"

similarities = cosine_sym_multi(d + additive(prep(newQ)), np.vstack([additive(prep(a)) for a in testAs]))
lprint(similarities)
lprint(similarities.tolist())

print("WHoa!?!")
lprint([[sym, testAs[i]] for i, sym in enumerate(similarities.tolist())])

#
#
# adQ, adA = additive(prep(testQ)), additive(prep(testA))
# muQ, muA = multiplicative(prep(testQ)), multiplicative(prep(testA))
#
#
# sim = cosine_sym_single(adQ,adA)
# print(sim)
# sim = cosine_sym_single(adQ,muA)
# print(sim)
# sim = cosine_sym_single(muQ,adA)
# print(sim)
# sim = cosine_sym_single(muQ,muA)
# print(sim)
# sim = cosine_sym_multi(np.vstack([adQ, muQ]), np.vstack([adA, muA]))
# print(sim)
